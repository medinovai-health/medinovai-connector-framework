#!/usr/bin/env bash
# medinovai-connector-framework — Harness 2.1 init (Python / FastAPI)
set -euo pipefail

E_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${E_ROOT}"

mos_python="${PYTHON:-python3}"
if ! command -v "${mos_python}" &>/dev/null; then
  echo "ERROR: ${mos_python} not found"
  exit 1
fi

if [[ ! -d .venv ]]; then
  "${mos_python}" -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate

pip install --upgrade pip >/dev/null
pip install -r requirements.txt

export PYTHONPATH="${E_ROOT}/src:${PYTHONPATH:-}"
python -c "from main import app; print('import_ok', app.title)"

echo "Smoke: uvicorn not started (run: uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000)"
echo "init.sh PASS"
