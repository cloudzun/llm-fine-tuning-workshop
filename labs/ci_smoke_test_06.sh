#!/usr/bin/env bash
set -e
python - <<'PY'
try:
    import detoxify
    print('DETOX_OK')
except Exception as e:
    print('DETOX_MISSING', e)
    raise
print('SMOKE OK')
PY
