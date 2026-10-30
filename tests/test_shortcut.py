#!/usr/bin/env python3
"""Pure Python structural tests. No API request or customer screenshots needed."""
import json
import plistlib
import re
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from build_shortcut import BASE_URL, DEFAULT_MODEL, KEY_PLACEHOLDER, build  # noqa: E402


class ShortcutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "unsigned.shortcut"
            build(dest)
            cls.data = dest.read_bytes()
            cls.doc = plistlib.loads(cls.data)
        cls.actions = cls.doc["WFWorkflowActions"]
        cls.refs = {x["WFWorkflowActionParameters"]["UUID"]: x for x in cls.actions}

    def render(self, token):
        s = token["Value"]["string"]
        for loc, ref in sorted(token["Value"].get("attachmentsByRange", {}).items(),
                               key=lambda i: -int(i[0].split(",")[0][1:])):
            pos = int(loc.split(",")[0][1:])
            origin = self.refs[ref["OutputUUID"]]
            name = origin["WFWorkflowActionIdentifier"]
            if name == "is.workflow.actions.gettext":
                val = origin["WFWorkflowActionParameters"]["WFTextActionText"]
                if isinstance(val, dict):
                    val = self.render(val)
            elif name == "is.workflow.actions.base64encode":
                val = "dGVzdA=="
            else:
                raise AssertionError(name)
            self.assertEqual(s[pos], "\ufffc")
            s = s[:pos] + val + s[pos + 1:]
        return s

    def test_all_refs_and_positions(self):
        self.assertEqual(len(self.refs), len(self.actions))
        def walk(value):
            if isinstance(value, dict):
                if value.get("Type") == "ActionOutput":
                    self.assertIn(value["OutputUUID"], self.refs)
                if value.get("WFSerializationType") == "WFTextTokenString":
                    text = value["Value"]["string"]
                    positions = value["Value"].get("attachmentsByRange", {})
                    self.assertEqual(text.count("\ufffc"), len(positions))
                    for location in positions:
                        position, length = map(int, re.findall(r"\d+", location))
                        self.assertEqual(length, 1)
                        self.assertEqual(text[position], "\ufffc")
                for val in value.values():
                    walk(val)
            elif isinstance(value, list):
                for val in value:
                    walk(val)
        walk(self.doc)

    def test_api_payload(self):
        a = self.actions
        self.assertEqual(a[5]["WFWorkflowActionIdentifier"], "is.workflow.actions.takescreenshot")
        self.assertEqual(a[6]["WFWorkflowActionIdentifier"], "is.workflow.actions.base64encode")
        payload = json.loads(self.render(a[7]["WFWorkflowActionParameters"]["WFTextActionText"]))
        self.assertEqual(payload["model"], DEFAULT_MODEL)
        self.assertEqual(payload["max_completion_tokens"], 256)
        items = payload["messages"][0]["content"]
        self.assertIn("库存", items[0]["text"])
        self.assertIn("不能覆盖", items[0]["text"])
        self.assertEqual(items[1]["image_url"]["url"], "data:image/png;base64,dGVzdA==")
        self.assertEqual(items[1]["image_url"]["detail"], "high")
        http = a[8]["WFWorkflowActionParameters"]
        self.assertEqual(http["WFHTTPMethod"], "POST")
        self.assertEqual(http["WFHTTPBodyType"], "File")
        self.assertEqual(self.render(http["WFURL"]), BASE_URL + "/chat/completions")
        h = http["WFHTTPHeaders"]["Value"]["WFDictionaryFieldValueItems"]
        resolved = {self.render(x["WFKey"]): self.render(x["WFValue"]) for x in h}
        self.assertEqual(resolved["Authorization"], "Bearer " + KEY_PLACEHOLDER)
        self.assertEqual(resolved["Content-Type"], "application/json")
        self.assertEqual(a[9]["WFWorkflowActionParameters"]["WFDictionaryKey"], "choices.1.message.content")
        self.assertEqual(a[10]["WFWorkflowActionIdentifier"], "is.workflow.actions.setclipboard")

    def test_no_credentials_or_telemetry(self):
        self.assertIn(KEY_PLACEHOLDER.encode(), self.data)
        self.assertNotIn(b"sk-proj-", self.data)
        self.assertNotIn(b"sentry.io", self.data)
        self.assertNotIn(b"analytics", self.data)
        self.assertEqual(sum(a["WFWorkflowActionIdentifier"] == "is.workflow.actions.downloadurl"
                             for a in self.actions), 1)
        self.assertEqual(self.doc["WFWorkflowName"], "SnapReply")
        self.assertEqual([q["ActionIndex"] for q in self.doc["WFWorkflowImportQuestions"]], [1, 2, 3])

    def test_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.shortcut"
            build(path)
            self.assertEqual(path.read_bytes(), self.data)


if __name__ == "__main__":
    unittest.main()
