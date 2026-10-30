#!/bin/zsh
set -eu
cd "$(dirname "$0")/.."

if ! command -v shortcuts >/dev/null 2>&1; then
  echo 'ERROR: Apple Shortcuts CLI is missing. Use a Mac with the Shortcuts app.' >&2
  exit 1
fi

# Python 3.14 from Homebrew can fail to import plistlib because pyexpat
# tries to load an incompatible system libexpat. This is an environment error,
# not a SnapReply error. Prefer the built-in macOS Python if it works.
PYTHON=""
for candidate in "${SNAPREPLY_PYTHON:-}" /usr/bin/python3 \
    /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 \
    python3.13 python3.12 python3.11 python3.10 python3; do
  if [[ -n "$candidate" ]] && command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import plistlib, json, uuid, unittest' >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
  fi
done
if [[ -z "$PYTHON" ]]; then
  echo 'ERROR: No working Python 3 found. Try /usr/bin/python3; or install Python 3.12 with Homebrew.' >&2
  echo 'You can also use the iPhone-only setup in docs/iphone-setup.zh-CN.md.' >&2
  exit 1
fi

echo "Using Python: $PYTHON"
"$PYTHON" src/build_shortcut.py --output dist/SnapReply-unsigned.shortcut
"$PYTHON" -m unittest discover -s tests -v
"$PYTHON" scripts/scan_release.py dist/SnapReply-unsigned.shortcut

# Apple requires a signed-in iCloud account for shortcuts sign.
shortcuts sign --mode anyone --input dist/SnapReply-unsigned.shortcut --output dist/SnapReply.shortcut
echo 'Signed: dist/SnapReply.shortcut'
if [[ "${SNAPREPLY_NO_OPEN:-0}" != "1" ]]; then
  echo 'Opening Shortcuts.app to import the full workflow. Click Add Shortcut.'
  open -a Shortcuts "$PWD/dist/SnapReply.shortcut" || echo 'Open dist/SnapReply.shortcut manually (signing succeeded).'
fi
echo 'After importing, enable Shortcuts iCloud Sync on Mac and iPhone, or AirDrop the signed file.'
echo 'Configure your API Key privately on your device; never publish that configured copy.'
