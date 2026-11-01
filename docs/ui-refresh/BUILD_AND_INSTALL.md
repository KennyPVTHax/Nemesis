Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# Build and install — 0.3.0

Use Node 24 (tested), a full JDK 21, Android SDK platform 35, Build Tools 35.0.0 and platform-tools. Gradle wrapper is included. Set `JAVA_HOME` and `ANDROID_HOME` to your local installations. Unzip the source with `android-app/` and `docs/` as sibling folders so preservation tests can read the manifests.

```sh
cd android-app
npm ci
npm run build
npm test
npx cap sync android
cd android
./gradlew --no-daemon :app:assembleDebug :app:testDebugUnitTest :app:lintDebug :app:assembleDebugAndroidTest
```

Main APK: `android-app/android/app/build/outputs/apk/debug/app-debug.apk`. The separately compiled instrumentation APK is under `android/app/build/outputs/apk/androidTest/debug/`; it is not the customer application and was not executed here. Explicit `:app:` tasks avoid selecting generated dependency modules' own instrumentation assemblies.

Browser regression checks, from `android-app/`, use two terminals:

```sh
npx vite preview --host 127.0.0.1 --port 4179 --strictPort
```

```sh
npm run test:ui
node scripts/preview-board.mjs
```

Chromium is expected at `/usr/bin/chromium` for browser/asset scripts. Tests build a separate non-shipped harness under artifacts. `ARTIFACT_DIR` and `APP_URL` can select alternate local output/preview locations. This does not change the production API origin. Regenerate native branding with `node scripts/apply-branding.mjs`; the original generated PNG is kept in `public/nemesis-mark.png`. Do not run the historical `export-logo.mjs`.

In this managed executor, Java used the normal configured proxy and system CA trust for dependency downloads. These are build-environment settings, not embedded APK settings:

```sh
export JAVA_HOME=/workspace/tools/jdk-21
export ANDROID_HOME=/workspace/tools/android-sdk
export JAVA_TOOL_OPTIONS='-Dhttps.proxyHost=proxy -Dhttps.proxyPort=8080 -Dhttp.proxyHost=proxy -Dhttp.proxyPort=8080 -Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts'
```

Install the delivered APK on the owner's device:

```sh
adb install -r nemesis-ui-refresh-auth-debug.apk
```

Its debug signer matches the prior Step 22 APK in this workspace. No device installation was performed here. Use an existing authorized customer account and linked Telegram account on the device; do not paste passwords, codes or bearer tokens into logs or source.

Verify password login → Telegram OTP → four tabs; account details; force-stop/reopen → server-validated session restore; logout → relaunch requires login. Check incorrect/expired code and service/network errors. Open each login/OTP input with Gboard, rotate, scroll, dismiss keyboard with Back, and confirm no blank area or clipped input. Confirm the first Back dismisses keyboard, subsequent Back returns from OTP/secondary tab, and modal Back works. Check launcher, adaptive masking and splash on the actual OS.

For native Keystore encryption/tamper tests on a dedicated debug install only:

```sh
cd android-app/android
./gradlew :app:connectedDebugAndroidTest
```

These tests clear that install's saved session. No attached device/emulator is available in this executor. Target-35 edge-to-edge opt-out remains part of the prior keyboard fix; a future target-36 migration requires a separate compatible single-inset-owner solution.
