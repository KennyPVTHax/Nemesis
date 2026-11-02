# Original feature implementation audit

Audited 2026-11-02 against `44bd8d709fe2dd3fc2803f55cac72d05be30e71c` on `review/original-feature-code-audit`. This audit does not change or activate application/backend code.

**Finding: full original implementation preservation cannot be established.** The Android extraction preserves selected rendered markup/styles, not the original website business logic. Several entire child renderers are missing. The contemporaneous website analysis is evidence of what was inspected then; it is not a recoverable source implementation. Historical source hashes alone are not a backup.

## Evidence and limits

- Reviewed the requested status/provenance documents, current generated UI, all tracked legacy files and all available local application checkpoints. No source was fetched from production or recreated from assumptions.
- Six ZIP archives were opened and every member hashed; two Step 22 before/after directories and `/workspace/android-app` were compared. The census records 1004 archive/directory file occurrences and 92 unique first-party code/configuration variants. Tests, generated bundles/native packaged assets, binaries and vendored dependencies are excluded from the source-variant recovery set, but archive entries remain listed in the census.
- All 216 reachable Git blobs and current remote refs were checked for the original attachment SHA-256 values. No matching original attachment blob or readable workspace/tmp file was found. Search limits and exact remote commits are in [SEARCH_EVIDENCE.json](original-feature-code-audit/SEARCH_EVIDENCE.json).
- Original HTML line ranges below are **historical coordinates** from [the preserved contemporaneous analysis](original-feature-code-audit/evidence/EXISTING_PROJECT_ANALYSIS.md) (copied unchanged from `/workspace/docs/EXISTING_PROJECT_ANALYSIS.md`), not line numbers reverified against missing HTML. Symbols are named only where surviving provenance/bindings identify them. No missing original function names are invented.
- Website `.bak` was a different historical version. Its individual function offsets/content cannot be compared without recovering that file. The exported FastAPI backend is a later separate source, not the missing original Firebase REST website handlers.

## Original attachment availability

| Original file | Historical SHA-256 | Current recoverable source |
|---|---|---|
| `1-surgeignore` | `82aab09128b8a3feee151e78f30bbea617c9e6fab29bc3a3a338dc992bcee08d` | MISSING; original input path absent; manifest only |
| `2-200.html` | `1293fcff7a500f0f4bb21cf4da4d736d797a563508dbad21fe7e8ce3bdfead6a` | MISSING; original input path absent; manifest only |
| `3-CNAME` | `e596ec303e63edfc706ff615020ce97d0fdce6a48ca7808589fab1921931c12a` | MISSING; original input path absent; manifest only |
| `4-index.html` | `1293fcff7a500f0f4bb21cf4da4d736d797a563508dbad21fe7e8ce3bdfead6a` | MISSING; original input path absent; manifest only |
| `5-index.html.bak` | `03ac69798436219826120bef5eeb1c92d997fbdf72775a2fdcf2975f786bdb7c` | MISSING; original input path absent; manifest only |

`2-200.html` and `4-index.html` had identical historical bytes; `5-index.html.bak` had different bytes. These five artifacts remain unavailable. No full editable original React project, source map, native child-device project, child APK builder implementation or original website backend/Rules was located. A missing-source requirement does not prove such code once existed.

## Feature-by-feature original website comparison

Every row uses `4-index.html` as the original file except explicitly named deployment files. Current paths are repository-relative GitHub locations on this review branch. `UI_ONLY` means no original operational handler; `PARTIAL_IMPLEMENTATION` means some local behavior survives, not complete parity.

| Original feature | Original source coordinate | Current GitHub source location | Preservation | Exact limitation |
|---|---|---|---|---|
| Brand/title, logos and iconography | s1/p1 render, original HTML application section | `android/src/generated/OriginalUI.jsx:63`; generated/icons.js | PARTIAL_RENDER | Account/dashboard decorations and 29 icon definitions retained; entire original branding/gate implementation not recovered. |
| Tailwind/card/layout styling | inline style blocks | android/src/generated/original.css; styles.mjs | PARTIAL_SOURCE | Extracted CSS retained; provenance expressly excludes anti-inspection CSS. |
| Four themes and persistence | 21162–21198 | android/src/App.jsx; components/Settings.jsx; generated/original.css | ADAPTED | Palette/styles retained; React theme selection/persistence is a wrapper implementation; original widget JS absent. |
| Stars, blobs, fog, snowflakes | inline styles and render sections | android/src/generated/OriginalUI.jsx; generated/original.css; components/Pages.jsx | PARTIAL_RENDER | Selected decorative markup/styles retained; no proof of complete original root composition. |
| Telegram support link | original literal labels/navigation; exact function unavailable | android/src/generated/OriginalUI.jsx | PARTIAL_RENDER | Retained links/labels do not preserve original navigation implementation; raw source needed. |
| Telegram channel join gate | original root before account chooser | No implementation located | MISSING | Gate component and confirmation logic absent; new login is not original gate source. |
| Anti-inspection/frame-buster/debugger trap | added current index; exact functions unavailable | No implementation located | MISSING | Excluded during extraction; neither JS nor excluded CSS recovered. |
| Saved Firebase accounts/config storage | 18109–18120; s1 18658–19361 | `android/src/generated/OriginalUI.jsx:54` | UI_ONLY | tt initializes []; localStorage loader/saver absent. |
| Add database URL and secret | s1 18658–19361 | `android/src/generated/OriginalUI.jsx:56`; URL/key inputs 455/470 | UI_ONLY | blocked/A alias replaces connection/save; backend manager is a later distinct implementation. |
| Bulk database connect | s1 18658–19361 | `android/src/generated/OriginalUI.jsx:455` | UI_ONLY | Textarea retained; bulk parse/connect handler absent. |
| Connect existing saved account | 18121–18175; s1 | `android/src/generated/OriginalUI.jsx:57` | UI_ONLY | at=blocked; yn throws instead of Firebase REST. |
| Delete saved account | s1 18658–19361 | `android/src/generated/OriginalUI.jsx:57` | UI_ONLY | Z=blocked; no original storage deletion code. |
| Single share/copy/decode links | 18525–18540; s1 | `android/src/generated/OriginalUI.jsx:57` | UI_ONLY | c/I blocked; ?s= decode/credential serialization absent. |
| Multi-select/merge/share | s1; root 21142–21157 | `android/src/generated/OriginalUI.jsx:57` | UI_ONLY | toggleSel/openMerged blocked; no ?m= merge/decode. |
| APK upload/drop/ZIP inspection | 18542–18632; s1 | `android/src/generated/OriginalUI.jsx:59`–60 | UI_ONLY | it/bt clear/ignore input and show unavailable; no ZIP/parser implementation. |
| APK Firebase URL/key/project/package extraction/copy | 18542–18632; s1 | `android/src/generated/OriginalUI.jsx:410`–436 | UI_ONLY | No extractor; L remains null; Zu copy renderer replaced with NotIntegrated. |
| Telegram APK document/parse notifications | 18542–18632 | No original implementation located | MISSING | No original sendDocument/report code retained. Auth bot is unrelated replacement integration. |
| Automatic credential/device Telegram reports | 18177–18196; p1 | No original implementation located | MISSING | Original embedded credential/report logic absent; no secrets reconstructed. |
| Dashboard header/status/empty state | p1 20346–21139 | `android/src/generated/OriginalUI.jsx:563` | PARTIAL_RENDER | Selected p1 return expression retained, not complete component logic. |
| Total/online/offline/bank/card counts | p1 20346–21139 | `android/src/generated/OriginalUI.jsx:564` | UI_ONLY | it/bt/y/_ fixed zero; no counting/analysis implementation. |
| Device name/number/ID search | p1 | `android/src/generated/OriginalUI.jsx:709` | UI_ONLY | Input state survives; mt fixed []; no real filtering pipeline. |
| All/online/offline/saved/UPI/bank/card filters | p1 | `android/src/generated/OriginalUI.jsx:565`; filter buttons 829 | UI_ONLY | Selection changes w, but data derivation absent. |
| Newest/oldest/name/battery sort | p1 | `android/src/generated/OriginalUI.jsx:565` | UI_ONLY | Sort state retained; mt fixed []; no comparator pipeline. |
| Manual refresh/loading/error/toast | p1 | `android/src/generated/OriginalUI.jsx:568` | PARTIAL_RENDER | Refresh I only sets unavailable message; error/skeleton renderers h1/m1 survive. |
| 15s device and 45s analysis polling | 18121–18175; p1 | No original poller implementation located | MISSING | No Firebase refresh timers present in extracted dashboard. |
| Saved-device stars and storage | 19362–19793; p1 | `android/src/generated/OriginalUI.jsx:564`; Sv 568/935 | UI_ONLY | sv new empty Set, Sv aliases unavailable refresh; original persistence absent. |
| Device cards/model/ID/Android/battery/SIM/network | 19362–19793; f1 | `android/src/generated/OriginalUI.jsx:6`; invocation 931 | COMPONENT_MISSING | f1=NotIntegrated; original card renderer not preserved, not merely disconnected. |
| Phone/bank/field copy | 19362–20345; Zu | `android/src/generated/OriginalUI.jsx:6`; invocations 410/423/436 | COMPONENT_MISSING | Zu=NotIntegrated; original reusable copy renderer missing. |
| Online/offline/last-seen timestamps | 19362–19793; p1 | `android/src/generated/OriginalUI.jsx:564` | UI_ONLY | No live timestamps/model; X em dash; original calculations absent. |
| SMS Searcher query/clear/close modal | p1 | `android/src/generated/OriginalUI.jsx:948`–1120 | PARTIAL_IMPLEMENTATION | Modal and local case-insensitive content filter retained; source d always empty; escape/back added. |
| Cross-device SMS loading/progress/search | p1 20346–21139 | `android/src/generated/OriginalUI.jsx:566`; onChange 1042 | PARTIAL_IMPLEMENTATION | Local search over dev._sms retained, but acquisition/aggregation absent; no network data. |
| Device drawer and Info tab | 19794–20345; d1 | `android/src/generated/OriginalUI.jsx:6`; invocation 1123 | COMPONENT_MISSING | d1=NotIntegrated, x=null; original drawer/Info renderer and handlers missing. |
| SMS list/sender/date/content | 19794–20345; d1 | Only missing drawer binding; no original component | MISSING | SMS panel renderer and 6-second message poller absent; search-modal snippets are not full SMS module. |
| Bank balances/transaction parsing/tab | 18198–18512; 19794–20345 | Labels/count shell only | MISSING | No original parsers or Bank panel implementation recovered. |
| Card/expiry/CVV extraction/reveal | 18198–18512; d1 | Labels/count shell only | MISSING | Original parser, display and reveal implementation absent; stays inactive. |
| UPI PIN/Auto Token panel | 18198–18512; d1 | Labels/filter shell only | MISSING | Original extraction/display code absent; stays inactive. |
| Send SMS/SIM selection/queued command | 19794–20345; clients/{deviceId}/webhookEvent/sendSms | No original implementation located | MISSING | Form/remote write handler not retained in extracted d1; stays inactive. |
| Device deletion and confirmation | 18121–18175; 19794–20345 | `android/src/generated/OriginalUI.jsx:1129` callback binding only | UI_ONLY | Callback uses replacement T/I; original DELETE and confirmation component absent. |
| Logout to account chooser | root 21142–21157; p1 | `android/src/generated/OriginalUI.jsx:568`; App.jsx | ADAPTED | Z calls new authenticated logout; original chooser root navigation absent. |
| Surge ignore/hostname/SPA fallback | 1-surgeignore; 3-CNAME; 2-200.html | Historical hashes in docs/SOURCE_MANIFEST.json | MISSING | No original configuration bytes or standalone fallback HTML available. |

## Exact replacement and mock findings

| Current file / lines | Replacement | Consequence |
|---|---|---|
| `android/src/generated/OriginalUI.jsx:6` | `Zu`, `f1`, `d1` all alias `NotIntegrated` | Copy control, device card and device drawer implementations are absent. References/props do not retain component definitions. |
| `android/src/generated/OriginalUI.jsx:55` | `tt=[]`, APK `L=null` | No saved-account data loader or parser result producer. |
| `android/src/generated/OriginalUI.jsx:56`+ | `at,c,I,Z,openMerged,toggleSel,A=blocked` | Connect/share/copy/delete/merge/select/bulk actions are replaced. Original algorithms unavailable. |
| `android/src/generated/OriginalUI.jsx:58` | `yn` throws, `nh=()=>{}` | Firebase access explicitly unavailable; empty callback survives, original role cannot be resolved beyond bindings. |
| `android/src/generated/OriginalUI.jsx:59`–60 | upload `it`/drop `bt` ignore file and display status | No APK bytes parsed/uploaded by these handlers. |
| `android/src/generated/OriginalUI.jsx:564`–568 | `Ac,d,mt=[]`, `sv=new Set`, totals zero, `x=null`; `I,q,T,Sv` unavailable aliases | No device store/filter pipeline/selection/saved-device or refresh integration; drawer cannot be reached. Z is real new logout. |
| `android/src/generated/OriginalUI.jsx:1042`–1065 | Actual local query loop over `d`/`dev._sms` | This subset is real preserved local code, but `d=[]` guarantees no data; not a complete SMS integration. |
| `android/src/components/Settings.jsx:10`–14 | Unavailable explanatory account-security rows | Password change/history/session listing/Telegram management/2SV toggling not implemented. These were new requested interfaces, not proven original website backend features. |
| `android/src/auth/api-auth.mjs:18`; `vault-queue.mjs`; `App.jsx` | Default callback and error-cleanup empty callbacks | Lifecycle/queue cleanup, not original feature replacements; do not misclassify them as missing auth. Live auth has real HTTPS code and no mock fallback. |
| Checkpoint `src/auth/mock-auth.mjs` | Offline MockAuthAdapter, local OTP and `customerAccess:false` | Real historical mock implementation recovered as sanitized inactive source. It is not server authentication. |
| UI proposal `src/main.jsx` | UI-only navigation, fake display clock and notify callbacks | Historical design preview, not the original monitoring engine. Recovered separately with provenance; never used to claim parity. |

## Exported backend: exact file and function preservation

The ten extracted export modules were rehashed against the supplied `SHA256SUMS.txt` and `docs/BACKEND_EXPORT_SHA256SUMS.txt`. All match. Archive container itself is unavailable in this resumed workspace, so its historical container checksum was not reverified. Every original module has an exact-byte current or legacy copy; this does not claim original runtime configuration, SQLite data or private credentials were exported. The vulnerable original OTP verifier remains history only; working `backend/auth_api.py` retains the security patch.

| Export source | Exact-byte current GitHub location | SHA-256 | Current extension |
|---|---|---|---|
| `export/backend/account_store.py` | `backend/account_store.py` | `b6c9a2116667451c3e496d5f23817a9a8e37c61f91b8e52ac07bd46502b538c2` | Original bytes unchanged |
| `export/backend/auth_api.py` | `legacy/backend-baseline/auth_api.py` | `6cabe5ad6729bb5d8dc93519a2c3b99ea8cc40134a0b15bef2ae89241d44fdd4` | Active `backend/auth_api.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/firebase_api.py` | `legacy/phase3-baseline/backend/firebase_api.py` | `9e499720cf5dfbb263a07c892b4a96c47be8591f2fa768dfab430981d25328e7` | Active `backend/firebase_api.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/firebase_cli.py` | `legacy/phase3-baseline/backend/firebase_cli.py` | `79c8cd23881cb3882679cc26acf8ddc799c7576afb8e0c2aa752e6278ad3b53a` | Active `backend/firebase_cli.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/firebase_pool.py` | `legacy/phase3-baseline/backend/firebase_pool.py` | `278cb7baed5479f8bf6b0ce5fc285af69c2c93b6dc0522ef3520bfe588d5e501` | Active `backend/firebase_pool.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/main.py` | `legacy/phase3-baseline/backend/main.py` | `d69c8934b00cb01be45ee860af0a8b7c62dc57fd2a42bb6e7e51e17acfe0907b` | Active `backend/main.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/registration_api.py` | `backend/registration_api.py` | `cfebc09aafc167b5de01267e4fb2ff0896e869f32fce7547fbb0f775bb6329d4` | Original bytes unchanged |
| `export/backend/registration_store.py` | `backend/registration_store.py` | `4402fa46de99d6bf48e3fc5316e5b4516640c705e825ca309c1e2b5621003bc7` | Original bytes unchanged |
| `export/backend/telegram_bot.py` | `legacy/phase3-baseline/backend/telegram_bot.py` | `92e399fa043b2fed116ec739f3ca3120c892b85c27fddd33f9db11a2d65786a4` | Active `backend/telegram_bot.py` changed in reviewed OTP/Phase 3; baseline retained |
| `export/backend/telegram_link.py` | `backend/telegram_link.py` | `2bbb32a13dd8cbca8bec36e69791f9a38bf4331f54decff24cd434cad39181fd` | Original bytes unchanged |

All exported function definitions are accounted for below (including helper functions, not only API routes). The baseline line identifies the exact implementation retained. Current code may add security checks; baseline code must not replace active OTP code.

| Original function | Exact original/baseline GitHub location | Active module |
|---|---|---|
| `export/backend/account_store.py::connect` | `backend/account_store.py:40` | `backend/account_store.py` |
| `export/backend/account_store.py::initialize` | `backend/account_store.py:47` | `backend/account_store.py` |
| `export/backend/account_store.py::create_owner` | `backend/account_store.py:62` | `backend/account_store.py` |
| `export/backend/account_store.py::verify` | `backend/account_store.py:111` | `backend/account_store.py` |
| `export/backend/auth_api.py::init` | `legacy/backend-baseline/auth_api.py:12` | `backend/auth_api.py` |
| `export/backend/auth_api.py::digest` | `legacy/backend-baseline/auth_api.py:20` | `backend/auth_api.py` |
| `export/backend/auth_api.py::deny` | `legacy/backend-baseline/auth_api.py:21` | `backend/auth_api.py` |
| `export/backend/auth_api.py::throttle` | `legacy/backend-baseline/auth_api.py:22` | `backend/auth_api.py` |
| `export/backend/auth_api.py::eligible` | `legacy/backend-baseline/auth_api.py:32` | `backend/auth_api.py` |
| `export/backend/auth_api.py::get_user` | `legacy/backend-baseline/auth_api.py:35` | `backend/auth_api.py` |
| `export/backend/auth_api.py::current_user` | `legacy/backend-baseline/auth_api.py:41` | `backend/auth_api.py` |
| `export/backend/auth_api.py::login` | `legacy/backend-baseline/auth_api.py:53` | `backend/auth_api.py` |
| `export/backend/auth_api.py::verify` | `legacy/backend-baseline/auth_api.py:78` | `backend/auth_api.py` |
| `export/backend/auth_api.py::me` | `legacy/backend-baseline/auth_api.py:94` | `backend/auth_api.py` |
| `export/backend/auth_api.py::logout` | `legacy/backend-baseline/auth_api.py:98` | `backend/auth_api.py` |
| `export/backend/firebase_api.py::status` | `legacy/phase3-baseline/backend/firebase_api.py:7` | `backend/firebase_api.py` |
| `export/backend/firebase_api.py::request` | `legacy/phase3-baseline/backend/firebase_api.py:13` | `backend/firebase_api.py` |
| `export/backend/firebase_api.py::approved` | `legacy/phase3-baseline/backend/firebase_api.py:21` | `backend/firebase_api.py` |
| `export/backend/firebase_cli.py::strict_url` | `legacy/phase3-baseline/backend/firebase_cli.py:8` | `backend/firebase_cli.py` |
| `export/backend/firebase_cli.py::run` | `legacy/phase3-baseline/backend/firebase_cli.py:14` | `backend/firebase_cli.py` |
| `export/backend/firebase_pool.py::init` | `legacy/phase3-baseline/backend/firebase_pool.py:9` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::eligible` | `legacy/phase3-baseline/backend/firebase_pool.py:38` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::assignment` | `legacy/phase3-baseline/backend/firebase_pool.py:42` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::allocate` | `legacy/phase3-baseline/backend/firebase_pool.py:45` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::get_or_assign` | `legacy/phase3-baseline/backend/firebase_pool.py:56` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::summary` | `legacy/phase3-baseline/backend/firebase_pool.py:62` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::request_link` | `legacy/phase3-baseline/backend/firebase_pool.py:69` | `backend/firebase_pool.py` |
| `export/backend/firebase_pool.py::approved_url` | `legacy/phase3-baseline/backend/firebase_pool.py:82` | `backend/firebase_pool.py` |
| `export/backend/main.py::health` | `legacy/phase3-baseline/backend/main.py:11` | `backend/main.py` |
| `export/backend/registration_api.py::register` | `backend/registration_api.py:9` | `backend/registration_api.py` |
| `export/backend/registration_api.py::page` | `backend/registration_api.py:15` | `backend/registration_api.py` |
| `export/backend/registration_store.py::hashval` | `backend/registration_store.py:4` | `backend/registration_store.py` |
| `export/backend/registration_store.py::init` | `backend/registration_store.py:5` | `backend/registration_store.py` |
| `export/backend/registration_store.py::new_key` | `backend/registration_store.py:13` | `backend/registration_store.py` |
| `export/backend/registration_store.py::redeem` | `backend/registration_store.py:20` | `backend/registration_store.py` |
| `export/backend/registration_store.py::setid` | `backend/registration_store.py:40` | `backend/registration_store.py` |
| `export/backend/registration_store.py::status` | `backend/registration_store.py:52` | `backend/registration_store.py` |
| `export/backend/registration_store.py::setup` | `backend/registration_store.py:60` | `backend/registration_store.py` |
| `export/backend/registration_store.py::activate` | `backend/registration_store.py:73` | `backend/registration_store.py` |
| `export/backend/telegram_bot.py::api` | `legacy/phase3-baseline/backend/telegram_bot.py:20` | `backend/telegram_bot.py` |
| `export/backend/telegram_bot.py::send` | `legacy/phase3-baseline/backend/telegram_bot.py:75` | `backend/telegram_bot.py` |
| `export/backend/telegram_bot.py::process` | `legacy/phase3-baseline/backend/telegram_bot.py:83` | `backend/telegram_bot.py` |
| `export/backend/telegram_bot.py::load_offset` | `legacy/phase3-baseline/backend/telegram_bot.py:188` | `backend/telegram_bot.py` |
| `export/backend/telegram_bot.py::save_offset` | `legacy/phase3-baseline/backend/telegram_bot.py:195` | `backend/telegram_bot.py` |
| `export/backend/telegram_bot.py::main` | `legacy/phase3-baseline/backend/telegram_bot.py:204` | `backend/telegram_bot.py` |
| `export/backend/telegram_link.py::initialize` | `backend/telegram_link.py:11` | `backend/telegram_link.py` |
| `export/backend/telegram_link.py::issue_code` | `backend/telegram_link.py:23` | `backend/telegram_link.py` |
| `export/backend/telegram_link.py::consume_code` | `backend/telegram_link.py:62` | `backend/telegram_link.py` |
| `export/backend/telegram_link.py::is_owner` | `backend/telegram_link.py:125` | `backend/telegram_link.py` |

Export features include Argon2 account initialization, linked owner, login/OTP/bearer/logout/eligibility, key generation/redemption/renewal/set-ID/setup/cancel, registration activation, bot private sender checks/polling offsets/403 recovery, Firebase inventory/one-customer assignment/link approval, API health and registration page. These have actual code, not just UI. Production credentials/data/service configuration are intentionally absent.

## Historical 34-feature inventory reconciliation

This separately reconciles every row of `docs/FEATURE_STATUS.md` / `FEATURES.json`; aggregate website rows are expanded into the 40 website comparisons above. “Implementation retained” is source availability, not a claim of live production verification.

| Historical feature | Original source file | Current code / preservation finding |
|---|---|---|
| 1. Password login | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. |
| 2. Telegram six-digit OTP delivery | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. |
| 3. OTP three-attempt enforcement | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. Current verifier contains deployed/reviewed OTP fix; historical PARTIAL/xfail label is obsolete. |
| 4. OTP expiry and single use | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. |
| 5. Bearer sessions and logout | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. |
| 6. Owner creation and Argon2id storage | `export/backend/account_store.py` | `backend/account_store.py`; original implementation retained at exact-byte backend location above. |
| 7. Owner Telegram linking | `export/backend/telegram_link.py` | `backend/telegram_link.py`; original implementation retained at exact-byte backend location above. |
| 8. Telegram private-chat command guard | `export/backend/telegram_bot.py` | `backend/telegram_bot.py`; original implementation retained at exact-byte backend location above. |
| 9. Bot polling offset and delivery errors | `export/backend/telegram_bot.py` | `backend/telegram_bot.py`; original implementation retained at exact-byte backend location above. |
| 10. Customer keys and redemption | `export/backend/registration_store.py` | `backend/registration_store.py`; original implementation retained at exact-byte backend location above. |
| 11. Login ID reservation | `export/backend/registration_store.py` | `backend/registration_store.py`; original implementation retained at exact-byte backend location above. |
| 12. Private setup and password activation | `export/backend/registration_api.py` | `backend/registration_api.py`; original implementation retained at exact-byte backend location above. |
| 13. Customer renewal | `export/backend/registration_store.py` | `backend/registration_store.py`; original implementation retained at exact-byte backend location above. |
| 14. Account status and registration cancel | `export/backend/telegram_bot.py` | `backend/telegram_bot.py`; original implementation retained at exact-byte backend location above. |
| 15. Account eligibility and expiry | `export/backend/auth_api.py` | `backend/auth_api.py`; original implementation retained at exact-byte backend location above. |
| 16. Firebase inventory CLI | `export/backend/firebase_cli.py` | `backend/firebase_cli.py`; original implementation retained at exact-byte backend location above. |
| 17. Per-customer Firebase allocation | `export/backend/firebase_pool.py` | `backend/firebase_pool.py`; original implementation retained at exact-byte backend location above. |
| 18. Firebase link request and owner approval | `export/backend/firebase_api.py` | `backend/firebase_api.py`; original implementation retained at exact-byte backend location above. |
| 19. Firebase Rules and live project isolation | `export/backend/firebase_pool.py` | Original export contains allocation metadata, not Rules; Phase 3 adds real `firebase_cloud.py`, gateway, deny-all Rules and emulator tests. Original website Rules were not supplied. |
| 20. Android login/OTP API adapter | `workspace/android-app/src/auth/api-auth.mjs` | `android/src/auth/api-auth.mjs`; real production HTTPS adapter; pre-Phase3 adapter in `legacy/phase3-baseline/android/src/auth/api-auth.mjs`; earlier variants indexed below. |
| 21. Encrypted saved Android sessions | `workspace/android-app/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` and `SecureSessionPlugin.java`; actual Java implementation retained. |
| 22. Four primary tabs and Back | `workspace/android-app/src/App.jsx` | `android/src/App.jsx`; actual tabs/back/navigation implementation; earlier App variants recovered/indexed. |
| 23. Keyboard single-owner resizing | `workspace/android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java`; current fix intact; actual old Java variants recovered and excluded from build. |
| 24. Approved branding and themes | `workspace/android-app/src/branding/BrandLogo.jsx` | `android/src/branding/BrandLogo.jsx`, `ui-refresh.css`, native resources, `App.jsx`; actual current branding/theme source; earlier logo components/style variants indexed. No original website widget JS recovered. |
| 25. Account profile/settings/logout | `workspace/android-app/src/components/Settings.jsx` | `android/src/components/Settings.jsx`, `auth/api-auth.mjs`; actual profile/refresh/logout, pre-Phase3 Settings exact copy retained in phase3-baseline. |
| 26. Password change/history/session-list/link settings | `workspace/android-app/src/components/Settings.jsx` | `android/src/components/Settings.jsx:10`–14; explanatory UI only. No missing endpoint implementation in export/checkpoints. |
| 27. Original monitoring dashboard controls | `workspace/android-app/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx`; partial render/blocked handlers only. Detailed missing code above; NOT complete original implementation. |
| 28. APK/Firebase Android interface | `workspace/android-app/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx`; partial render/blocked handlers only. Detailed missing code above; NOT complete original implementation. |
| 29. Reserved third tab | `workspace/android-app/src/components/Pages.jsx` | `android/src/components/Pages.jsx`; deliberately reserved UI. No unspecified feature implementation expected or invented. |
| 30. Earlier extracted website UI | `legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx` | `legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx`; exact checkpoint render extraction; already disconnected in earliest checkpoint. |
| 31. Historical mock authentication | `private workspace checkpoint` | `legacy/preserved-features/checkpoint-code/01ae6b223665/src/auth/mock-auth.mjs`; actual offline mock algorithm recovered, fixed demo literals redacted. Exact private original locations/digest in census. |
| 32. Independent original website project | `Unavailable` | MISSING. Five original website files unavailable; historical hashes/analysis only. No original editable website repo recovered. |
| 33. Child-device Android source | `Unavailable` | MISSING. Only panel-wrapper native source available; it is not a child-device app implementation. |
| 34. Future child APK builder/packer | `Unavailable` | MISSING/UNPROVEN. Future requirement, not a recovered original APK packer implementation. |

## Existing Phase 3 baseline verification

Every file in `legacy/phase3-baseline/` matches its recorded original digest. Active changes are separate, and no file under that baseline is edited in this audit.

| Exact baseline path | Original/active path | Verified original SHA-256 |
|---|---|---|
| `legacy/phase3-baseline/android/src/auth/api-auth.mjs` | `android/src/auth/api-auth.mjs` | `893b7fb599c0390bb4aaf9dff4d73e1e57f0d3c97ed2180737101d146dc397d1` |
| `legacy/phase3-baseline/android/src/auth/https-transport.mjs` | `android/src/auth/https-transport.mjs` | `505ead3f246dccf0ff2c7ba23d6534e366e9f1752c9994e057d704a8c719ed2f` |
| `legacy/phase3-baseline/android/src/components/Settings.jsx` | `android/src/components/Settings.jsx` | `de06f62eeba328d17df650eb58b17f416096f65a2adf71197def26e542505445` |
| `legacy/phase3-baseline/backend/firebase_api.py` | `backend/firebase_api.py` | `9e499720cf5dfbb263a07c892b4a96c47be8591f2fa768dfab430981d25328e7` |
| `legacy/phase3-baseline/backend/firebase_cli.py` | `backend/firebase_cli.py` | `79c8cd23881cb3882679cc26acf8ddc799c7576afb8e0c2aa752e6278ad3b53a` |
| `legacy/phase3-baseline/backend/firebase_pool.py` | `backend/firebase_pool.py` | `278cb7baed5479f8bf6b0ce5fc285af69c2c93b6dc0522ef3520bfe588d5e501` |
| `legacy/phase3-baseline/backend/main.py` | `backend/main.py` | `d69c8934b00cb01be45ee860af0a8b7c62dc57fd2a42bb6e7e51e17acfe0907b` |
| `legacy/phase3-baseline/backend/telegram_bot.py` | `backend/telegram_bot.py` | `92e399fa043b2fed116ec739f3ca3120c892b85c27fddd33f9db11a2d65786a4` |

## Android and legacy file-by-file reconciliation

[CHECKPOINT_FILE_COMPARISON.json](original-feature-code-audit/CHECKPOINT_FILE_COMPARISON.json) contains **every archive member**, digest and all source-variant origins, exact GitHub mappings and redaction records. The table below accounts for every unique first-party code/config variant from those sources; identical files are consolidated by full SHA-256, never by filename alone. A variant may be a historical wrapper/preview instead of original website implementation.

| SHA-256 | Original source occurrence (first; all in JSON) | Current GitHub location | Result |
|---|---|---|---|
| `bbe200ceb34437f2b6d190ac3aaf38764b104f76a8c7d819e9ce5008941ddec6` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/package.json` | `legacy/preserved-features/checkpoint-code/bbe200ceb344/package.json` | RECOVERED_EXACT_BYTES |
| `abb938c6a666042edb0195c7b431f3b3192ecef4ee9bff2e810fdba5025bf4e1` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/vite.config.js` | `android/vite.config.js` | EXACT_BYTES_ALREADY_IN_GIT |
| `c486dd7a326ab26f955beb133a2516d61709f1dc18b1838de635592f777a1b1d` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/index.html` | `legacy/preserved-features/checkpoint-code/c486dd7a326a/index.html` | RECOVERED_EXACT_BYTES |
| `9b1db65469c3034726e44cef1cd82d8d9f720019880b70fa4ebcfff0e3ab1475` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/capacitor.config.json` | `legacy/preserved-features/checkpoint-code/9b1db65469c3/capacitor.config.json` | RECOVERED_EXACT_BYTES |
| `2d839e748976ddd103673bf88365ce04cc992a373f821e08122d3bce8360eee0` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/scripts/export-logo.mjs` | `android/scripts/export-logo.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `9759b440b4a7c8851153f493e2ded4aff74e45c6abba64f4eed8b229e506ebba` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/scripts/extract-ui.mjs` | `android/scripts/extract-ui.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `6b4439bc35170fbb602be71f5957102ce2eddcdd1165dedff663182da2f2f8ac` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/variables.gradle` | `android/android/variables.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `fb90e59c50e34b6a070b02270aea3994c6f8ab53731bbe7a4e6815214502e45f` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/local.properties` | `legacy/preserved-features/checkpoint-code/fb90e59c50e3/android/local.properties` | RECOVERED_EXACT_BYTES |
| `6ce098d15ebd69b44c4ecd786bca1bdc366340d2459b2af4d7bb0ab317aa9669` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/settings.gradle` | `android/android/settings.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `8c79463755fe8086390e9e6c702979db88df37d7769e50fc958b30eaebc64c78` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/capacitor.settings.gradle` | `android/android/capacitor.settings.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `3bab15c5b8bc4c2f4b6cf525497d15ad4abca53a460e6dd2eb0f0135817d31e6` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/gradle.properties` | `android/android/gradle.properties` | EXACT_BYTES_ALREADY_IN_GIT |
| `9c4d6e6418d24f903a6d8710a3d829acbf4dbd14959a6617643f5e03f5bd53ae` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/build.gradle` | `android/android/build.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `475bfed8e40108ef4a852df92f89c6db7deb959c6e8f0b4f9d03dc2f329e4e8a` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/main.jsx` | `legacy/preserved-features/checkpoint-code/475bfed8e401/src/main.jsx` | RECOVERED_EXACT_BYTES |
| `803f6ac87dd8c44708d1ba3f4ae701d32ea88f24998d1a19529a1afbfd7e98d7` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/App.jsx` | `legacy/preserved-features/checkpoint-code/803f6ac87dd8/src/App.jsx` | RECOVERED_EXACT_BYTES |
| `89f2e64813c1aae5d76c7cc0607da2a2769b43b83e8525ca6c868bedd8aed910` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/mobile.css` | `legacy/preserved-features/phase1-ui/src/mobile.css` | EXACT_BYTES_ALREADY_IN_GIT |
| `d9b722bc9784798bd46d7340c87ecb028ccf99cfbf599d9e855a52efdfe817b8` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/capacitor.build.gradle` | `android/android/app/capacitor.build.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `6c802557068e9bc1971594d592aee39eb3dff784b67bb2e2a0c2c4e9d333f77f` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/build.gradle` | `legacy/preserved-features/checkpoint-code/6c802557068e/android/app/build.gradle` | RECOVERED_EXACT_BYTES |
| `268844885a8d04cf34044ffbe362499ca14836fd1123d05e64f94b12798a8bb9` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/capacitor-cordova-android-plugins/cordova.variables.gradle` | `legacy/preserved-features/checkpoint-code/268844885a8d/android/capacitor-cordova-android-plugins/cordova.variables.gradle` | RECOVERED_EXACT_BYTES |
| `8f5cea7b546643b388fc1f3a83633cc12657fea59fec8ae19d76253cb6c13cc1` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/capacitor-cordova-android-plugins/build.gradle` | `legacy/preserved-features/checkpoint-code/8f5cea7b5466/android/capacitor-cordova-android-plugins/build.gradle` | RECOVERED_EXACT_BYTES |
| `11cd0bd3430abf8dc7eee791112570fd93337f724768c96961c7d36935f46d29` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/AndroidManifest.xml` | `android/android/app/src/main/AndroidManifest.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `d4045ae8fac1f0807e6b24eb34e68409a9a235df9d1a3f896fb8c9a49424363d` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/test/java/com/getcapacitor/myapp/ExampleUnitTest.java` | `android/android/app/src/test/java/com/getcapacitor/myapp/ExampleUnitTest.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `d6cdfa659876ff4e505304ee02bf4258caac952aaa570eadc31e0d1f82641981` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `9c3a7e0a6515c6e1a7ae834a9ae430311ebc3241f7b2e5e7f0460aa690709a7c` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` | `android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`<br>`android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `5d770feb791313b947020cbfc57e5c733c556dac5e9e49261a1190e527073253` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/layout/activity_main.xml` | `android/android/app/src/main/res/layout/activity_main.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `718ba51adf166bb55c3e9936bb8199a0148457f7f0191aaa2f37a94f3159d6ec` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/drawable/ic_launcher_background.xml` | `android/android/app/src/main/res/drawable/ic_launcher_background.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `e9dcda493e663c5c4db9e3cb3bd968477a6e90aa8840bcbba40d72ed54b767ce` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/xml/config.xml` | `legacy/preserved-features/checkpoint-code/e9dcda493e66/android/app/src/main/res/xml/config.xml` | RECOVERED_EXACT_BYTES |
| `eda9dddce1e895de1efd716fe75e244187bf8f91a3bb7444c6ea1731e51c74a8` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/xml/data_extraction_rules.xml` | `android/android/app/src/main/res/xml/data_extraction_rules.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `d1e231640a2e07dfa95a4032261dec03357439a3d6615c5e7a686dcaeec691e6` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/xml/backup_rules.xml` | `android/android/app/src/main/res/xml/backup_rules.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `a46ed43ef65c90cb6778f4581decf3556e3f0055aad8f36d69dae16f9a0e99aa` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/xml/file_paths.xml` | `android/android/app/src/main/res/xml/file_paths.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `69b5adc5eb612bceb8927b68a05fd076b6b31017c4cdaf9582e18553db6696b8` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/values/ic_launcher_background.xml` | `legacy/preserved-features/checkpoint-code/69b5adc5eb61/android/app/src/main/res/values/ic_launcher_background.xml` | RECOVERED_EXACT_BYTES |
| `d7c44154328491f4aeee4222f100357ff88df031896baed74c0a98940e691f00` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/values/styles.xml` | `legacy/preserved-features/checkpoint-code/d7c441543284/android/app/src/main/res/values/styles.xml` | RECOVERED_EXACT_BYTES |
| `cc6695b22de48da1f3d9e73f15808353ecd78f1399d935f9a0dfac7f480b6d3c` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/values/strings.xml` | `android/android/app/src/main/res/values/strings.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `a8514094f754b099d3e55ce1d6e0b2de79db418b2eeacb0fc2a6bb0bfadef221` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/res/drawable-v24/ic_launcher_foreground.xml` | `android/android/app/src/main/res/drawable-v24/ic_launcher_foreground.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `213b6ed55846c5657f23aa1628b2537549dc31cf424280665c7eb86f93dfc3f9` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `legacy/preserved-features/checkpoint-code/213b6ed55846/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | RECOVERED_EXACT_BYTES |
| `df76e7afe655db04867bd53800919e1f1bd9595858ef17051d1ab7c3376a7077` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/gradle/wrapper/gradle-wrapper.properties` | `android/android/gradle/wrapper/gradle-wrapper.properties` | EXACT_BYTES_ALREADY_IN_GIT |
| `2e3e383475f0e6cb76f0a7b46017a546663fba8e5bd1ef2a537412afac2ee9b5` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/android/capacitor-cordova-android-plugins/src/main/AndroidManifest.xml` | `legacy/preserved-features/checkpoint-code/2e3e383475f0/android/capacitor-cordova-android-plugins/src/main/AndroidManifest.xml` | RECOVERED_EXACT_BYTES |
| `841064c784365ae4dc3df0b4c7f86c9c6dfe8060fbbe9ab87d891d142a08c417` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/generated/provenance.json` | `android/src/generated/provenance.json`<br>`legacy/preserved-features/phase1-ui/src/generated/provenance.json` | EXACT_BYTES_ALREADY_IN_GIT |
| `be1fd9df79f471dfe5abe9dc4bcba3df6a6ce5b1058a2a7095954cbcda947f4c` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/generated/icons.js` | `android/src/generated/icons.js`<br>`legacy/preserved-features/phase1-ui/src/generated/icons.js` | EXACT_BYTES_ALREADY_IN_GIT |
| `f12dde2cd37fa04ecca60a443f9f1e71d89288a1bfc6669e9885b14f21a82f80` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx`<br>`legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `1d7f2f9fe6709578e120e5145ed56db11c1905d679066d84992e686ac43cfecd` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/generated/original.css` | `android/src/generated/original.css`<br>`legacy/preserved-features/phase1-ui/src/generated/original.css` | EXACT_BYTES_ALREADY_IN_GIT |
| `01ae6b223665107639b754ca83587aa84ab246b827c39752c832ef1bd6a10973` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/auth/mock-auth.mjs` | `legacy/preserved-features/checkpoint-code/01ae6b223665/src/auth/mock-auth.mjs` | SANITIZED_IMPLEMENTATION |
| `cfce73df7d4c4ec4069d2909d1d59ddbb3b877d93e33318f026634f58faf9f3f` | `/workspace/checkpoints/00-phase1-baseline.zip!android-app/src/components/Auth.jsx` | `legacy/preserved-features/checkpoint-code/cfce73df7d4c/src/components/Auth.jsx` | RECOVERED_EXACT_BYTES |
| `0bbaf89f66d7fd70eb6c841dee2a2ce939e02b82a4402c70d783f5a5b68023c8` | `/workspace/checkpoints/step23-before-source.zip!android-app/package.json` | `legacy/preserved-features/checkpoint-code/0bbaf89f66d7/package.json` | RECOVERED_EXACT_BYTES |
| `cdfabe2b3a78afd5e518455cf55bee24e036031845093806bc3eb10967454942` | `/workspace/checkpoints/step23-before-source.zip!android-app/index.html` | `android/index.html` | EXACT_BYTES_ALREADY_IN_GIT |
| `651e3643a6cd3c8d8d83c9f5626f073880eef72a07cbf1f9b4c5b9ccea1007cc` | `/workspace/checkpoints/step23-before-source.zip!android-app/capacitor.config.json` | `legacy/preserved-features/checkpoint-code/651e3643a6cd/capacitor.config.json` | RECOVERED_EXACT_BYTES |
| `de068d7d67f428bdaa7111e386dcf21b4e4bf0f39ca0532eba8571395ef5d4da` | `/workspace/checkpoints/step23-before-source.zip!android-app/scripts/apply-branding.mjs` | `legacy/preserved-features/checkpoint-code/de068d7d67f4/scripts/apply-branding.mjs` | RECOVERED_EXACT_BYTES |
| `5b8b4538f8e0b28b4902b012264e43c71890c225a0016bd139ad6773b16e4a22` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/main.jsx` | `android/src/main.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `e7d9f807322db8f4eff61b25629490f40fcb904031f21727aa842878afba0856` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/App.jsx` | `legacy/preserved-features/checkpoint-code/e7d9f807322d/src/App.jsx` | RECOVERED_EXACT_BYTES |
| `095fdeb9dc4eb50a566baeeea6e57cffe1b3f228c5a6bf03139c86d0886f484b` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/styles.mjs` | `legacy/preserved-features/checkpoint-code/095fdeb9dc4e/src/styles.mjs` | RECOVERED_EXACT_BYTES |
| `7680bf333abaf06e6236c236e7993274c4858b54b260b9c3f0f8eda28b0802dd` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/mobile.css` | `android/src/mobile.css` | EXACT_BYTES_ALREADY_IN_GIT |
| `8a5f1dfdf56363eee2354e0a895006a025bcfcba0d7c97f7edf83afa42584acc` | `/workspace/checkpoints/step23-before-source.zip!android-app/android/app/build.gradle` | `legacy/preserved-features/checkpoint-code/8a5f1dfdf563/android/app/build.gradle` | RECOVERED_EXACT_BYTES |
| `17b5e8f1ebb076fee5ae1632070b1c026519774ac94dd4795d97e2e023f100e2` | `/workspace/checkpoints/step23-before-source.zip!android-app/android/app/src/main/res/values-v35/styles.xml` | `android/android/app/src/main/res/values-v35/styles.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `f5ab202b465ef289a1197bc60ee0154a3515297ee944959cc325cf49fd467f62` | `/workspace/checkpoints/step23-before-source.zip!android-app/android/app/src/main/res/values/ic_launcher_background.xml` | `legacy/preserved-features/checkpoint-code/f5ab202b465e/android/app/src/main/res/values/ic_launcher_background.xml` | RECOVERED_EXACT_BYTES |
| `a63d244239f03f171da956f1b392d4bd49a97c526e260627c6586b2872b76a0b` | `/workspace/checkpoints/step23-before-source.zip!android-app/android/app/src/main/res/values/styles.xml` | `android/android/app/src/main/res/values/styles.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `8b1d4f7b130d36113a10627ebe6c8ef12e2f66f64789f3443e9be87f471a612d` | `/workspace/checkpoints/step23-before-source.zip!android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `legacy/preserved-features/checkpoint-code/8b1d4f7b130d/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | RECOVERED_EXACT_BYTES |
| `e3dd28e6a45b9888dceb886f3e8a7ea6698125c8ee678b1a55f7cdfec305419e` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/branding/BrandLogo.jsx` | `legacy/preserved-features/checkpoint-code/e3dd28e6a45b/src/branding/BrandLogo.jsx` | RECOVERED_EXACT_BYTES |
| `de84f06afb9673797f8f80b46c43d4f285c7d2933ef2d970d754b711c691c8d0` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/branding/branding.json` | `legacy/preserved-features/checkpoint-code/de84f06afb96/src/branding/branding.json` | RECOVERED_EXACT_BYTES |
| `44a3e59dcd7835c403f128040f8528818ae761422ceb0b4cd83e0b28461243e4` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/auth/api-auth.mjs` | `legacy/preserved-features/checkpoint-code/44a3e59dcd78/src/auth/api-auth.mjs` | RECOVERED_EXACT_BYTES |
| `fbc12d1a2ae5c8850ea9fb1cdd88017dc591e7e49a2941ba9cc1adec6d90b785` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/auth/api-contract.mjs` | `legacy/preserved-features/checkpoint-code/fbc12d1a2ae5/src/auth/api-contract.mjs` | RECOVERED_EXACT_BYTES |
| `d354c5ec958f7ad99e2d7d3de847341cc23ced924b8dac43f0987f16034f5725` | `/workspace/checkpoints/step23-before-source.zip!android-app/src/components/Auth.jsx` | `legacy/preserved-features/checkpoint-code/d354c5ec958f/src/components/Auth.jsx` | RECOVERED_EXACT_BYTES |
| `2667ba411e89c9e92d84ab97164e9c88ebce4537093386ae4bb31482992f1af3` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/index.html` | `legacy/preserved-features/checkpoint-code/2667ba411e89/index.html` | RECOVERED_EXACT_BYTES |
| `0df753f7bce6135594d7fcff4592b5a27334503a45e3bc28d8b5a43a821ad7af` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/package.json` | `legacy/preserved-features/checkpoint-code/0df753f7bce6/package.json` | RECOVERED_EXACT_BYTES |
| `600c02ec642671fa7143114a2e5ed754d86e7a050817938a9d3655366deda0cf` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/scripts/boards.mjs` | `legacy/preserved-features/checkpoint-code/600c02ec6426/scripts/boards.mjs` | RECOVERED_EXACT_BYTES |
| `9cee1c3d5553bbe666f7e88112efa2c63b8147ff5bb231db41a4a8b35c911f2f` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/scripts/build.mjs` | `legacy/preserved-features/checkpoint-code/9cee1c3d5553/scripts/build.mjs` | RECOVERED_EXACT_BYTES |
| `46aded5f842d2cd2ceba386be515e01f05c415ea49ec34367e98ac581f2b46e8` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/scripts/capture.mjs` | `legacy/preserved-features/checkpoint-code/46aded5f842d/scripts/capture.mjs` | RECOVERED_EXACT_BYTES |
| `9dfa889609cb696abcbe43f09a461db2b6be56c378398ad85b522afd878784ef` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/src/main.jsx` | `legacy/preserved-features/checkpoint-code/9dfa889609cb/src/main.jsx` | RECOVERED_EXACT_BYTES |
| `258f222f55b1a528efe9b2200ed4b9d0799e2829968d7ff3a4a16eb8571fa132` | `/workspace/artifacts/ui-preview/NEMESIS-ui-proposal-source.zip!ui-proposal/src/proposal.css` | `legacy/preserved-features/checkpoint-code/258f222f55b1/src/proposal.css` | RECOVERED_EXACT_BYTES |
| `79e1863768f00879c0640b55aa932dac5ce8ecf5d3e6357ebac5dfc9873e438b` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/build.gradle` | `android/android/app/build.gradle` | EXACT_BYTES_ALREADY_IN_GIT |
| `b9d91d343c9ab83e6044efbea0c37f98e76c64807effa3f23896e50db012c02b` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/src/androidTest/java/com/nemesis/panel/dev/KeystoreSessionStoreInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/nemesis/panel/dev/KeystoreSessionStoreInstrumentedTest.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `3920fd017453549b8d8d9429583e3db0c69143c0d1bb7082aaab33db92eac6ad` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `a16a46f7bf88a81e4947b112394f12ba9ca40b309a52a202dd3848f2828bf36d` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `82251a05652c8b34f7869fe7b019a185b46afed791972b1a4ff51021ae2b84f1` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/src/main/java/com/nemesis/panel/dev/SecureSessionPlugin.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/SecureSessionPlugin.java` | EXACT_BYTES_ALREADY_IN_GIT |
| `d24846ea2daaa6e2a786742feae34cbce9ef54f07fdaed746ed46c8ab1295547` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/android/app/src/main/res/values/ic_launcher_background.xml` | `android/android/app/src/main/res/values/ic_launcher_background.xml` | EXACT_BYTES_ALREADY_IN_GIT |
| `1a5211e5a2ec4938f05d5b1e7bf2c2e6c05dfa36b37a4482ceeebdcd7908eeb1` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/capacitor.config.json` | `android/capacitor.config.json` | EXACT_BYTES_ALREADY_IN_GIT |
| `2636b63d21c174d7ef591bfbee3eefdc5c8b3e38f00fb8d9ea63906ad30927e8` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/package.json` | `android/package.json` | EXACT_BYTES_ALREADY_IN_GIT |
| `99a733452117a54414523c527f328a4f156ea26f95697661f31210562b25140d` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/scripts/apply-branding.mjs` | `android/scripts/apply-branding.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `419eb4c742d75e91d9e66ea75240404c623d3ecd870f7ffd697a2d98989e2d6e` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/scripts/preview-board.mjs` | `android/scripts/preview-board.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `a2085e470a1400bb81fc46ca3792ff2df40bb778b78ca30c0914f385bb629f59` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/App.jsx` | `android/src/App.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `893b7fb599c0390bb4aaf9dff4d73e1e57f0d3c97ed2180737101d146dc397d1` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/api-auth.mjs` | `legacy/phase3-baseline/android/src/auth/api-auth.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `14b36f9426ae32e91b1a1f882105ce52f0f6024829ab2ec3413c7488ce6b395a` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/api-contract.mjs` | `android/src/auth/api-contract.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `8f2f8a08e79da5ae7dac40e2354fd349f006449603d607f241c0b6d14f87bd3f` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/capacitor-transport.mjs` | `android/src/auth/capacitor-transport.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `505ead3f246dccf0ff2c7ba23d6534e366e9f1752c9994e057d704a8c719ed2f` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/https-transport.mjs` | `legacy/phase3-baseline/android/src/auth/https-transport.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `82d00e352170819413b1fdd7cae56ba6feafb7917bf1c09dafb9996599139966` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/secure-session.mjs` | `android/src/auth/secure-session.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `3090fd19cb1d27ae6d2bc93746a173978866c69e0c02eefdb9e4e47759e45f78` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/auth/vault-queue.mjs` | `android/src/auth/vault-queue.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `d748f4c6fddd5c6a1aeb96312c19febe8ea89464c59e6329c09a0ff527bc6969` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/branding/BrandLogo.jsx` | `android/src/branding/BrandLogo.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `fffe374728520084327444cab3cc97c0b9a59915c1c327e517273b8bbbb00e4a` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/branding/branding.json` | `android/src/branding/branding.json` | EXACT_BYTES_ALREADY_IN_GIT |
| `d02991f9055545a5f0b8e0a3db151583e6b072eb03702722c73540b819321ff8` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/components/Auth.jsx` | `android/src/components/Auth.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `94f54904ec8c35242e51a6e762f1cf47e31977fcc06209b23146fa837b5d70c7` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/components/Icon.jsx` | `android/src/components/Icon.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `24b86febe0e47c67488dc5ea6e175c19bbcb6b3db230e5b2b8251ac31b0877fb` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/components/Pages.jsx` | `android/src/components/Pages.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `de06f62eeba328d17df650eb58b17f416096f65a2adf71197def26e542505445` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/components/Settings.jsx` | `legacy/phase3-baseline/android/src/components/Settings.jsx` | EXACT_BYTES_ALREADY_IN_GIT |
| `e97d48a7f8f2e6cd1b9a46545b17c5ea2d2ecacabf9d2f441cfeb47c358630ab` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/styles.mjs` | `android/src/styles.mjs` | EXACT_BYTES_ALREADY_IN_GIT |
| `e8060c7d9f35072f35b8d2b2ac50e1421e75f4409b33f089a818493f80ca17f7` | `/workspace/artifacts/ui-refresh/nemesis-ui-refresh-source.zip!android-app/src/ui-refresh.css` | `android/src/ui-refresh.css` | EXACT_BYTES_ALREADY_IN_GIT |

## Imported-source manifest reconciliation

Every entry from the original import manifest is listed here. A previous manifest path may now contain reviewed patched bytes; the original is located by its digest, not presumed intact. Original manifests are unchanged.

| Original source | Import target | Exact-byte copy, or explicit exception |
|---|---|---|
| `android-app/package-lock.json` | `android/package-lock.json` | `android/package-lock.json` |
| `android-app/THIRD_PARTY_NOTICES.md` | `android/THIRD_PARTY_NOTICES.md` | `android/THIRD_PARTY_NOTICES.md` |
| `android-app/.gitignore` | `android/.gitignore` | `android/.gitignore` |
| `android-app/package.json` | `android/package.json` | `android/package.json` |
| `android-app/vite.config.js` | `android/vite.config.js` | `android/vite.config.js` |
| `android-app/index.html` | `android/index.html` | `android/index.html` |
| `android-app/capacitor.config.json` | `android/capacitor.config.json` | `android/capacitor.config.json` |
| `android-app/README.md` | `android/README.md` | `android/README.md` |
| `android-app/scripts/preview-board.mjs` | `android/scripts/preview-board.mjs` | `android/scripts/preview-board.mjs` |
| `android-app/scripts/apply-branding.mjs` | `android/scripts/apply-branding.mjs` | `android/scripts/apply-branding.mjs` |
| `android-app/scripts/export-logo.mjs` | `android/scripts/export-logo.mjs` | `android/scripts/export-logo.mjs` |
| `android-app/scripts/extract-ui.mjs` | `android/scripts/extract-ui.mjs` | `android/scripts/extract-ui.mjs` |
| `android-app/scripts/verify-apk.py` | `android/scripts/verify-apk.py` | `android/scripts/verify-apk.py` |
| `android-app/scripts/build-android.sh` | `android/scripts/build-android.sh` | `android/scripts/build-android.sh` |
| `android-app/android/variables.gradle` | `android/android/variables.gradle` | `android/android/variables.gradle` |
| `android-app/android/.gitignore` | `android/android/.gitignore` | `android/android/.gitignore` |
| `android-app/android/settings.gradle` | `android/android/settings.gradle` | `android/android/settings.gradle` |
| `android-app/android/capacitor.settings.gradle` | `android/android/capacitor.settings.gradle` | `android/android/capacitor.settings.gradle` |
| `android-app/android/gradle.properties` | `android/android/gradle.properties` | `android/android/gradle.properties` |
| `android-app/android/gradlew` | `android/android/gradlew` | `android/android/gradlew` |
| `android-app/android/gradlew.bat` | `android/android/gradlew.bat` | `android/android/gradlew.bat` |
| `android-app/android/build.gradle` | `android/android/build.gradle` | `android/android/build.gradle` |
| `android-app/public/nemesis-logo.jpg` | `android/public/nemesis-logo.jpg` | `android/public/nemesis-logo.jpg` |
| `android-app/public/nemesis-logo.png` | `android/public/nemesis-logo.png` | `android/public/nemesis-logo.png` |
| `android-app/public/nemesis-mark.png` | `android/public/nemesis-mark.png` | `android/public/nemesis-mark.png` |
| `android-app/licenses/Capacitor-MIT.txt` | `android/licenses/Capacitor-MIT.txt` | `android/licenses/Capacitor-MIT.txt` |
| `android-app/licenses/Inter-OFL.txt` | `android/licenses/Inter-OFL.txt` | `android/licenses/Inter-OFL.txt`<br>`android/licenses/JetBrainsMono-OFL.txt`<br>`android/licenses/Outfit-OFL.txt` |
| `android-app/licenses/JetBrainsMono-OFL.txt` | `android/licenses/JetBrainsMono-OFL.txt` | `android/licenses/Inter-OFL.txt`<br>`android/licenses/JetBrainsMono-OFL.txt`<br>`android/licenses/Outfit-OFL.txt` |
| `android-app/licenses/Lucide-ISC.txt` | `android/licenses/Lucide-ISC.txt` | `android/licenses/Lucide-ISC.txt` |
| `android-app/licenses/Outfit-OFL.txt` | `android/licenses/Outfit-OFL.txt` | `android/licenses/Inter-OFL.txt`<br>`android/licenses/JetBrainsMono-OFL.txt`<br>`android/licenses/Outfit-OFL.txt` |
| `android-app/licenses/React-MIT.txt` | `android/licenses/React-MIT.txt` | `android/licenses/React-MIT.txt` |
| `android-app/src/main.jsx` | `android/src/main.jsx` | `android/src/main.jsx` |
| `android-app/src/App.jsx` | `android/src/App.jsx` | `android/src/App.jsx` |
| `android-app/src/styles.mjs` | `android/src/styles.mjs` | `android/src/styles.mjs` |
| `android-app/src/mobile.css` | `android/src/mobile.css` | `android/src/mobile.css` |
| `android-app/src/ui-refresh.css` | `android/src/ui-refresh.css` | `android/src/ui-refresh.css` |
| `android-app/tests/branding.test.mjs` | `android/tests/branding.test.mjs` | `android/tests/branding.test.mjs` |
| `android-app/tests/keyboard.test.mjs` | `android/tests/keyboard.test.mjs` | `android/tests/keyboard.test.mjs` |
| `android-app/tests/harness.jsx` | `android/tests/harness.jsx` | `android/tests/harness.jsx` |
| `android-app/tests/browser.mjs` | `android/tests/browser.mjs` | `android/tests/browser.mjs` |
| `android-app/tests/auth.test.mjs` | `android/tests/auth.test.mjs` | `android/tests/auth.test.mjs` |
| `android-app/tests/https-transport.test.mjs` | `android/tests/https-transport.test.mjs` | `android/tests/https-transport.test.mjs` |
| `android-app/tests/harness.html` | `android/tests/harness.html` | `android/tests/harness.html` |
| `android-app/tests/live-contract.test.mjs` | `android/tests/live-contract.test.mjs` | `android/tests/live-contract.test.mjs` |
| `android-app/tests/vault-queue.test.mjs` | `android/tests/vault-queue.test.mjs` | `android/tests/vault-queue.test.mjs` |
| `android-app/tests/isolation.test.mjs` | `android/tests/isolation.test.mjs` | `android/tests/isolation.test.mjs` |
| `android-app/android/app/.gitignore` | `android/android/app/.gitignore` | `android/android/app/.gitignore` |
| `android-app/android/app/proguard-rules.pro` | `android/android/app/proguard-rules.pro` | `android/android/app/proguard-rules.pro` |
| `android-app/android/app/capacitor.build.gradle` | `android/android/app/capacitor.build.gradle` | `android/android/app/capacitor.build.gradle` |
| `android-app/android/app/build.gradle` | `android/android/app/build.gradle` | `android/android/app/build.gradle` |
| `android-app/android/capacitor-cordova-android-plugins/cordova.variables.gradle` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/268844885a8d/android/capacitor-cordova-android-plugins/cordova.variables.gradle` |
| `android-app/android/capacitor-cordova-android-plugins/build.gradle` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/8f5cea7b5466/android/capacitor-cordova-android-plugins/build.gradle` |
| `android-app/android/app/src/main/AndroidManifest.xml` | `android/android/app/src/main/AndroidManifest.xml` | `android/android/app/src/main/AndroidManifest.xml` |
| `android-app/android/app/src/test/java/com/getcapacitor/myapp/ExampleUnitTest.java` | `android/android/app/src/test/java/com/getcapacitor/myapp/ExampleUnitTest.java` | `android/android/app/src/test/java/com/getcapacitor/myapp/ExampleUnitTest.java` |
| `android-app/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java` |
| `android-app/android/app/src/androidTest/java/com/nemesis/panel/dev/KeystoreSessionStoreInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/nemesis/panel/dev/KeystoreSessionStoreInstrumentedTest.java` | `android/android/app/src/androidTest/java/com/nemesis/panel/dev/KeystoreSessionStoreInstrumentedTest.java` |
| `android-app/android/app/src/main/res/drawable-land-xxhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xxhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xxhdpi/splash.png` |
| `android-app/android/app/src/main/res/drawable-land-xxxhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xxxhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xxxhdpi/splash.png` |
| `android-app/android/app/src/main/res/drawable-port-hdpi/splash.png` | `android/android/app/src/main/res/drawable-port-hdpi/splash.png` | `android/android/app/src/main/res/drawable-port-hdpi/splash.png` |
| `android-app/android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png` |
| `android-app/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` |
| `android-app/android/app/src/main/res/mipmap-xhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xhdpi/ic_launcher_foreground.png` |
| `android-app/android/app/src/main/res/drawable-land-mdpi/splash.png` | `android/android/app/src/main/res/drawable-land-mdpi/splash.png` | `android/android/app/src/main/res/drawable-land-mdpi/splash.png`<br>`android/android/app/src/main/res/drawable/splash.png` |
| `android-app/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` | `android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` | `android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`<br>`android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` |
| `android-app/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` | `android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` | `android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`<br>`android/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` |
| `android-app/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png` |
| `android-app/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` |
| `android-app/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png` |
| `android-app/android/app/src/main/res/drawable-land-xhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xhdpi/splash.png` | `android/android/app/src/main/res/drawable-land-xhdpi/splash.png` |
| `android-app/android/app/src/main/res/layout/activity_main.xml` | `android/android/app/src/main/res/layout/activity_main.xml` | `android/android/app/src/main/res/layout/activity_main.xml` |
| `android-app/android/app/src/main/res/drawable-port-mdpi/splash.png` | `android/android/app/src/main/res/drawable-port-mdpi/splash.png` | `android/android/app/src/main/res/drawable-port-mdpi/splash.png` |
| `android-app/android/app/src/main/res/drawable/ic_launcher_background.xml` | `android/android/app/src/main/res/drawable/ic_launcher_background.xml` | `android/android/app/src/main/res/drawable/ic_launcher_background.xml` |
| `android-app/android/app/src/main/res/drawable/splash.png` | `android/android/app/src/main/res/drawable/splash.png` | `android/android/app/src/main/res/drawable-land-mdpi/splash.png`<br>`android/android/app/src/main/res/drawable/splash.png` |
| `android-app/android/app/src/main/res/drawable-land-hdpi/splash.png` | `android/android/app/src/main/res/drawable-land-hdpi/splash.png` | `android/android/app/src/main/res/drawable-land-hdpi/splash.png` |
| `android-app/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png` |
| `android-app/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` |
| `android-app/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_foreground.png` |
| `android-app/android/app/src/main/res/values-v35/styles.xml` | `android/android/app/src/main/res/values-v35/styles.xml` | `android/android/app/src/main/res/values-v35/styles.xml` |
| `android-app/android/app/src/main/res/drawable-port-xxxhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xxxhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xxxhdpi/splash.png` |
| `android-app/android/app/src/main/res/drawable-port-xxhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xxhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xxhdpi/splash.png` |
| `android-app/android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png` |
| `android-app/android/app/src/main/res/mipmap-hdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher.png` |
| `android-app/android/app/src/main/res/mipmap-hdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-hdpi/ic_launcher_foreground.png` |
| `android-app/android/app/src/main/res/drawable-port-xhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xhdpi/splash.png` | `android/android/app/src/main/res/drawable-port-xhdpi/splash.png` |
| `android-app/android/app/src/main/res/xml/config.xml` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/e9dcda493e66/android/app/src/main/res/xml/config.xml` |
| `android-app/android/app/src/main/res/xml/data_extraction_rules.xml` | `android/android/app/src/main/res/xml/data_extraction_rules.xml` | `android/android/app/src/main/res/xml/data_extraction_rules.xml` |
| `android-app/android/app/src/main/res/xml/backup_rules.xml` | `android/android/app/src/main/res/xml/backup_rules.xml` | `android/android/app/src/main/res/xml/backup_rules.xml` |
| `android-app/android/app/src/main/res/xml/file_paths.xml` | `android/android/app/src/main/res/xml/file_paths.xml` | `android/android/app/src/main/res/xml/file_paths.xml` |
| `android-app/android/app/src/main/res/values/ic_launcher_background.xml` | `android/android/app/src/main/res/values/ic_launcher_background.xml` | `android/android/app/src/main/res/values/ic_launcher_background.xml` |
| `android-app/android/app/src/main/res/values/styles.xml` | `android/android/app/src/main/res/values/styles.xml` | `android/android/app/src/main/res/values/styles.xml` |
| `android-app/android/app/src/main/res/values/strings.xml` | `android/android/app/src/main/res/values/strings.xml` | `android/android/app/src/main/res/values/strings.xml` |
| `android-app/android/app/src/main/res/drawable-v24/ic_launcher_foreground.xml` | `android/android/app/src/main/res/drawable-v24/ic_launcher_foreground.xml` | `android/android/app/src/main/res/drawable-v24/ic_launcher_foreground.xml` |
| `android-app/android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png` |
| `android-app/android/app/src/main/res/mipmap-mdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher.png` |
| `android-app/android/app/src/main/res/mipmap-mdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher_foreground.png` | `android/android/app/src/main/res/mipmap-mdpi/ic_launcher_foreground.png` |
| `android-app/android/app/src/main/java/com/nemesis/panel/dev/SecureSessionPlugin.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/SecureSessionPlugin.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/SecureSessionPlugin.java` |
| `android-app/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/MainActivity.java` |
| `android-app/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` | `android/android/app/src/main/java/com/nemesis/panel/dev/KeystoreSessionStore.java` |
| `android-app/android/gradle/wrapper/gradle-wrapper.properties` | `android/android/gradle/wrapper/gradle-wrapper.properties` | `android/android/gradle/wrapper/gradle-wrapper.properties` |
| `android-app/android/gradle/wrapper/gradle-wrapper.jar` | `android/android/gradle/wrapper/gradle-wrapper.jar` | `android/android/gradle/wrapper/gradle-wrapper.jar` |
| `android-app/android/capacitor-cordova-android-plugins/src/main/AndroidManifest.xml` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/2e3e383475f0/android/capacitor-cordova-android-plugins/src/main/AndroidManifest.xml` |
| `android-app/android/capacitor-cordova-android-plugins/src/main/res/.gitkeep` | Excluded from original public import | NOT present as exact bytes; see original exclusion reason and census/redactions |
| `android-app/android/capacitor-cordova-android-plugins/src/main/java/.gitkeep` | Excluded from original public import | NOT present as exact bytes; see original exclusion reason and census/redactions |
| `android-app/src/generated/provenance.json` | `android/src/generated/provenance.json` | `android/src/generated/provenance.json`<br>`legacy/preserved-features/phase1-ui/src/generated/provenance.json` |
| `android-app/src/generated/icons.js` | `android/src/generated/icons.js` | `android/src/generated/icons.js`<br>`legacy/preserved-features/phase1-ui/src/generated/icons.js` |
| `android-app/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx`<br>`legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx` |
| `android-app/src/generated/original.css` | `android/src/generated/original.css` | `android/src/generated/original.css`<br>`legacy/preserved-features/phase1-ui/src/generated/original.css` |
| `android-app/src/branding/BrandLogo.jsx` | `android/src/branding/BrandLogo.jsx` | `android/src/branding/BrandLogo.jsx` |
| `android-app/src/branding/branding.json` | `android/src/branding/branding.json` | `android/src/branding/branding.json` |
| `android-app/src/auth/vault-queue.mjs` | `android/src/auth/vault-queue.mjs` | `android/src/auth/vault-queue.mjs` |
| `android-app/src/auth/api-auth.mjs` | `android/src/auth/api-auth.mjs` | `legacy/phase3-baseline/android/src/auth/api-auth.mjs` |
| `android-app/src/auth/capacitor-transport.mjs` | `android/src/auth/capacitor-transport.mjs` | `android/src/auth/capacitor-transport.mjs` |
| `android-app/src/auth/mock-auth.mjs` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/01ae6b223665/src/auth/mock-auth.mjs`  **SANITIZED ONLY**; exact original remains private, not public |
| `android-app/src/auth/api-contract.mjs` | `android/src/auth/api-contract.mjs` | `android/src/auth/api-contract.mjs` |
| `android-app/src/auth/https-transport.mjs` | `android/src/auth/https-transport.mjs` | `legacy/phase3-baseline/android/src/auth/https-transport.mjs` |
| `android-app/src/auth/secure-session.mjs` | `android/src/auth/secure-session.mjs` | `android/src/auth/secure-session.mjs` |
| `android-app/src/components/Settings.jsx` | `android/src/components/Settings.jsx` | `legacy/phase3-baseline/android/src/components/Settings.jsx` |
| `android-app/src/components/Pages.jsx` | `android/src/components/Pages.jsx` | `android/src/components/Pages.jsx` |
| `android-app/src/components/Icon.jsx` | `android/src/components/Icon.jsx` | `android/src/components/Icon.jsx` |
| `android-app/src/components/Auth.jsx` | `android/src/components/Auth.jsx` | `android/src/components/Auth.jsx` |
| `android-app/tests/fixtures/phase1-browser.mjs` | Excluded from original public import | NOT present as exact bytes; see original exclusion reason and census/redactions |
| `android-app/tests/fixtures/legacy-mock-auth.mjs` | Excluded from original public import | `legacy/preserved-features/checkpoint-code/01ae6b223665/src/auth/mock-auth.mjs`  **SANITIZED ONLY**; exact original remains private, not public |
| `android-app/tests/fixtures/phase1-auth.test.mjs` | Excluded from original public import | NOT present as exact bytes; see original exclusion reason and census/redactions |
| `android-app/tests/fixtures/schema.mjs` | `android/tests/fixtures/schema.mjs` | `android/tests/fixtures/schema.mjs` |
| `backend-export/backend/auth_api.py` | `backend/auth_api.py` | `legacy/backend-baseline/auth_api.py` |
| `backend-export/backend/registration_api.py` | `backend/registration_api.py` | `backend/registration_api.py` |
| `backend-export/backend/firebase_pool.py` | `backend/firebase_pool.py` | `legacy/phase3-baseline/backend/firebase_pool.py` |
| `backend-export/backend/telegram_bot.py` | `backend/telegram_bot.py` | `legacy/phase3-baseline/backend/telegram_bot.py` |
| `backend-export/backend/registration_store.py` | `backend/registration_store.py` | `backend/registration_store.py` |
| `backend-export/backend/account_store.py` | `backend/account_store.py` | `backend/account_store.py` |
| `backend-export/backend/firebase_api.py` | `backend/firebase_api.py` | `legacy/phase3-baseline/backend/firebase_api.py` |
| `backend-export/backend/firebase_cli.py` | `backend/firebase_cli.py` | `legacy/phase3-baseline/backend/firebase_cli.py` |
| `backend-export/backend/main.py` | `backend/main.py` | `legacy/phase3-baseline/backend/main.py` |
| `backend-export/backend/telegram_link.py` | `backend/telegram_link.py` | `backend/telegram_link.py` |
| `checkpoints/00-phase1-baseline.zip!android-app/src/mobile.css` | `legacy/preserved-features/phase1-ui/src/mobile.css` | `legacy/preserved-features/phase1-ui/src/mobile.css` |
| `checkpoints/00-phase1-baseline.zip!android-app/src/generated/provenance.json` | `legacy/preserved-features/phase1-ui/src/generated/provenance.json` | `android/src/generated/provenance.json`<br>`legacy/preserved-features/phase1-ui/src/generated/provenance.json` |
| `checkpoints/00-phase1-baseline.zip!android-app/src/generated/icons.js` | `legacy/preserved-features/phase1-ui/src/generated/icons.js` | `android/src/generated/icons.js`<br>`legacy/preserved-features/phase1-ui/src/generated/icons.js` |
| `checkpoints/00-phase1-baseline.zip!android-app/src/generated/OriginalUI.jsx` | `legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx` | `android/src/generated/OriginalUI.jsx`<br>`legacy/preserved-features/phase1-ui/src/generated/OriginalUI.jsx` |
| `checkpoints/00-phase1-baseline.zip!android-app/src/generated/original.css` | `legacy/preserved-features/phase1-ui/src/generated/original.css` | `android/src/generated/original.css`<br>`legacy/preserved-features/phase1-ui/src/generated/original.css` |

## Recoveries, exclusions and remaining missing implementations

- Recovered **36** previously untracked first-party code/config variants into `legacy/preserved-features/checkpoint-code/`. **35 are byte-identical** to available sources; one mock-auth variant retains its algorithm with fixed demonstration credential literals redacted. Its original SHA-256, sanitized SHA-256, and original archive locations are recorded. The untouched original remains in private checkpoints, not public Git. No original website handler was recovered by this process.
- Recovered history includes phase-one/Step22/Step23 App/Auth/Settings, auth transport/contract/mock adapter, theme/mobile styles, earlier Java MainActivity/styles, wrappers/build configuration and the approved UI proposal. These are inactive, nonassembled source variants, not runnable restoration bundles. Imports/assets may point to absent sibling versions; use the provenance index to assemble a reviewed historical tree privately.
- Existing `legacy/preserved-features/phase1-ui` and `legacy/phase3-baseline` bytes are unchanged. Phase3 baselines preserve previous Android API/Settings and exported Firebase/bot modules; they contain no missing original HTML business logic. `legacy/backend-baseline/auth_api.py` preserves the original OTP verifier.
- Missing: original website Firebase REST/storage helpers; account connect/bulk/share/merge/delete implementations; JSZip APK parsing; original Telegram notification/document/report routines; SMS/financial parsers; device card/copy/drawer components; device/message polling; saved-device persistence; device deletion/send-SMS handlers; channel gate and anti-inspection code; original root navigation/theme-widget JS; complete independent HTML/backup/deployment source. Some surrounding render expressions survive as listed above.
- Also unavailable: original editable website repository/source maps, any original native child-device app and builder implementation. Password-change/history/security-management APIs are not in the backend export; do not label those planned requirements recovered original features.
- The six archived checkpoint containers remain private/local; their per-entry metadata is public evidence, not a claim that every binary/generated output/test/log/asset was republished. Dependencies, generated bundles, APKs/signing material, native packaged assets and test fixtures were not imported by this code recovery. No unreviewed monitoring implementation or secret-bearing raw website was added to public Git.

## Validation and restoration instructions

- Verified all ten original backend module checksums and 49 exported function definitions against exact retained copies.
- Recovery integrity checks compare available source bytes/public hashes; current working Android/backend/site/legacy source remains identical to audit base. The audit changes only documentation and new inactive legacy copies. No app build, service restart, Firebase call or Telegram message is needed for this documentation/source-only change.
- Staged-file source/secret audit and Gitleaks results are recorded in [VALIDATION.json](original-feature-code-audit/VALIDATION.json). Six archive checksums, 92 source variants, ten backend modules and 15 recovered JavaScript/JSX syntax checks passed. Exact recovery preserves two original trailing-whitespace lines in config.xml; diff whitespace checking reports these inherited lines. No app/backend runtime suite was rerun because active code is unchanged. Existing historical checksum false positives are explicitly distinguished from actual credentials. These scans do not establish feature completeness.
- To resolve missing implementations, recover the exact five original attachments (prefer matching recorded hashes), the original editable website project if it exists, and any original child-device archive. Review privately for credentials/customer data before public preservation. Preserve untouched originals in protected owner storage and publish sanitized, explicitly inactive copies with before/after digests. Do not execute recovered handlers or overwrite active authentication/manager modules.
- `docs/FEATURE_STATUS.md` is a historical import inventory: its OTP PARTIAL/xfail row is superseded by the OTP patch, and its two aggregate “original controls” rows do not establish code parity. `docs/ORIGINAL_SOURCE_MANIFEST.md` describes import-time provenance; “module bytes unchanged” applies to retained baselines after reviewed patches, not all current backend paths. Earlier checklist “source retained” statements relied on then-available attachments and are not proof those bytes remain available today. This audit corrects the interpretation without rewriting baseline documents.

**Conclusion:** exported backend implementations are accounted for; available Android checkpoint code is now mapped and recovered, subject to the documented mock redaction. Full preservation of the original website features is **not achieved** because the original operational implementations and three child renderers are not recoverable from the available inputs. No original feature has been activated by this audit.
