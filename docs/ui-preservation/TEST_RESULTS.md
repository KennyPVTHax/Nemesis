# UI-preservation verification

- Frontend build and Capacitor sync passed.
- JavaScript: **51 passed, 0 failed, 1 skipped**. The inherited exact-original-input test stays skipped; alternative HTML bytes are not falsely used as the missing historical primary.
- Full-app browser: **14 scenarios passed**, including login/password/OTP, four tabs, all themes/settings disclosures, customer Firebase status/request/approved-link contracts, logout, and viewport/Back simulations. Production API responses are intercepted synthetic fixtures.
- Isolated component: **55 scenario checks passed**, zero runtime errors, zero external requests. Detailed control coverage and limitations are in BUTTON_COVERAGE.md.
- Backend/recovery metadata: **96 passed**, 0 failed, one inherited Starlette/httpx deprecation warning. All databases and network providers are isolated fixtures.
- Native Gradle application assembleDebug, testDebugUnitTest and lintDebug passed; lint **0 errors / 16 warnings**. JVM tasks contain inherited scaffold tests, not physical IME/Keystore evidence.
- APK: ZIP/DEX/CSP, Keystore plugin presence, credential-pattern scans and every packaged web asset versus final dist passed. Debug APK 5850810 bytes; SHA-256 `bf628a5296270d1aa87f1996ce734a7352fad22b9433bfaf51ad46a620208f2f`.
- The extracted render tree retains all **22 button sites, 4 inputs, 1 select, 1 textarea, 1 link**. Safe new card/drawer/copy views occupy previously missing component slots. Original baseline bytes remain in legacy/ui-preservation-baseline with explicit authorized delta hashes.

No physical Android device was available. Actual clipboard/keyboard/Back/exit and production account operations were not device-tested here. Old conditional APK-result/error controls remain source-preserved; no successful parse, SMS send, financial retrieval, credential share or deletion is fabricated. The website-only click gate remains an owner decision rather than an unreviewed authentication change. No original sensitive module was imported or activated.
