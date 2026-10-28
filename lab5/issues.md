# Static Analysis Findings and Fixes

The before reports were generated from the original `attendance_tracker.py`.
Line numbers in this table refer to that original file, before changes.
Findings are ordered by severity, with the highest-severity items first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| TLS certificate verification disabled | Bandit B501 — High | 60 | `verify=False` allowed an ERP connection to accept an untrusted certificate, enabling interception. | Removed the override and kept Requests' default certificate verification enabled. |
| Shell command with wildcard and shell execution | Bandit B609/B602 — High / Low | 64 | A shell command used `*.csv` and `shell=True`, which risks command and wildcard injection. | Replaced the shell command with `tarfile` and explicit CSV paths. |
| Hard-coded ERP API credential | Manual security review — High | 12 | A credential was embedded in source code and would be exposed to anyone with repository access. | Read the key from `ERP_API_KEY` at runtime and fail explicitly if it is missing. |
| ERP request had no timeout | Bandit B113 — Medium | 60 | The request could hang indefinitely if the server did not respond. | Added a finite request timeout and call `raise_for_status()` to report HTTP errors. |
| Obsolete TLS protocol default | Bandit B503 — Medium | 66 | The legacy helper selected TLS 1.0, which is not safe for current connections. | Removed the legacy helper; ERP requests now use Requests' secure TLS defaults. |
| Reminder helper enabled shell execution | Bandit B604 — Medium | 73 | The reminder command was represented with `shell=True`, making later execution unsafe. | Return an argument list and do not invoke a shell. |
| Shared mutable default register | Pylint W0102 — Warning | 18 | Calls shared the same default dictionary, causing attendance from unrelated calls to leak together. | Require callers to pass an explicit register, created locally for each run. |
| Empty attendance and incorrect threshold | Runtime review — Bug | 23, 30 | A student with no records caused division by zero, and exactly 75% was incorrectly ineligible. | Return 0 for no working days and treat the configured threshold as inclusive. |
| Duplicate and malformed attendance dates | Runtime review — Bug | 25, 82–83 | Repeated dates inflated attendance, and lexicographic comparison of non-padded dates could select the wrong latest date. | Validate and normalize ISO dates, update an existing day's status, and keep the register unique. |
| Spreadsheet formula injection in exported names | Manual security review — Medium | 49, 53, 77 | A name beginning with a formula marker could execute as a spreadsheet formula when the CSV was opened. | Prefix spreadsheet-sensitive values with a text marker before writing the CSV. |
| Pylint quality and naming findings | Pylint — Low | Multiple | Missing documentation, non-snake-case names, unused imports, and simplifiable logic reduced maintainability; the baseline score was 4.55/10. | Added documentation and type annotations, used consistent naming, removed unused imports, and simplified the logic. |
| Flake8 style findings | Flake8 — Low | Multiple | The original file had unused imports, spacing errors, and lines exceeding the configured limit. | Removed unused imports and reformatted the file to satisfy Flake8. |

## Verification

The final application scored **10.00/10** with Pylint, produced **no
Bandit findings**, and produced **no Flake8 violations**. The regression
suite also verifies attendance behavior, CSV escaping, backup creation,
and ERP integration safeguards. See `reports/before/` and `reports/after/`
for the saved tool output.
