# OTP security patch validation

Executed against the source-import baseline and this patch, with temporary SQLite storage and synthetic secrets only:

- **Before:** `pytest tests/test_backend.py::test_three_wrong_attempts_are_persisted --runxfail` reproduced the failure (zero persisted attempts after three wrong codes).
- **After:** `pytest tests/test_backend.py tests/test_otp_security.py tests/test_otp_deployment.py -q`: **31 passed**, no expected failures or skipped Python cases. One existing Starlette/httpx deprecation warning remains. Includes original backend tests, the converted regression, lockout/expiry/replay/concurrency/commit-failure checks, full FastAPI/Android wire-contract flow and ten isolated deployment-orchestration tests.
- **Android compatibility:** existing `npm test` suite: **48 passed, 0 failed, 1 skipped** (unavailable original website attachments). Android source and UI were not modified. The HTTP contract test uses real FastAPI routing, an intercepted Telegram client and temporary accounts; it does not call the production API.
- Exact baseline file and all other original backend module checksums remain verified against the unmodified preservation manifest; the patch has its own checksum in OTP_SOURCE_CHECKSUMS.json. The indexed-source audit explicitly checks both versions for this authorized change.
- Diff whitespace, syntax, scoped-change and secret scans were reviewed before publishing. Gitleaks default rules report only the same three provenance SHA-256 false positives from the import baseline; no suppression rules are enabled. No secrets were found in the reviewed patch.

No production account data, passwords, bot credentials, OTPs, challenges or sessions were logged or committed. Test transport/health/restart callbacks are synthetic. No actual VPS preflight, backup, deployment, service restart, rollback, live OTP delivery, Android device test or PR merge was performed. Deployment unit/interpreter/loopback endpoint must be verified by the operator before an approved deployment. Existing historical preservation documents retain their original pre-fix findings and checksums.

Private local evidence is under `/workspace/private-source-review/otp-fix/`; public reports contain summaries only. No need to repeat the unchanged Android Gradle/UI validation for this backend-only patch; Android integration checks were executed as above.
