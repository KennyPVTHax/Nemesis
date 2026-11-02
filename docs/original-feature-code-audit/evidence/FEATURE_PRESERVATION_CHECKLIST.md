Current Android 0.3.0 comparison: [FEATURE_INTEGRATION_CHECKLIST.md](ui-refresh/FEATURE_INTEGRATION_CHECKLIST.md). The inventory below is retained as the original discovery record.

# Feature preservation checklist

All original source files are preserved unchanged. UI reuse and executable integration are separate statuses. No production feature parity is claimed. No feature is classified as disposable search functionality. The development app intentionally cannot access customer data.

| Existing/new feature | Android disposition |
|---|---|
| Brand/title, original logos, iconography | Reuse original markup and icon definitions |
| Tailwind utilities and dark card/layout styling | Copy original CSS |
| Four themes and local theme persistence | Reuse theme CSS; local selection |
| Animated stars, blobs, fog and snowflakes | Reuse original decoration |
| Telegram support link | Preserve link; explicit external navigation |
| Telegram channel join gate | Inventory retained; authentication replacement proposal |
| Anti-inspection shortcuts, frame-buster, debugger trap | Inventory retained; incompatible with hybrid dev inspection; proposal |
| Local Firebase account list and saved config | Original chooser UI retained offline; no secrets accepted for storage |
| Add Firebase account and URL/key form | Original form retained offline; privileged key flow blocked |
| Multiple database URLs / bulk connect | UI retained offline; backend approval needed |
| Connect existing account | Offline adapter blocks live access |
| Delete saved account | No real configs loaded; backend/settings approval needed |
| Single-account share / copy / decode | Credential-bearing links blocked; proposal |
| Multi-select accounts / merged dashboard / merged sharing | Original empty UI retained; backend approval needed |
| APK upload / drag/drop / ZIP inspection | Original form retained; upload not sent or processed |
| APK Firebase URL/key/project/package extraction / copy | Source retained; integration pending secure authorized design |
| Telegram APK upload and parse notifications | Not executed; sends uploaded files / credentials |
| Automatic credential/device Telegram reports | Not executed; sends database credentials |
| Dashboard original header, status cards and empty state | Reuse original React render code |
| Total / online / offline / bank SMS / card counts | Original empty UI; no customer records or invented stats |
| Device name / number / ID search | Original search input and state retained |
| All / online / offline / saved / UPI / bank / card filters | Original controls retained offline |
| Newest / oldest / name / battery sort | Original controls retained offline |
| Manual refresh and loading/error/toast states | Original UI; explicit offline blocker on refresh |
| Auto refresh devices at 15s / analysis at 45s | Not connected in mock sessions |
| Saved-device star / local persistence | Source retained; no devices loaded |
| Device cards, model / ID / Android / battery / SIM / network | Source retained; no customer device cards rendered |
| Phone / bank / field copy controls | Source retained; requires real authorized data |
| Online/offline and last-seen timestamps | Source retained; no invented activity |
| SMS Searcher modal and query / clear / close | Original markup reused; empty results only |
| Cross-device SMS search and loading progress | Source retained; authenticated integration pending |
| Device drawer and Info tab | Source retained; no real devices available |
| SMS message list / sender / dates / content | Source retained; consent-aware backend pending |
| Bank balance / transaction extraction and Bank tab | Not activated; sensitive-data feature outside authorized monitoring |
| Card / expiry / CVV extraction and reveal | Not activated; sensitive-data feature outside authorized monitoring |
| UPI PIN display / Auto Token tab | Not activated; sensitive-data feature outside authorized monitoring |
| Send SMS form / SIM choice / queued webhook command | Not connected; authenticated scoped backend and consent needed |
| Delete-device command and confirmation | Not connected; server authorization needed |
| Existing logout to account chooser | New development logout clears mock auth and returns login |
| Surge hostname / SPA fallback / ignore configuration | Original preserved; not packaged as Android deployment config |
| Login ID → password → Telegram OTP | New offline mock interfaces; no Telegram request |
| Settings account / password / activity / sessions / Telegram / 2SV | New truthful disconnected UI; real backend unavailable |
| Exactly four primary application tabs | New APK Management / Monitoring / Future / Settings |

Complete discovered literal labels are listed in SOURCE_UI_LABELS.json. Original nonpackaged functional code remains in the supplied files, with hashes recorded in SOURCE_MANIFEST.json.
