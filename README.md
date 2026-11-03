# Resident appointment booking

SWE6301 educational prototype. AI-assisted development is disclosed in
AI_USAGE.md. Uses synthetic resident identifiers; no real resident data.

## Run

Requires Python 3.10 or later.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m behave --no-color --format plain
python -m unittest discover -s tests -v
python demo.py
```

This is an in-memory domain prototype, not a deployed council service.

## Scope and rules

The main stakeholder is a resident seeking a council support appointment.
Only offered future slots can be reserved. All datetimes need a UTC offset.
Resident identifiers use 1–40 ASCII letters, digits, underscores or hyphens.
Rejected requests leave existing reservations unchanged. The fixed demo
clock makes results reproducible after the demonstration dates have passed.
Real integration must inject an appropriate current clock.

Three BDD scenarios cover success, malformed input and an occupied slot.
Sixteen unittest checks cover extra boundaries and state integrity.
Evidence files are actual captured runs, including pre-fix failures.
An invalid booking is expected business behaviour: its final BDD scenario
passes when the booking is correctly rejected. This is distinct from the
genuinely failing scenario runs saved during development.

## Limitations

There is no database, authentication, web interface, cancellation, live
council integration or protection against concurrent requests. Data is lost
when the process exits. The prototype does not establish accessibility,
security or legal compliance. Production reservation requires transactional
storage and a unique constraint on the slot, plus appropriate access control,
retention rules, monitoring and usability testing. Synthetic IDs are a demo
choice, not proof of anonymisation in a real system.

## Repository and submission

This directory contains the real local Git repository. No remote repository
has been created. Create an empty repository in your own account, then run:

```sh
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace YOUR_REPOSITORY_URL with the actual URL. Add it to the report and
check that your marker has access. Do not initialise the remote with a README
if you intend to push this existing history. Use requirements-lock.txt to
reproduce the exact dependency versions used for the captured runs.
