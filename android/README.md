# NEMESIS Android — 0.3.0

This updates the existing React/Vite/Capacitor Android project with the approved UI styling, a new owner-authorized crimson N logo, and enabled production authentication at https://nemesispanel.shop. The original extracted dashboard/APK markup, four tabs and prior keyboard repair remain.

The exact response schema was supplied by the owner on 2026-10-30 and is mapped in src/auth/api-contract.mjs. Login → Telegram OTP → /auth/me → dashboard uses real production endpoints, with no development account or mock fallback. Account expiry (nullable UNIX seconds) is separate from token lifetime. Android uses native HTTPS for these fixed routes because server WebView CORS preflight returns 405; TLS verification and redirect rejection remain enabled.

Native sessions use AES-GCM and Android Keystore with backups/logging disabled. The saved bearer is revalidated against /auth/me at startup. There is no plaintext/browser storage fallback on Android. Passwords, codes and challenges are not saved. Logout erases the saved key/envelope and requests server revocation.

Monitoring/Firebase/APK-building integrations remain disconnected and outside this build's scope. The original controls stay visible; unavailable account-security operations explain their missing endpoints. No website, deployed backend, database or production infrastructure was changed.

The frontend/JS/browser tests and app Gradle build/lint/instrumentation assembly passed. Real customer login, Telegram delivery, Keystore and keyboard behavior still require the owner's physical-device validation. The automated auth responses are isolated synthetic tests using the confirmed field names; they are never an APK fallback.

Build with Node 24, JDK 21 and Android SDK 35 / Build Tools 35.0.0:

```sh
npm ci
npm run build
npm test
npx cap sync android
cd android
./gradlew --no-daemon :app:assembleDebug :app:testDebugUnitTest :app:lintDebug :app:assembleDebugAndroidTest
```

Use explicit :app: tasks; the generated Cordova library's own instrumentation assembly has an unrelated Kotlin duplicate-class conflict. Application assembly and its test APK pass. No vendor versions were changed.

From this directory, serve dist with npx vite preview --host 127.0.0.1 --port 4179, then run npm run test:ui in another terminal. Chromium is expected at /usr/bin/chromium. The synthetic browser harness is built outside dist and never packaged. Run node scripts/preview-board.mjs after capture to reproduce the contact sheet. Native branding conversion: node scripts/apply-branding.mjs. Do not use the historical export-logo.mjs or regenerate the original website UI.

See ../docs/ui-refresh/DELIVERY_REPORT.md, API_INTEGRATION.md, BUILD_AND_INSTALL.md, TEST_RESULTS.md and PENDING_APPROVALS.md. Source archives keep android-app and docs as sibling directories for tests. The old website attachments are not currently mounted; their direct rehash test is explicitly skipped. Extracted original UI/CSS/icons/provenance hashes still match, and prior APK/source archives are preserved.
