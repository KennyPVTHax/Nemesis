# Verified feature status

Statuses describe imported source/local verification, with owner-reported deployment distinguished from tests executed here. ACTIVE does not claim every device/live-service test ran. No feature was activated by importing it.

| Feature | Original location | Current location | Status | Missing dependencies | Reason for disabling / required activation work | Verification |
|---|---|---|---|---|---|---|
| Password login | export/backend/auth_api.py | backend/auth_api.py | ACTIVE | Production account/Telegram | None | Argon2id; owner-reported live; isolated tests |
| Telegram six-digit OTP delivery | export/backend/auth_api.py | backend/auth_api.py | ACTIVE | Server bot token | None | Source reviewed; owner-reported live; network not invoked |
| OTP three-attempt enforcement | export/backend/auth_api.py | backend/auth_api.py | PARTIAL | Approved transaction fix | Fix failed-attempt commit behavior in separate reviewed patch | Strict expected-failure regression confirms rollback |
| OTP expiry and single use | export/backend/auth_api.py | backend/auth_api.py | ACTIVE | Server clock | None | Single-use test passed; expiry source reviewed |
| Bearer sessions and logout | export/backend/auth_api.py | backend/auth_api.py | ACTIVE | Production DB excluded | None | Isolated verify/profile/logout passed |
| Owner creation and Argon2id storage | export/backend/account_store.py | backend/account_store.py | ACTIVE | Operator initialization | None | Temporary DB/hash tests passed |
| Owner Telegram linking | export/backend/telegram_link.py | backend/telegram_link.py | LEGACY | Owner setup/private Telegram | Review before a new deployment | Source retained; linking runtime not tested |
| Telegram private-chat command guard | export/backend/telegram_bot.py | backend/telegram_bot.py | LEGACY | Bot token and verified sender | Review runtime permissions | Source reviewed, no poller started |
| Bot polling offset and delivery errors | export/backend/telegram_bot.py | backend/telegram_bot.py | LEGACY | Private offset file | Review before running poller | Source retained; no live test |
| Customer keys and redemption | export/backend/registration_store.py | backend/registration_store.py | ACTIVE | Existing owner | None | Isolated registration passed |
| Login ID reservation | export/backend/registration_store.py | backend/registration_store.py | ACTIVE | Redeemed key | None | Isolated setid passed |
| Private setup and password activation | export/backend/registration_api.py | backend/registration_api.py | ACTIVE | Private signup link | None | Isolated activation/single-use passed |
| Customer renewal | export/backend/registration_store.py | backend/registration_store.py | LEGACY | Valid one-use key | Add renewal/concurrency tests | Source reviewed; renewal not exercised |
| Account status and registration cancel | export/backend/telegram_bot.py | backend/telegram_bot.py | LEGACY | Telegram identity | Add bot command tests; stale help needs proposal | Source retained, no Telegram invocation |
| Account eligibility and expiry | export/backend/auth_api.py | backend/auth_api.py | ACTIVE | DB state | None | Owner-null/customer-expired tests passed |
| Firebase inventory CLI | export/backend/firebase_cli.py | backend/firebase_cli.py | LEGACY | Private service-account files and OS permissions | Operator/security review before use | Source retained; operator actions not run |
| Per-customer Firebase allocation | export/backend/firebase_pool.py | backend/firebase_pool.py | ACTIVE | Inventory entries | No live Firebase connectivity claimed | Isolated two-customer allocation test passed |
| Firebase link request and owner approval | export/backend/firebase_api.py | backend/firebase_api.py | ACTIVE | Owner approval | Independent Firebase Rules review still required | Isolated approval/isolation passed |
| Firebase Rules and live project isolation | export/backend/firebase_pool.py | backend/firebase_pool.py | PARTIAL | Isolated Firebase project and Rules source | Run actual Firebase authorization tests | Only allocation exists; Rules not supplied |
| Android login/OTP API adapter | workspace/android-app/src/auth/api-auth.mjs | android/src/auth/api-auth.mjs | ACTIVE | Existing HTTPS API | None | JS/browser tests; owner reports device login working |
| Encrypted saved Android sessions | workspace/android-app/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java | android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java | ACTIVE | Android Keystore | Native test remains | JS persistence tests; native device execution not run |
| Four primary tabs and Back | workspace/android-app/src/App.jsx | android/src/App.jsx | ACTIVE | Android runtime for physical Back | Physical verification remains | Browser navigation passed |
| Keyboard single-owner resizing | workspace/android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java | android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java | ACTIVE | Gboard/device | Physical IME check remains | Source/short-viewport regressions passed |
| Approved branding and themes | workspace/android-app/src/branding/BrandLogo.jsx | android/src/branding/BrandLogo.jsx | ACTIVE | OS launcher for masking review | None | Asset dimensions and theme tests passed |
| Account profile/settings/logout | workspace/android-app/src/components/Settings.jsx | android/src/components/Settings.jsx | ACTIVE | HTTPS API | None | Authenticated profile and logout tests passed |
| Password change/history/session-list/link settings | workspace/android-app/src/components/Settings.jsx | android/src/components/Settings.jsx | PARTIAL | Additional reviewed APIs | Implement separate approved integration | UI retained; endpoints absent from export |
| Original monitoring dashboard controls | workspace/android-app/src/generated/OriginalUI.jsx | android/src/generated/OriginalUI.jsx | INACTIVE | Authorized device-data adapter | Remain disconnected; no collection or remote commands | Original extracted JSX/CSS hash preserved; SMS search modal tested |
| APK/Firebase Android interface | workspace/android-app/src/generated/OriginalUI.jsx | android/src/generated/OriginalUI.jsx | INACTIVE | Reviewed client Firebase API integration | Do not connect automatically | Original extracted UI retained; no backend mapping |
| Reserved third tab | workspace/android-app/src/components/Pages.jsx | android/src/components/Pages.jsx | ACTIVE | Owner future specification | Reserved by design | Browser tab check passed |
| Earlier extracted website UI | legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx | legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx | LEGACY | Full independent website missing | Compare original website if recovered | Real checkpoint source retained |
| Historical mock authentication | private workspace checkpoint | private workspace checkpoint | LEGACY | Private checkpoint | Never a production fallback | Private original retained; excluded from public import |
| Independent original website project | Unavailable | Unavailable | PENDING | Original five attachments/full website | Locate original and conduct private security review | Not recovered; only extracted UI available |
| Child-device Android source | Unavailable | Unavailable | PENDING | Original child project | Do not reconstruct or claim preserved | No actual child app source located |
| Future child APK builder/packer | Unavailable | Unavailable | PENDING | Owner specification and source | Outside import activation scope | Planned reserve only; no original implementation found |

Counts: {"ACTIVE": 18, "PARTIAL": 3, "LEGACY": 8, "INACTIVE": 2, "PENDING": 3}. Total: 34.
