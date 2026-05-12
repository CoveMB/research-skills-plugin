#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
python3 scripts/test_check_book_artifact_contract.py
python3 scripts/test_plugin_structure.py
