# Telegram Firebase Manager delivery

Implemented on feature/telegram-firebase-manager, based on the unchanged OTP security fix d4f967c745b3a0a457f013d6b7295b01b65ae174. Source-preservation PR #1 and OTP PR #2 remain separate; this feature PR targets the OTP branch. No history rewrite, automatic merge, production deployment or Google resource creation occurred.

## Modules

- New backend modules: firebase_config.py, firebase_cloud.py, firebase_migration.py, firebase_manager_store.py, firebase_jobs.py, firebase_telegram.py, firebase_worker.py, firebase_gateway.py.
- Extended existing backend modules: firebase_pool.py, firebase_api.py, firebase_cli.py, telegram_bot.py, main.py. auth_api.py and registration/account modules are unchanged.
- Android: existing adapter/transport and Settings receive minimal customer-only Firebase integration; FirebaseSettings.jsx is new. Four tabs, styling/branding, extracted UI, keyboard repair and Keystore implementation remain.
- Tooling: bootstrap_firebase_profile.py, install_firebase_manager.py, requirements-firebase-manager.txt; real local Rules test/configuration; backend/Android operation tests; baseline-preserving audit updates and source manifests. All changed paths and hashes are in SOURCE_CHANGES.json and the PR diff.

The owner can use /firebase and the full commands in COMMANDS.md for guided Add/Create, paginated pool/assignment/request/audit/job views, verified assignment, decision confirmations and disable/enable/test operations. Commands use private linked-owner authorization and opaque single-use inline callbacks. Cloud work is persisted and retry-safe rather than blocking polling. Original bot commands, polling offsets, 403 handling and OTP transaction protections are preserved.

## What is operationally ready versus pending

The implementation and isolated tests are complete for the documented workflows. Creation, registration and validation call official Google Cloud interfaces; they do not fabricate a successful database. A provider must verify identity, billing/permissions/role/policy/quota/cap, connectivity, exact deny-all Rules, client denial and (for new/unassigned resources) emptiness before a database is assignable. Nonempty/duplicate legacy identities require private ownership review and are not silently reused. One customer retains one dedicated instance through expiry/renewal; no automatic reassignment/deletion exists.

No Google credentials or real project/billing settings were supplied, so **live Cloud creation/registration and production readiness have not been verified**. The manager is installed disabled unless explicitly enabled after bootstrap; per-profile provisioning is separately disabled by default. Required operator inputs are the actual project ID/number/region, dedicated service-account/workload identity, exact custom role and reviewed inherited IAM/policy fingerprint, Blaze billing/quota/resource cap, private credential delivery when needed, and verified service configuration. See BOOTSTRAP.md for exact seven permissions and copy-paste setup; no private keys enter Telegram or Android.

Architecture is backend-mediated with direct client denial. The customer receives only their approved database URL; it confers no read/write permission. The narrow optional preferences gateway derives the database from the authenticated account, rechecks isolation, and accepts only fixed theme/locale fields. It is off by default; no device collection or monitoring integration is activated. Authorized devices use separate existing password/Telegram OTP sessions for their account; no per-device collector/enrollment feature is invented. The full independent original website and child application are still unavailable and are not claimed recovered.

Tests: Python 89 passed; Android JS 51 passed/1 existing skip; browser 12 passed; real local Rules denial 6 passed; frontend/sync and native application build/unit/lint passed (0 lint errors/16 warnings). Read TEST_RESULTS.md for scope, warnings and unavailable live/device checks. Source/secret review found no actual credentials; only the existing three provenance-digest scanner false positives remain, without suppression.

## Deployment handoff

DEPLOYMENT.md contains complete check/apply/enable/rollback commands for the supplied Ubuntu paths and two service units. The prepared installer checks actual source/configuration, makes protected source/SQLite/venv backups, prefetches SDK wheels, applies additive migration, restarts only necessary services and checks API plus successful bot poll heartbeat. Recovery restores code/dependencies/drop-ins but retains live customer data/additive schema and quarantines unverified allocator entries. Cloud resources are never automatically deleted on recovery. Tests exercise temporary-directory recovery only; no VPS command was executed.

Before acceptance: review/merge the stacked branches deliberately; run the installer check privately; bootstrap the authorized Cloud identity/project/billing/Rules; explicitly enable the manager and creation flags; use dedicated test customers to create/verify separate instances, approve links, test direct/client and gateway cross-tenant denial, expire/renew one customer, and verify the bot/Android flow on an actual device. Only then expand from 10–20 initial resources toward 50+ under the approved cap and budget.
