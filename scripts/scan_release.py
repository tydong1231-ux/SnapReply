#!/usr/bin/env python3
"""Basic safety gate for publicly released placeholder-only shortcut templates."""
import plistlib
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/SnapReply-unsigned.shortcut")
workflow = plistlib.loads(path.read_bytes())
actions = workflow["WFWorkflowActions"]
assert actions[2]["WFWorkflowActionParameters"]["WFTextActionText"] == "PASTE_YOUR_API_KEY_HERE"
assert actions[3]["WFWorkflowActionParameters"]["WFTextActionText"] == "gpt-5.4-mini"
assert sum(a["WFWorkflowActionIdentifier"] == "is.workflow.actions.downloadurl" for a in actions) == 1
assert actions[-1]["WFWorkflowActionIdentifier"] == "is.workflow.actions.setclipboard"
for pattern in (rb"sk-(?:proj-)?[A-Za-z0-9_-]{24,}", rb"ghp_[A-Za-z0-9]{30,}", rb"AKIA[A-Z0-9]{16}"):
    if re.search(pattern, path.read_bytes()):
        raise SystemExit("Potential secret in release binary. Aborting.")
print("PASS: public build contains placeholder key and exactly one model API call")
