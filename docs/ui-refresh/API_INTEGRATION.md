Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# Production authentication integration — 0.3.0

The owner supplied verified response structures from the deployed backend on 2026-10-30. `src/auth/api-contract.mjs` now maps that exact contract. Login is enabled. No response-property guesses or production mock fallback are used.

| Route | Request | Response used by Android |
|---|---|---|
| POST https://nemesispanel.shop/auth/login | JSON `login_id`, `password` | `challenge_id`, `expires_in` in seconds |
| POST /auth/verify | JSON `challenge_id`, six-character numeric `code` | `access_token`, `token_type: bearer`, `expires_in` in seconds |
| GET /auth/me | Bearer authorization | Root `login_id`, `role`, `is_active`, nullable `expires_at` in UNIX seconds |
| POST /auth/logout | Bearer authorization; no request body | Successful HTTP status; no invented required body |

`login_id` is the canonical identity returned by this API; no separate database ID is supplied. The adapter's normalized `id` aliases that value and is not used to authorize another account. Unknown response properties are not rendered or used.

After successful password validation, the challenge stays only in memory and the six-digit OTP interface opens. The backend delivers the code to the previously linked Telegram account. Codes and passwords are cleared from the rendered component state on submission. No Telegram bot credentials or client-generated OTPs are used. Restart login requests a fresh challenge through the confirmed login endpoint, subject to server limits. There is no invented resend route.

Verification alone does not open the tabs. The returned bearer must first succeed at `/auth/me` and yield a valid, active account. `expires_at: null` means no configured **account** expiry. A finite account timestamp is converted from seconds and checked separately from the **session** lifetime returned by `/auth/verify`. The expected 300-second challenge and 28,800-second token lifetimes are read from responses rather than invented timers. Derived local deadlines begin at receipt and are approximate; the server remains authoritative. Inactive, expired or malformed accounts fail closed. Session/account expiry timers clear access locally; profile checks run on foreground and account refresh. HTTP 401/403 clears the session; 422, 429 and 5xx have safe actionable messages without reflecting arbitrary server error content.

## Android transport

This execution reached `/health` (200) and `/auth/me` without a bearer (401). The owner independently reports successful live login/OTP/profile/logout tests. `/openapi.json`, `/docs` and the root are 404. Preflight for login/profile from `https://localhost` returns 405; health also returns no CORS allowance. Browser fetch would therefore be blocked from the packaged WebView origin.

The Android app now uses the existing Capacitor native HTTPS API directly, limited by its integration layer to the four exact route/method pairs above. It sends JSON and bearer headers, rejects redirects and other origins/paths, and sets connection/read timeouts. Platform TLS verification remains enabled. No server/proxy/CORS changes, trust overrides, global fetch patch, arbitrary API URL setting or native storage permissions were added. The strict original API-only CSP remains. Browser development uses ordinary fetch and still requires appropriate CORS or an isolated test harness; browser CORS is not claimed fixed on the server.

Capacitor native sockets cannot be physically aborted through this API. The wrapper discards aborted/timed-out responses, and adapter epochs prevent stale results restoring access. A request already received by the server may still execute; server expiry/revocation remains authoritative. No automatic retry can repeat OTP verification.

## Secure session storage

The Android-only `SecureSession` plugin uses AES-256-GCM, a random IV, package/version AAD, and a non-exportable Android Keystore key. Only authenticated ciphertext and its IV are stored in private SharedPreferences. Hardware backing depends on the device; no universal hardware-backed guarantee is claimed. Passwords, OTPs, challenges and profile records are never persisted. Backups and device transfer are excluded. Capacitor logging is disabled, and plugin errors contain no exception/payload details.

A bearer is saved only after validated `/auth/me`. Startup decrypts an unexpired envelope, then revalidates `/auth/me` before displaying the tabs. An unavailable service does not grant offline customer access. Corrupt, expired or rejected sessions are discarded. Persistence failures cancel login and attempt to revoke the newly issued bearer; there is no plaintext storage fallback. Native storage operations are serialized so logout cannot be overtaken by a delayed write. Logout clears memory, deletes the Keystore key and saved envelope, then requests server revocation. Failed local deletion or unconfirmed server revocation is disclosed. A browser preview uses volatile memory only.

No refresh-token endpoint, new backend, account provisioning, password-change API or security-history API was invented. The separate unfinished `backend-dev` directory is not used, deployed or packaged.

## Remaining validation

No live account password or OTP was supplied or used here. Automated auth tests use synthetic identities with the owner's exact response schema. Real Telegram delivery, account login/logout/revocation and native storage across a process restart must still be exercised on the owner's Android device. This distinction is not an authentication configuration blocker; the APK now contains the completed production response mapping and enabled login flow.
