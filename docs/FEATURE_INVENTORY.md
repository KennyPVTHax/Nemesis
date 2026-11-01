# Source-based feature inventory

34 features identified from actual source and explicitly missing requirements. See [FEATURE_STATUS.md](FEATURE_STATUS.md) for verification, activation boundaries and dependencies; machine-readable rows are in FEATURES.json. Original provisional inventory is retained in prior-review/.

1. **Password login** — ACTIVE; `backend/auth_api.py`.
2. **Telegram six-digit OTP delivery** — ACTIVE; `backend/auth_api.py`.
3. **OTP three-attempt enforcement** — PARTIAL; `backend/auth_api.py`.
4. **OTP expiry and single use** — ACTIVE; `backend/auth_api.py`.
5. **Bearer sessions and logout** — ACTIVE; `backend/auth_api.py`.
6. **Owner creation and Argon2id storage** — ACTIVE; `backend/account_store.py`.
7. **Owner Telegram linking** — LEGACY; `backend/telegram_link.py`.
8. **Telegram private-chat command guard** — LEGACY; `backend/telegram_bot.py`.
9. **Bot polling offset and delivery errors** — LEGACY; `backend/telegram_bot.py`.
10. **Customer keys and redemption** — ACTIVE; `backend/registration_store.py`.
11. **Login ID reservation** — ACTIVE; `backend/registration_store.py`.
12. **Private setup and password activation** — ACTIVE; `backend/registration_api.py`.
13. **Customer renewal** — LEGACY; `backend/registration_store.py`.
14. **Account status and registration cancel** — LEGACY; `backend/telegram_bot.py`.
15. **Account eligibility and expiry** — ACTIVE; `backend/auth_api.py`.
16. **Firebase inventory CLI** — LEGACY; `backend/firebase_cli.py`.
17. **Per-customer Firebase allocation** — ACTIVE; `backend/firebase_pool.py`.
18. **Firebase link request and owner approval** — ACTIVE; `backend/firebase_api.py`.
19. **Firebase Rules and live project isolation** — PARTIAL; `backend/firebase_pool.py`.
20. **Android login/OTP API adapter** — ACTIVE; `android/src/auth/api-auth.mjs`.
21. **Encrypted saved Android sessions** — ACTIVE; `android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java`.
22. **Four primary tabs and Back** — ACTIVE; `android/src/App.jsx`.
23. **Keyboard single-owner resizing** — ACTIVE; `android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java`.
24. **Approved branding and themes** — ACTIVE; `android/src/branding/BrandLogo.jsx`.
25. **Account profile/settings/logout** — ACTIVE; `android/src/components/Settings.jsx`.
26. **Password change/history/session-list/link settings** — PARTIAL; `android/src/components/Settings.jsx`.
27. **Original monitoring dashboard controls** — INACTIVE; `android/src/generated/OriginalUI.jsx`.
28. **APK/Firebase Android interface** — INACTIVE; `android/src/generated/OriginalUI.jsx`.
29. **Reserved third tab** — ACTIVE; `android/src/components/Pages.jsx`.
30. **Earlier extracted website UI** — LEGACY; `legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx`.
31. **Historical mock authentication** — LEGACY; `private workspace checkpoint`.
32. **Independent original website project** — PENDING; `Unavailable`.
33. **Child-device Android source** — PENDING; `Unavailable`.
34. **Future child APK builder/packer** — PENDING; `Unavailable`.
