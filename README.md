# Automated-build-with-MISE

Manage CI build workflow and tasks using MISE-EN-PLACE to install dependencies, lint, run unit tests with coverage, run the utility, and print project info for a small Python utilities project.

[![CI build workflow badge for the repository Automated-build-with-MISE showing the GitHub Actions workflow name CI build workflow with MISE-EN-PLACE and the current build status for branch main; text on badge reads CI build workflow with MISE-EN-PLACE and a status label such as passing or failing; neutral informational tone.](https://github.com/Brisinger/Automated-build-with-MISE/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Brisinger/Automated-build-with-MISE/actions/workflows/ci.yml)

## Overview

This repository contains a small Python utility module (`utilities/util.py`) that provides robust temperature conversion functions with strict input validation and a custom exception type. Tests are defined in `tests/test_util.py` and run with `pytest`.

The project uses MISE-EN-PLACE to manage tooling, virtualenvs, and common tasks via `mise.toml`. The repository also includes `scripts/trust-mise.sh` to help trust the `mise.toml` configuration when running in CI or locally.

## MISE usage (preferred)

If you have `mise` installed, the project defines convenient tasks in `mise.toml`. Typical workflow:

```bash
# Trust the mise.toml (one-time; creates a .mise_trusted marker)
bash scripts/trust-mise.sh

# Install dependencies and tools defined by mise
mise run install

# Run tests (runs lint -> install -> pytest)
mise run test

# Run tests with coverage and generate XML/HTML reports
mise run coverage

# Run the full build pipeline
mise run build
```

## Standard Python usage (without mise)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Lint
pylint utilities/

# Run tests
pytest -q

# Coverage reports
pytest --cov=utilities --cov-report=xml:tests/coverage/coverage.xml --cov-report=html:tests/coverage/html tests/
```

## Files of interest

- `utilities/util.py` — temperature conversion utilities and `TemperatureFormatNotSupported` exception.
- `tests/test_util.py` — unit tests using `pytest`.
- `mise.toml` — MISE tasks and env configuration.
- `scripts/trust-mise.sh` — helper to trust `mise.toml`.
- `.github/workflows/ci.yml` — CI workflow that uses MISE in GitHub Actions.

## Contributing

Contributions, issues and feature requests are welcome. For CI-related changes, keep `mise.toml` in sync with workflow expectations.
