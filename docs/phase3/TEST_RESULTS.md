# Phase 3 verification

| Executed check | Result |
|---|---|
| Python backend/security/operations suite | 89 passed, 0 failed; existing Starlette/httpx deprecation warning |
| Android JavaScript suite | 51 passed, 0 failed, 1 skipped (original website inputs unavailable) |
| Browser regression scenarios | 12 passed; no runtime errors |
| Real local RTDB emulator Rules clients | 6 denial checks + 3 authentication controls passed, 0 failed: anonymous and two Firebase user identities |
| Frontend build / Capacitor sync | Passed; original CSS minifier warnings retained |
| Android :app:assembleDebug / testDebugUnitTest / lintDebug | Passed; lint 0 errors / 16 warnings; inherited JVM scaffold only |
| Source preservation and checksums | Original manifests and OTP fixed verifier unchanged; authorized deltas and copied baselines separately recorded |
| Indexed-source secret audit and Gitleaks | No real secrets found; only the three previously reviewed SHA-256 false positives in the preservation manifest |

Python cases include private owner authorization/customer rejection, forwarded/callback replay/message binding, concurrent confirmation, approval revisions, stale validation results, changed assignments at disable confirmation, invalid/duplicate URLs, real official REST request shapes with mocked responses, IAM/project identity/broad-role rejection, billing/quota/cap failures, timeout-after-create recovery, bounded interrupted jobs, safe legacy migration, 50 distinct concurrent customer assignments, expiry/renewal reservation, disable exclusion, request/decision outbox, own-instance gateway scoping, original bot commands/403 recovery, and all existing OTP transaction/three-attempt/concurrency tests. Existing registration and API tests continue to run against temporary SQLite accounts. Deployment tests use temporary source/venv/database directories and injected service callbacks; they verify idempotence, source drift refusal, rollback recovery, retaining newer registrations and quarantining unverified records before old-code recovery.

The initial SDK-based emulator read did not complete, so the final Rules test uses actual bounded REST client requests with Firebase mock ID tokens through the emulator's client `auth` parameter. The emulator owner token is used only to install the test Rules. A Bearer-token probe was rejected as unsuitable for client Rules evidence; all six final read/write assertions use anonymous or mock-user client authentication and pass. Three positive/negative authentication controls first prove the emulator recognizes the mock user identity (A is allowed under an A-only test policy while B/anonymous are denied), then restore the actual deny-all policy before the six isolation assertions. No Admin SDK read is counted as tenant-isolation proof. The emulator uses a demo project and real local emulator process; no Cloud Firebase project is contacted.

Android regressions exercise existing login/OTP, four tabs, original dashboard controls/modal, themes, keyboard viewport simulation, account refresh and logout. New customer calls use bearer headers and exact endpoint methods. Approval-denied 403 / Firebase 503 preserves a valid login; 401 still invalidates an expired session. The capability guard prevents calling old unverified Firebase allocation until the updated backend advertises manager support. No Android management controls or admin credentials were added.

No actual VPS, real Telegram polling/delivery, live Google Cloud provisioning/IAM/billing/quota, native device/Keystore/IME, full unavailable original website or production Firebase isolation test was performed. Actual cloud/configuration checks remain mandatory before activation. Local fixtures and mocked providers are tests, never production fallback implementations. No release APK was published; the debug build is a local validation artifact. Raw logs and scanner reports remain private under /workspace/private-source-review/firebase-manager.

## Reproduce

- Python: isolated venv with backend requirements and deployment/requirements-firebase-manager.txt plus pytest; run `python -m pytest tests -q`.
- Android: from android/, `npm ci`, `npm run build`, `npm test`, `npx cap sync android`; then native explicit application Gradle tasks with JDK21/SDK35.
- Browser: serve built dist on 127.0.0.1:4179, then `npm run test:ui` from android/.
- Rules: `npm ci` in firebase-security/, then installed Firebase CLI `firebase emulators:exec --project demo-nemesis --config firebase.json --only database 'npm test'` with Java available. Node24, Java21 and RTDB emulator 4.11.2 were used here. Firebase CLI bootstrap may need its public emulator download on a new machine.
- Source: `python tests/source_audit.py` against the index, plus Gitleaks default file/history scans; review findings rather than suppressing arbitrary paths. The original raw website attachment test remains explicitly skipped; extracted UI hashes are checked.
