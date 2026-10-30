# SnapReply

**One tap → understand the visible chat → draft a reply → clipboard.**

An independently implemented, open-source Apple Shortcuts workflow for iPhone. No custom keyboard, app developer account, Xcode project or App Store submission required. Made for Chinese-language customer replies in WeChat; also works with other visible conversations.

**Status:** MVP template and static tests completed. Apple signing on GitHub-hosted macOS and real iPhone / iOS 26.2 usage still require validation. This is not an app that reads WeChat's internal chat history.

[简体中文说明](README.zh-CN.md) · [Security](SECURITY.md)

## User experience

1. Open a customer conversation in WeChat.
2. Launch **SnapReply** using iPhone Back Tap, Action Button, or the Shortcuts app.
3. The shortcut captures the **current screen**, sends it to your configured vision-enabled API, and copies **one** draft to the clipboard.
4. Tap the clipboard candidate in your keyboard (or long-press **Paste**), check the text, then send yourself.

No continuous screen recording, auto-sending, remote repository updates, or third-party telemetry. Only **one API request per invocation**. The shortcut cannot see messages that are off-screen.

## Install with GitHub Actions (easiest)

1. Open this repository's **Actions → Build and sign SnapReply template**. Select the newest **successful** run (or **Run workflow**).
2. Download the **SnapReply-iPhone-Shortcut** artifact. Unzip it to get `SnapReply.shortcut`.
3. Open that file on your iPhone and import into Apple's **Shortcuts** app. If import questions are displayed, enter:
   - **Base URL**: `https://api.openai.com/v1` (no trailing `/`)
   - **API Key**: your **private** API key, entered on-device only
   - **Model**: `gpt-5.4-mini` (or a vision-capable Chat Completions-compatible model)
4. If import prompts did not appear, edit the **first three Text actions** in the imported shortcut and enter those values there.
5. Test with a **fake, non-sensitive** conversation first. On iPhone: **Settings → Accessibility → Touch → Back Tap → Triple Tap → SnapReply**. Optionally assign the Action Button.

If signing fails in GitHub Actions, use the local macOS instructions below. A raw/unsigned file cannot be imported directly on modern iOS. An Actions artifact is **not** a public iCloud shortcut link.

## Install using your Mac

Requires macOS with the built-in Apple Shortcuts CLI, Python 3, and an internet connection for Apple signing. No paid Apple Developer account is needed.

```sh
git clone https://github.com/tydong1231-ux/SnapReply.git
cd SnapReply
zsh scripts/sign-on-mac.sh
```

The output is `dist/SnapReply.shortcut`. AirDrop it to your iPhone or open it on your Mac to add it to Shortcuts and sync via your Apple Account.

## Settings and API compatibility

| Setting | Default | Purpose |
| --- | --- | --- |
| Base URL | `https://api.openai.com/v1` | HTTPS endpoint root, **without** `/chat/completions` |
| API Key | Placeholder | Never committed or pre-bundled |
| Model | `gpt-5.4-mini` | Economical vision model |

SnapReply calls `POST {Base URL}/chat/completions` with `Authorization: Bearer <key>`, a screenshot data URL, and `max_completion_tokens=256`. The provider **must support both images and the Chat Completions request/response format**. Some compatible providers require modifying the payload; changing only the model name may not work.

The request uses a File-body payload built from a JSON Text action. If your device rejects it, please open an issue with iOS version, *redacted* action screenshot, and a generic error message (never real screenshots or keys). See [source](src/build_shortcut.py) and [tests](tests/test_shortcut.py).

## Privacy & important constraints

- **Your entire visible screenshot leaves the phone.** Only run on conversations you are comfortable sharing with the configured AI provider. Avoid addresses, payment information, private IDs, and health details.
- **Your secret is saved as editable text inside your personal shortcut.** Anyone with an exported configured shortcut can read it. Never upload or share that copy. Use a separate API project/key with a low spending limit.
- OpenAI API requests are not used to train models by default, but retention/monitoring policies apply. Other API providers have their own rules.
- The generated reply is placed on the **system clipboard** and may be read by other apps with appropriate access. Review before sending.
- No claim of complete end-to-end security, automatic reply correctness, or tested compatibility with every iOS version.

Read [SECURITY.md](SECURITY.md) before using it with real customer conversations.

## Contribute / licensing

Source is under the repository's existing **Apache License 2.0**. Inspired by the one-tap screenshot-to-reply idea from [rishiv7/relay](https://github.com/rishiv7/relay), whose repository had no explicit license as checked in October 2026. **No code or signed shortcut binary is copied from it.**

Run tests without external dependencies:

```sh
python3 src/build_shortcut.py
python3 -m unittest discover -s tests -v
python3 scripts/scan_release.py dist/SnapReply-unsigned.shortcut
```

For pricing and model support, see [OpenAI GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini). Using an API key incurs separate API costs; a ChatGPT subscription is not an API subscription.
