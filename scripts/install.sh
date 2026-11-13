#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-${HOME}/.gemini/config/skills}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "${TARGET_DIR}"

for skill in informs-writing informs-zh-review; do
  rm -rf "${TARGET_DIR}/${skill}"
  cp -r "${REPO_ROOT}/${skill}" "${TARGET_DIR}/${skill}"
  find "${TARGET_DIR}/${skill}" -type d -name "__pycache__" -exec rm -rf {} +
  echo "Installed ${skill} -> ${TARGET_DIR}/${skill}"
done
