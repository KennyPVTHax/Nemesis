# NEMESIS source preservation

This review import preserves the deployed FastAPI/Telegram registration/Firebase-inventory source and the current Android 0.3.0 application. It does not deploy, restart services, activate monitoring or merge itself.

- backend/: ten checksum-identical exported Python modules.
- android/: existing React/Vite/Capacitor project; native Gradle project at android/android/ to retain build compatibility.
- legacy/preserved-features/: reviewed real earlier extracted UI. This is not a recovered standalone website.
- docs/: feature status, source manifests, security findings, build verification and restoration instructions. Prior branch documentation is retained in prior-review/ and Git history.
- tests/: temporary SQLite backend regressions; no production calls.
- deployment/: nonsecret configuration requirements only; no recovered service units were supplied.

See docs/FEATURE_STATUS.md, ORIGINAL_SOURCE_MANIFEST.md, RESTORATION_GUIDE.md and VALIDATION.md. **Known source defect:** failed OTP increments roll back; a strict expected-failure test records it. Backend bytes remain unchanged pending a separately approved fix. Existing Android visuals, four tabs, login/OTP, HTTPS, encrypted sessions, keyboard repair and branding are preserved. Monitoring/APK adapters remain disconnected; no new collection or APK builder was added.

The full original website and child-device app source are unavailable. Historical mock credentials and unfinished backend-dev work remain outside this public repository. No production credentials, databases, signing keys, customer data or unreviewed monitoring payloads are imported. This is source preservation, not proof that every deployed feature or Firebase Rules is validated.
