# Backend source review — 2026-11-02

## Evidence / scope
User-provided `NEMESIS_BACKEND_SOURCE_REVIEW.tar.gz` inspected. Archive SHA-256:
`5a239b8470cee190ff48cde7989b044db7e9f4de3cf5bd4d98cb9a7d018e1e6a`.

**Ten Python files** were extracted in a local workspace; 10/10 matched the archive's SHA256SUMS.txt; all passed Python syntax parsing. This is a **source-only export** from `/opt/nemesis/backend`. It excludes the Android app, original website, service unit files, Nginx configuration, runtime database and credentials. It does **not** prove the entire running project is backed up.

## Credentials review
Automated checks found no inlined Telegram bot-token patterns, Google API key patterns, GitHub PAT patterns, PEM private keys, AWS access-key IDs, or obvious literal secret assignments. Public URLs, including the production backend address, are present. Regex-based scanning is **not exhaustive**; manual review and a second scanner are recommended before any public release. Do not import `/etc/nemesis`, `/opt/nemesis/data`, production databases, logs or private key material.

## Modules present
- `account_store.py`: account schema, Argon2id owner.
- `auth_api.py`: password + Telegram OTP, bearer sessions.
- `telegram_bot.py`, `telegram_link.py`: Telegram commands, owner linking.
- `registration_store.py`, `registration_api.py`: redeem keys, registration, setup form.
- `firebase_pool.py`, `firebase_api.py`, `firebase_cli.py`: allocation inventory, owner-approved link workflow.
- `main.py`: FastAPI route inclusion.

## Known implementation/verification gaps
- Source export contains no Android or website files; these must be supplied and compared to originals.
- Firebase pool is *inventory/allocation* logic, not evidence of connectivity, Rules, or production-grade isolation; service credentials and actual Firebase projects aren't included.
- Telegram `/start` help text still says registration commands will be added, although the bot code implements them.
- Verify renewal, account expiry, repeated OTP attempts, audit/error handling and customer-level authorization with automated tests; no test suite was included.
- Preserving inactive monitoring features requires the **actual original code**; avoid writing imagined placeholders as if already preserved.

## Import status
This review branch contains preservation documentation and a verified manifest. The backend files must be imported from the validated export without editing; only then should their status be marked "source committed". No production VPS files have been changed by this review.
