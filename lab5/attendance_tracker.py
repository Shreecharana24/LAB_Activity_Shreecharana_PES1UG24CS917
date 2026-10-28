"""Attendance tracking, reporting, and ERP integration."""

import csv
import os
import tarfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import requests

ERP_URL = "https://erp.college.example/api/attendance"
MIN_ATTENDANCE = 75
VALID_STATUSES = {"P", "A", "L", "H"}
REQUEST_TIMEOUT = 10


@dataclass
class Student:
    """A student's profile and dated attendance records."""

    name: str
    section: str = "A"
    records: list[tuple[str, str]] = field(default_factory=list)


students: dict[str, Student] = {}


def add_student(roll_no: str, name: str, section: str = "A") -> None:
    """Add or replace a student in the attendance register."""
    students[roll_no] = Student(name=name, section=section)


def mark_attendance(
    roll_no: str,
    attendance_date: str,
    status: str,
    register: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Record or update one student's status for an ISO calendar date."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported attendance status: {status}")

    normalized_date = date.fromisoformat(attendance_date).isoformat()
    student = students[roll_no]
    existing_index = next(
        (
            index
            for index, (record_date, _) in enumerate(student.records)
            if record_date == normalized_date
        ),
        None,
    )
    if existing_index is None:
        student.records.append((normalized_date, status))
    else:
        student.records[existing_index] = (normalized_date, status)

    attendees = register.setdefault(normalized_date, [])
    if roll_no not in attendees:
        attendees.append(roll_no)
    return register


def attendance_percentage(roll_no: str) -> int:
    """Return a student's attended percentage, excluding holidays."""
    records = students[roll_no].records
    working_days = [status for _, status in records if status != "H"]
    if not working_days:
        return 0

    present_days = sum(status == "P" for status in working_days)
    return int(present_days / len(working_days) * 100)


def is_eligible(percentage: int) -> bool:
    """Check whether a percentage meets the minimum attendance threshold."""
    return percentage >= MIN_ATTENDANCE


def shortage_list() -> list[str] | None:
    """Return roll numbers below the attendance threshold, if any."""
    shortages = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return shortages or None


def has_long_absence(roll_no: str, days: int = 3) -> bool:
    """Check whether a student has the requested consecutive absences."""
    if days < 1:
        raise ValueError("days must be at least 1")

    statuses = [status for _, status in students[roll_no].records]
    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no: str) -> str | None:
    """Return a student's latest ISO attendance date, if recorded."""
    records = students[roll_no].records
    return max((record_date for record_date, _ in records), default=None)


def _spreadsheet_safe(value: str) -> str:
    """Prevent spreadsheet applications from evaluating formula-like cells."""
    if value.startswith(("=", "+", "-", "@", "\t", "\r")):
        return f"'{value}"
    return value


def export_csv(path: str | Path = "attendance.csv") -> Path:
    """Export student attendance percentages to a UTF-8 CSV file."""
    output_path = Path(path)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])
        for roll_no, student in students.items():
            writer.writerow(
                [
                    _spreadsheet_safe(roll_no),
                    _spreadsheet_safe(student.name),
                    attendance_percentage(roll_no),
                ]
            )
    return output_path


def sync_to_erp(roll_no: str) -> int:
    """Send attendance to the ERP using validated TLS and a bounded timeout."""
    api_key = os.getenv("ERP_API_KEY")
    if not api_key:
        raise RuntimeError("Set ERP_API_KEY before syncing attendance.")

    response = requests.post(
        os.getenv("ERP_URL", ERP_URL),
        json={
            "roll_no": roll_no,
            "pct": attendance_percentage(roll_no),
        },
        headers={"X-API-Key": api_key},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.status_code


def backup_reports(directory: str | Path = ".") -> Path:
    """Create a gzip tar archive of CSV reports in a directory."""
    report_directory = Path(directory)
    report_files = sorted(report_directory.glob("*.csv"))
    if not report_files:
        raise FileNotFoundError(f"No CSV reports found in {report_directory}.")

    archive_path = report_directory / "reports_backup.tgz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for report_file in report_files:
            archive.add(report_file, arcname=report_file.name)
    return archive_path


def schedule_reminders() -> list[str]:
    """Return the reminder command as arguments without invoking a shell."""
    return ["send_sms", "--shortage"]


def main() -> None:
    """Run a small attendance-tracker demonstration."""
    students.clear()
    attendance_register: dict[str, list[str]] = {}
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')

    first_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]
    second_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-06", "P"),
    ]
    for attendance_date, status in first_student_records:
        mark_attendance("R01", attendance_date, status, attendance_register)
    for attendance_date, status in second_student_records:
        mark_attendance("R02", attendance_date, status, attendance_register)

    mark_attendance("R01", "2030-01-01", "P", attendance_register)
    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        attendance_register["2026-09-01"],
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no credentials configured)")


if __name__ == "__main__":
    main()
