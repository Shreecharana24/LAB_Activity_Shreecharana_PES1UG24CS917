"""Unit tests for attendance tracking and report safety."""

import csv
import os
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import attendance_tracker as tracker


class AttendanceTrackerTests(unittest.TestCase):
    """Verify attendance calculations and safe report operations."""

    def setUp(self):
        tracker.students.clear()
        self.register = {}
        tracker.add_student("R01", "Aditi")

    def test_marking_same_date_updates_instead_of_duplicating(self):
        tracker.mark_attendance("R01", "2026-09-01", "P", self.register)
        tracker.mark_attendance("R01", "2026-09-01", "A", self.register)

        self.assertEqual(
            tracker.students["R01"].records,
            [("2026-09-01", "A")],
        )
        self.assertEqual(self.register, {"2026-09-01": ["R01"]})

    def test_percentage_excludes_holidays_and_handles_empty_records(self):
        self.assertEqual(tracker.attendance_percentage("R01"), 0)
        tracker.mark_attendance("R01", "2026-09-01", "P", self.register)
        tracker.mark_attendance("R01", "2026-09-02", "H", self.register)
        tracker.mark_attendance("R01", "2026-09-03", "L", self.register)

        self.assertEqual(tracker.attendance_percentage("R01"), 50)

    def test_eligibility_includes_exact_threshold(self):
        self.assertTrue(tracker.is_eligible(75))
        self.assertFalse(tracker.is_eligible(74))

    def test_latest_date_uses_normalized_iso_dates(self):
        tracker.mark_attendance("R01", "2026-09-09", "P", self.register)
        tracker.mark_attendance("R01", "2026-09-10", "P", self.register)

        self.assertEqual(tracker.latest_date("R01"), "2026-09-10")
        tracker.add_student("R02", "Bharat")
        self.assertIsNone(tracker.latest_date("R02"))

    def test_invalid_status_and_date_are_rejected(self):
        with self.assertRaises(ValueError):
            tracker.mark_attendance("R01", "2026-09-01", "X", self.register)
        with self.assertRaises(ValueError):
            tracker.mark_attendance("R01", "2026-9-1", "P", self.register)

    def test_long_absence_checks_consecutive_records(self):
        for day in range(1, 4):
            tracker.mark_attendance(
                "R01",
                f"2026-09-0{day}",
                "A",
                self.register,
            )

        self.assertTrue(tracker.has_long_absence("R01"))
        with self.assertRaises(ValueError):
            tracker.has_long_absence("R01", days=0)

    def test_csv_export_escapes_spreadsheet_formulas(self):
        formula_name = '=HYPERLINK("https://example.test","Aditi")'
        tracker.students["R01"].name = formula_name
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "attendance.csv"
            tracker.export_csv(output_path)

            with output_path.open(encoding="utf-8", newline="") as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(rows[1][1][0], "'")

    def test_backup_contains_csv_without_shell_execution(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "attendance.csv"
            report_path.write_text("roll_no,name\n", encoding="utf-8")

            archive_path = tracker.backup_reports(temporary_directory)

            with tarfile.open(archive_path, "r:gz") as archive:
                self.assertEqual(archive.getnames(), ["attendance.csv"])

    def test_erp_sync_requires_key_and_uses_request_timeout(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ERP_API_KEY"):
                tracker.sync_to_erp("R01")

        response = Mock(status_code=200)
        with patch.dict(os.environ, {"ERP_API_KEY": "test-key"}, clear=True):
            with patch.object(
                tracker.requests,
                "post",
                return_value=response,
            ) as post:
                self.assertEqual(tracker.sync_to_erp("R01"), 200)

        timeout = post.call_args.kwargs["timeout"]
        self.assertEqual(timeout, tracker.REQUEST_TIMEOUT)
        self.assertNotIn("verify", post.call_args.kwargs)
        response.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
