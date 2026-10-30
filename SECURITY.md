# Security & privacy

SnapReply is a **user-triggered** iOS Shortcut, not a background monitor.

## Data flow

1. Only after you trigger SnapReply, it captures the visible screen.
2. It sends the screenshot and reply prompt over HTTPS to the **Base URL you configured**.
3. The configured server receives **both your API credential and the image**.
4. It copies the generated text to your device clipboard for human review. It never sends the message automatically.

There is no developer-run SnapReply server, remote logging, background recording, hidden analytics, or access to the WeChat message database in this repository's template.

## Risks to understand

- Screenshots include the entire visible screen. Avoid personal addresses, ID information, banking records, payment screenshots, and private conversations.
- An API key stored in a Shortcuts **Text** action is **plain text**. Your Apple Account's Shortcuts sync may copy it to your other devices. A shared/exported shortcut can expose it. Prefer separate limited-purpose keys and billing alerts.
- An untrusted compatible Base URL can exfiltrate **both the API key and screenshot**. Prefer the OpenAI official HTTPS URL or a self-controlled HTTPS server.
- OpenAI API data is not used for training by default, but policy-dependent retention and abuse monitoring can apply. Other API providers' policies vary.
- iOS clipboard content can be available to other apps. The shortcut doesn't automatically clear it, so avoid sensitive information in generated replies.
- Conversation text in a screenshot can try to instruct the model. The prompt treats it as **untrusted data**, but no prompt is foolproof. Always review the generated message.
- This is **not** an independently audited security product. Static checks do not verify network behavior on a real phone.

## Public source and releases

- The published template contains `PASTE_YOUR_API_KEY_HERE`, **never a real key**.
- `scripts/scan_release.py` checks the generated template and blocks common credential patterns.
- GitHub Actions signs and uploads a **placeholder-only** artifact. No GitHub Secrets or API key are required.
- Do not commit signed shortcuts exported from your phone after configuration.
- Do not post real customer screenshots, API keys, or logs with headers in public GitHub issues.

If a configured key ever enters Git history, **revoke it immediately** at your provider and generate a new one. Deleting the latest commit does not erase historic leaked keys.
