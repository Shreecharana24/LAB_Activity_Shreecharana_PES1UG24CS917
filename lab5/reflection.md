# Lab 5 Reflection

The supplied handout asks for four reflection answers but does not provide
the question text. These responses address the lab's learning outcomes.

## 1. What did static analysis reveal about the original program?

Pylint and Flake8 exposed basic maintainability problems such as missing
documentation, inconsistent naming, unused imports, and formatting errors.
Bandit identified disabled HTTPS certificate verification, an unbounded
network request, an obsolete TLS protocol, and shell-enabled commands. Running
the demo also revealed logic problems that the tools could not fully judge:
duplicate dates were counted twice, a 75% attendance value failed eligibility,
and an empty record set could cause division by zero.

## 2. Which findings were most important to fix, and why?

The highest-priority changes removed the shell-based archive operation and
restored certificate verification for ERP traffic. The embedded API credential
was moved to an environment variable, and the request now has a timeout and
raises HTTP errors explicitly. These changes reduce the risk of command
injection, credential exposure, traffic interception, and a request that
never completes.

## 3. How did I verify the changes?

I saved baseline reports, fixed the findings, and reran all three tools. The
final results were Pylint 10.00/10, zero Bandit findings, and no Flake8
violations. Nine unit tests cover duplicate attendance updates, holiday and
empty-record percentages, the 75% boundary, date handling, CSV formula
escaping, archive contents, and ERP key/timeout behavior. I also ran the
demo and checked that it reports a unique register and a correctly ordered
latest date.

## 4. What are the limitations of static analysis, and how will I use it?

Static analyzers find patterns, not every incorrect business rule. They did
not decide whether holidays belong in the attendance denominator, whether
exactly 75% qualifies, or how duplicate attendance dates should behave; those
required reviewing the program's output and expected behavior. Analyzer
warnings also need judgment: this demo uses randomness nowhere, and a clean
Bandit run does not replace dependency updates or runtime testing. I would run
the tools and unit tests during development and review their findings alongside
the actual requirements.
