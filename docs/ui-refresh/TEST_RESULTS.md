Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# Validation — Android 0.3.0

| Check | Result |
|---|---|
| Frontend production build / Capacitor sync | Passed; inherited original-CSS minifier warnings remain |
| JavaScript tests | 49 total: 48 passed, 0 failed, 1 skipped |
| Browser integration | 12 scenarios passed, no runtime errors |
| `:app:assembleDebug` | Passed; updated APK exists and was inspected |
| `:app:testDebugUnitTest` | Passed; one inherited arithmetic scaffold only |
| `:app:lintDebug` | Passed: 0 errors, 16 warnings |
| `:app:assembleDebugAndroidTest` | Passed; instrumentation test APK compiled |
| Connected Android instrumentation | Not run: no attached device/emulator or `/dev/kvm` |
| APK assets, signature, configuration and credential scans | Passed |
| Existing extracted website UI/CSS/icons/provenance | All four hashes unchanged |
| Original five attachment rehash | Skipped: original files are not mounted |
| Previously delivered Step 22 APK/source/patch | All three existing checksums still match |

JavaScript coverage includes exact owner/customer response parsing, null account expiry, separate account/token lifetimes, active-status validation, OTP challenge flow, duplicate/replayed/cancelled operations, 401/403/422/429/503, no session before `/auth/me`, secure-storage adapter save/restore/erase/failure behavior, write/logout ordering, fixed HTTPS destinations, native cancellation and redirect handling, original UI preservation, branding densities and keyboard ownership. Native transport and storage calls are isolated test doubles in these tests; these are not claims that Android Keystore or real Telegram ran on this executor.

Browser tests exercise the real React app/adapter against routed synthetic responses using the exact supplied production field names. They confirm the shipped login is enabled, password visibility and clearing, a single accessible OTP field with six visual slots, four tabs, original SMS search modal/Back, verified account display, themes, logout and profile rejection. Compact 320px, 360px, 412px and landscape widths fit without horizontal page overflow. Keyboard checks reduce the browser viewport, scroll focused fields into view and dismiss focus; they do **not** reproduce Android/Gboard IME behavior.

The two new Keystore instrumentation cases cover encrypted round-trip/deletion and tamper rejection. They compiled with the application test APK but were not executed. The inherited context test also remains. Run them only against a dedicated debug install/test account because they clear that install's saved session.

The first broad Gradle invocation also selected generated Cordova-library instrumentation tasks and failed on that generated module's Kotlin 1.8.22 versus jdk7/jdk8 1.6.21 duplicate classes. The application APK and its instrumentation APK compiled. The final reproducible commands explicitly target the application's build, tests, lint and instrumentation assembly, and all passed. No vendor dependencies were silently upgraded. The failed broad attempt log is retained as `android-all-module-instrumentation-attempt.log`.

Lint warnings are inherited dependency-update suggestions, unused/template assets, launcher monochrome suggestions and legacy splash-density warnings, plus the deliberate synchronous SharedPreferences deletion on logout. None are lint errors. No original website CSS was rewritten to suppress its pre-existing parser warnings.

APK checks confirm valid ZIP/DEX, exact packaged web assets versus final `dist`, new monogram and Keystore classes, API-only CSP, HTTPS-only settings, no WebView debugging, disabled credential-bearing bridge logging, no global HTTP fetch interception, no shipped mock/fixture authentication and no bot-token/Firebase-key patterns. Exact comparison with the original website's embedded credentials could not run because those attachments are unavailable. No real customer credentials were embedded. The debug signature matches the Step 22 fallback; package/version are `com.nemesis.panel.dev`, 0.3.0 / code 3, min API 23, target/compile API 35.

Live read-only checks: health 200; unauthenticated profile 401; schema/docs/root 404; WebView-origin OPTIONS 405. These establish reachability and the native-transport requirement, not successful customer authentication. No live password/OTP/session/revocation or Firebase isolated-project test was performed. Firebase remains outside scope.

Evidence is under `/workspace/artifacts/ui-refresh`: build/test logs, browser-results.json, original-source comparisons, network checks, lint reports, APK verification, badging and signature details. Screenshots are Chromium renders. OTP/dashboard/account screenshots contain clearly isolated synthetic test responses; there are no real codes or customer monitoring records. Launcher previews are generated assets, not screenshots of an Android launcher.
