#!/usr/bin/env bash
# Set up a Python development environment for this repository.
# Usage: ./install_dev_env.sh   (run from the repository root)
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

echo "==> Checking prerequisites"
for cmd in git "$PYTHON_BIN"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: '$cmd' is not installed. Install it and re-run." >&2
    exit 1
  fi
done
echo "    git:    $(git --version)"
echo "    python: $("$PYTHON_BIN" --version)"

echo "==> Creating virtual environment in $VENV_DIR"
if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  echo "    already exists, reusing it"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Installing dependencies"
python -m pip install --upgrade pip >/dev/null
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install pytest pytest-mock
fi

echo "==> Running the test suite"
pytest

echo "Done. Activate the environment later with: source $VENV_DIR/bin/activate"
