# Phase 3 feature status

| Area | Source | Implementation / verification | Activation requirement |
|---|---|---|---|
| OTP/login/registration | auth_api.py, registration_*.py | Fixed verifier preserved byte-for-byte; existing regressions retained | Existing production behavior, no deploy performed |
| Owner inline manager | firebase_telegram.py, firebase_manager_store.py, telegram_bot.py | Implemented; private linked-owner, nonce/message binding, revision/result confirmation checks | Manager flag and active linked NemesisOwner |
| Existing-instance wizard | firebase_jobs.py, firebase_cloud.py | Implemented with official management identity, exact Rules and unprivileged-denial verification | Authorized alias and real verified instance |
| Automatic creation | firebase_cloud.py, firebase_jobs.py | Official API integration, persistent retry/idempotency/billing/cap/IAM checks; mocked tests | Disabled until credential/IAM/Blaze/quota bootstrap; no live creation verified |
| Dedicated allocation | firebase_pool.py, firebase_migration.py | Transactional, unique ledger, 50-customer isolated test; renewal/expiry reserve same instance | Verified free capacity; imported instances require validation |
| Link approval | firebase_api.py, firebase_worker.py | Existing routes preserved; durable notifications and single-revision decisions | Verified assignment and owner approval |
| Rules/client isolation | firebase-security/, firebase_gateway.py | Real local emulator denial for anonymous and two Firebase user identities; gateway tenant-scope test | Actual per-instance live checks and private IAM inheritance review still needed |
| Lifecycle/diagnostics | manager overlay/jobs/audit/outbox | Disabled/error resources never automatically recycled or deleted | Explicit verification/enable for recovery |
| Android customer Settings | FirebaseSettings.jsx, API adapter/transport | Minimal status/request/approved-link addition; backend capability guard; no admin functions | Updated backend manager capability enabled |
| Android layout/branding/Back/Keystore | Existing original files | Preserved; existing tests/build retained | Native device testing not performed here |
| Independent website/legacy | Preserved extracted UI and historical baselines | No redesign, collector or old monitoring activation; unavailable full original source remains unavailable | No change |
| VPS installer/rollback | install_firebase_manager.py | Prepared; temporary-file/dependency/service callback recovery tests | Operator approval; no production execution |

Original inventories/manifests remain historical evidence. SOURCE_CHANGES.json documents the authorized current changes without overwriting source-preservation checksums. Jobs/metadata are not proof of live Cloud resources unless the actual provider successfully validates them. No new APK is published or distributed by this PR; build output is local validation only.
