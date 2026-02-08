#!/usr/bin/env bash
set -e
python labs/03_clean_and_stats.py labs/sample.txt > /tmp/clean_stats_out.txt
grep -q "TOTAL" /tmp/clean_stats_out.txt && echo "SMOKE OK" || (cat /tmp/clean_stats_out.txt && exit 1)
