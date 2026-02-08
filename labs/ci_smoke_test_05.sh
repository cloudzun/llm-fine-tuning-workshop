#!/usr/bin/env bash
set -e
# Light-weight smoke test: check if serve script imports transformers
python - <<'PY'
try:
    import transformers
    print('TRANSFORMERS_OK')
except Exception as e:
    print('IMPORT_FAIL', e)
    raise
print('SMOKE OK')
PY
