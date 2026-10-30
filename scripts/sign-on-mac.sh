#!/bin/zsh
set -eu
cd "$(dirname "$0")/.."
if ! command -v shortcuts >/dev/null 2>&1; then
  echo 'Apple Shortcuts CLI required. Run this on macOS 12 or later.' >&2
  exit 1
fi
python3 src/build_shortcut.py --output dist/SnapReply-unsigned.shortcut
python3 -m unittest discover -s tests -v
python3 scripts/scan_release.py dist/SnapReply-unsigned.shortcut
shortcuts sign --mode anyone --input dist/SnapReply-unsigned.shortcut --output dist/SnapReply.shortcut
echo 'Ready: dist/SnapReply.shortcut — import on iPhone or Mac. Set private API key on device.'
