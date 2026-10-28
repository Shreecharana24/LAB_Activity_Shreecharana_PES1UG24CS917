# Lab 5 — Static Code Analysis

This lab analyzes and improves the student attendance tracker from the
[assigned Lab 5 repository](https://github.com/SETAPESU26/L5_61_attendance-tracker)
using Pylint, Bandit, and Flake8. All Lab 5 deliverables for this coursework
are kept in this repository's `lab5/` folder.

## Deliverables

- `attendance_tracker.py`: cleaned and updated attendance tracker.
- `issues.md`: prioritized findings and remediation table.
- `reflection.md`: four reflection responses based on the handout's learning
  outcomes. The handout references four questions but does not include their
  exact text.
- `reports/before/` and `reports/after/`: analyzer reports and program output.
- `tests/`: regression tests for attendance logic, CSV export, and integrations.

## Run the application and tests

From this directory:

```powershell
python -m pip install requests
python .\attendance_tracker.py
python -m unittest discover -s tests -v
```

ERP synchronization requires `ERP_API_KEY`; the application reports a clear
error if synchronization is requested without the key. It is not necessary to
set credentials to run the included offline demonstration.

## Run static analysis

Install the analyzers:

```powershell
python -m pip install pylint bandit flake8
```

Run them from this directory:

```powershell
python -m pylint .\attendance_tracker.py
python -m bandit -r .\attendance_tracker.py
python -m flake8 .\attendance_tracker.py .\tests
```

The final result is Pylint 10.00/10, zero Bandit findings, and no Flake8
violations.
