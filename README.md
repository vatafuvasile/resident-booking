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
```

This is an in-memory domain prototype, not a deployed council service.
