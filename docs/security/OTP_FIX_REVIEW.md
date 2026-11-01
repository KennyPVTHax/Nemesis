# OTP failed-attempt transaction fix

Baseline: source-import commit `8e5bc36f5bf88e6fdf9fd02dc1406d77befd8ed1`. The imported `backend/auth_api.py` is retained byte-for-byte at `legacy/backend-baseline/auth_api.py`; original export and import manifests are unchanged. `OTP_SOURCE_CHECKSUMS.json` records the original and patched hashes separately. The other nine exported modules and all Android/website sources are unchanged.

## Root cause and correction

`auth_api.verify()` incremented `attempts` and then raised `HTTPException` from inside `with connect() as db`. Python's SQLite connection context rolls back on that exception, including the increment. The original regression run with `--runxfail` failed: three wrong codes left attempts at zero.

The fixed implementation records a wrong code in a normally exiting transaction, then raises the same generic 401 **after commit**. If commit fails, an operational error propagates; no authentication rejection falsely claims a counted attempt. A challenge already at three failures is denied, including a correct code. Counter values cannot exceed three through verification. Expired/unknown/ineligible challenges retain generic denial behavior; malformed requests retain 422 validation.

`BEGIN IMMEDIATE` is preserved: each independent SQLite connection obtains the writer lock before reading challenge state, checking the counter, and updating it. This serialization works across service workers sharing this same SQLite database. Successful challenge deletion and session insertion remain one atomic transaction. Racing correct submissions yield one successful session; wrong/correct races follow lock order, with success possible only if it commits before the third failure. Session-insert failure rolls back challenge consumption. Time is now sampled after obtaining the writer lock, preventing queued requests from verifying against a stale pre-wait expiration timestamp.

No SQL schema, password check, Telegram delivery/registration, Firebase allocation, Android interface, bearer representation, or endpoint contract was changed. Login still creates a 300-second challenge; verification still returns `access_token`, `token_type: bearer`, `expires_in: 28800`. Actual customer session expiration remains bounded by account expiration. Owner null account expiry, logout and profile authorization are unchanged. This fix does not introduce a global single-session-per-user restriction: only duplicate consumption of the same challenge is prevented.

## Verification

The previously expected-failure test is now a normal passing test. Additional tests use temporary SQLite databases and random synthetic values only:

- One wrong code is visible from a fresh connection; the next correct code can succeed.
- Three wrong codes persist; correct and incorrect codes after lockout are denied without new sessions.
- Expired challenges, the exact expiry boundary, and expiration during an actual blocked writer-lock wait are rejected.
- Eight racing wrong submissions stop at three failures; eight racing correct submissions produce exactly one session; mixed races at the last attempt obey serialization.
- Inactive/expired customers cannot obtain a session, replay fails, and session-insert failure rolls back consumption.
- Commit failure cannot return an authentication denial without persistence.
- Full FastAPI password login → intercepted Telegram delivery → verify → profile → logout matches the existing Android wire schema, including 300-second OTP lifetime and customer session clipping. No external delivery occurs.
- Deployment orchestration tests cover backup/permissions, idempotent reapply/rollback, preflight and health failures, automatic rollback, drift/tamper/symlink refusals, and candidate change during preflight. They inject service/health callbacks and use temporary paths, never the VPS.

Run `python -m pytest tests/test_backend.py tests/test_otp_security.py tests/test_otp_deployment.py` in an isolated environment with the existing reviewed dependencies plus pytest. Android compatibility is also checked with the existing `npm test` suite from `android/`. No Android/UI edits or APK rebuild are required for this backend-only fix. The original source audit now validates the preserved baseline for this one authorized patch plus its distinct current hash, rather than overwriting the import manifest.

Deployment tooling and instructions are in `deployment/deploy_otp_fix.py` and `OTP_VPS_DEPLOYMENT.md`. They are prepared only. No VPS command, restart, deployment or PR merge was executed.
