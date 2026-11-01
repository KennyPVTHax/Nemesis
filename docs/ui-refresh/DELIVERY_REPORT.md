Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# NEMESIS Android 0.3.0 — UI refresh and production authentication

The existing Android project has been updated in place. The approved visual proposal is applied, the owner-requested new crimson N logo replaces the awkward helmet crop, and the exact production customer/owner authentication contract is implemented. Login is enabled. No mock account, response-field guessing or original website/backend changes are included.

## Delivered artifacts

- APK: /workspace/artifacts/ui-refresh/nemesis-ui-refresh-auth-debug.apk
- Complete source: /workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip
- Current UI board: /workspace/artifacts/ui-refresh/NEMESIS-updated-ui.png
- New logo: /workspace/artifacts/ui-refresh/nemesis-mark.png
- Checksums and evidence: /workspace/artifacts/ui-refresh/SHA256SUMS and adjacent logs/JSON/reports
- Checkpoint before these changes: /workspace/checkpoints/step23-before-source.zip
- App source: /workspace/android-app
- Current documentation: /workspace/docs/ui-refresh

APK: 5,891,314 bytes; SHA-256 c57aed2807017888cb9bd01a3c8f1bf37ce11cc844d4c89dfc9f609ab6fff5ca. App ID com.nemesis.panel.dev, version 0.3.0 / code 3, min API 23, target/compile API 35. The debug signature matches the prior Step 22 APK. No installation, deployment or external publication was performed.

## Implemented

The approved compact brand/form styling, consistent four-tab icons, readable original dashboard controls and grouped settings are applied without replacing the original dashboard/APK components. Login has password visibility, loading/errors and the real production request fields. OTP uses one accessible six-digit input, preserves the actual challenge and supports the confirmed restart-login path. The server controls OTP delivery, expiry, attempt limits and rate limits.

Production authentication uses POST /auth/login, POST /auth/verify, GET /auth/me and POST /auth/logout at https://nemesispanel.shop. A validated active profile is required before opening the four tabs. Owner expires_at:null is accepted as no account expiry; customer UNIX expiry is separate from the eight-hour token duration. Android uses the built-in native HTTPS transport for the fixed routes because the server's WebView preflight returns 405. No TLS/certificate bypass, global fetch interception or server CORS modification was introduced.

Bearer sessions are encrypted using AES-256-GCM and a non-exportable Android Keystore key, with private ciphertext storage and backups/logging disabled. Tokens are saved after profile validation and checked with /auth/me on restore. Logout removes the key/envelope and requests revocation. Inactive/expired/rejected accounts cannot use a stored session. No passwords, codes, challenges, bot tokens or administrative secrets are embedded or persisted by the app.

The prior single-owner keyboard repair is retained, with normal form scrolling and no extra IME padding. Launcher/adaptive/splash references use the new logo. The original supplied logo remains unchanged as a retained asset.

## Preservation and limits

Exactly four tabs remain: APK Management, Monitoring, Future, Settings. All four extracted original JSX/CSS/icons/provenance files match their checkpoint hashes. Their filters, SMS modal, original controls and animation source are preserved. Current source changes are recorded in CHANGED_FILES.json.

Monitoring and APK/Firebase services remain disconnected as they were in the scoped Step 22 build. They were not silently newly disabled and are not claimed operational. No child-APK builder or monitoring collector was added. Account details/profile refresh/logout use actual authentication endpoints. Password change, history, session lists, Telegram linking and 2SV settings retain their sections but require additional confirmed endpoints. Future stays reserved.

The five original website attachments are not mounted in this execution, so direct rehash was explicitly skipped; their manifest and prior archives are retained. There were no original website edits or production-system changes. Existing Step 22 APK/source/patch checksum verification passed. The earlier unfinished backend-dev work is not used or packaged.

## Validation

Frontend build/sync, 48 JavaScript tests, 12 browser scenarios, application Gradle build/unit/lint and instrumentation assembly passed. One original-attachment test was skipped. App lint has 0 errors and 16 warnings. The inherited JVM arithmetic test is a toolchain check; the new Keystore instrumentation tests were compiled, not executed. APK ZIP/DEX/assets/signature/configuration and credential-pattern scans passed. Native storage and network calls were isolated test doubles in JavaScript coverage; no production mock exists in the package.

A broad all-module instrumentation assembly exposed an unrelated generated Cordova-library Kotlin conflict. The final explicit application tasks all passed; both logs are retained. See TEST_RESULTS.md.

The live health endpoint now returns 200 and unauthenticated profile returns 401. The owner reports prior successful production OTP tests and supplied verified source-derived response structures. This execution did not use a real password/OTP or independently complete live customer login/Telegram delivery/revocation. No physical Android device/emulator is available, so keyboard, Keystore, OS icon/splash and live login require device validation. This is a compiled debug build with the real backend integration enabled, not a claim of completed live-device end-to-end verification.

See API_INTEGRATION.md, BUILD_AND_INSTALL.md, KEYBOARD_AND_BRANDING.md, FEATURE_INTEGRATION_CHECKLIST.md and PENDING_APPROVALS.md for exact behavior, reproduction and remaining checks.
