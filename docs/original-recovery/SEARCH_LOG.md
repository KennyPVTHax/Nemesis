# Incremental source-recovery search

Base: PR #4 head dcef2004dcb8229fd48e3b8d4edd0892e4db61a5, fetched and inspected. That PR and prior branches remain unchanged.

New evidence checked: every file in `/tmp/codex-remote-attachments/01a18514-b0c2-7636-9812-3cf6d0c9b069/1a12b4a7-7838-44a8-b004-85c8245e187d/`: `1-surgeignore`, `2-200.html`, `3-CNAME`, `4-index.html`, `5-index.html.bak`. Original bytes, byte counts, CRLF/LF-normalized hashes and historical hashes were compared. Only the ignore file, CNAME and backup match the historical checksums. The primary and fallback match each other but not history; no guessed newline/content replacement is labeled authentic.

Reused completed evidence: PR #4's six source archives, two Step22 directories, working Android checkpoint, 216 reachable Git blobs, and file/variant census under `docs/original-feature-code-audit/`. No exhausted archive scan was repeated. New HTML was parsed statically; no source script was run. Current GitHub PR/branch metadata was fetched to establish ancestry, not to rewrite existing history.

No new hosting/deployment/source-map export or child-device source was supplied. These locations were not guessed or scraped. No VPS, customer database, live Firebase, Telegram bot or unrelated server was accessed. Remaining exact primary/fallback identity can only be authenticated if the owner supplies the 925799-byte historical artifact matching the recorded digest. The authenticated original backup already restores its own historical executable logic for private review.
