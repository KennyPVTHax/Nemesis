#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${JAVA_HOME:?Set JAVA_HOME to a full JDK 21 installation}"
: "${ANDROID_HOME:?Set ANDROID_HOME to an Android SDK installation}"
command -v node >/dev/null
"$JAVA_HOME/bin/javac" -version
npm ci --no-audit --no-fund
npm run build
npx cap sync android
(cd android && ./gradlew --no-daemon :app:assembleDebug :app:testDebugUnitTest :app:lintDebug :app:assembleDebugAndroidTest)
