# Existing project analysis

Inspected 2026-10-29. All five supplied files were read in full with local structural searches; no production endpoints were contacted. See SOURCE_MANIFEST.json for exact paths, byte counts and original SHA-256 hashes. No project archive, backend repository, database rules, native child app, source map, package manifest or build configuration was supplied. The workspace had no existing application or AGENTS.md.

## Inputs and architecture

- `4-index.html`: authoritative NEMESIS PANEL single-page app, 21,200 lines, inline compiled React/React DOM runtime, JSX-runtime calls, Lucide icon definitions, JSZip and application code. No editable JSX/component source was supplied.
- `2-200.html`: byte-identical to index; Surge SPA fallback.
- `5-index.html.bak`: earlier Devil Panel, 20,497 lines. Compared completely against current index: current adds anti-inspection behavior, NEMESIS branding, four themes, copy controls, additional number display and SMS search changes. The earlier functional modules remain in current source. Backup is retained at its input path.
- `1-surgeignore`: ignores *.bak, *.log and .git.
- `3-CNAME`: Surge host configuration. No evidence that customer SMS search is disposable testing code; it must be retained.
- Styling: inline compiled Tailwind utility CSS, custom HSL theme variables, Outfit / Inter / JetBrains Mono Google Fonts, animated stars, fog, gradient blobs, snowflake/logo animations, rounded dark cards and crimson buttons. Themes: Crimson Hellfire, Cyber Amethyst, Toxic Emerald, Solar Gold.
- Original build tool is not supplied. Module-preload shim suggests a bundled frontend; do not infer a confirmed original Vite version. New wrapper uses Vite + React + Capacitor.

## Workflow and navigation

Telegram channel join overlay → local Firebase account chooser → add database URL + secret / inspect APK → test connection → persist account → open single or merged dashboard → filters / sort / SMS search / device drawer → info, bank, cards, SMS, auto-token or send SMS → logout to account chooser. Shared links accept `?s=` single and `?m=` merged configurations. Theme and saved-device controls persist locally. The channel gate is client-side and is not account authentication or Telegram identity verification.

## Integration map

| Code / lines in current index | Responsibility |
|---|---|
| 18109–18120 | Account localStorage loading/saving |
| 18121–18175 | Firebase Realtime Database REST GET, PUT, DELETE using auth query parameter |
| 18177–18196 | Hardcoded Telegram bot configuration and credential/device reporting |
| 18198–18512 | SMS parsing: banks, balances, cards, CVV/expiry, phone/network and UPI-related display |
| 18525–18540 | Reversible credential-bearing share links |
| 18542–18632 | Telegram messages/documents and JSZip APK Firebase configuration inspection |
| 18658–19361 | Account manager, APK upload, extraction, bulk database connect, merge/share/copy/delete |
| 19362–19793 | Battery, financial-data cards, device cards, saved devices and copy controls |
| 19794–20345 | Device detail drawer, SMS list, financial tabs, send-SMS command, delete-device action |
| 20346–21139 | Dashboard, counts, filter/sort/name-number-ID search, SMS search, periodic refresh, reporting |
| 21142–21157 | Root account/dashboard navigation |
| 21162–21198 | Theme widget and persistence |

Firebase paths are `clients`, `messages/{deviceId}`, `clients/{deviceId}/webhookEvent/sendSms` and device deletion under `clients/{deviceId}`. GET device polling is 15 seconds; analysis refresh 45 seconds; detail messages 6 seconds. No Firebase SDK, Firestore, Cloud Functions, server authentication implementation, secure user session, account password API, verified Telegram binding or OTP endpoint was supplied. Backend framework and database access rules are unknown, not proven absent in the user's infrastructure.

## Material blockers

The supplied client embeds a Telegram bot credential and automatically transmits database secrets and APK files to a configured Telegram chat. No values are reproduced here. Financial extraction includes PIN/card/CVV-related functionality, which cannot be activated as transparent family monitoring. The app must not ship privileged credentials or give development mock sessions customer access. Existing files remain untouched; original operations are documented and excluded from execution in the development app. This is an explicit incomplete integration, not a claim of full feature parity. See PENDING_APPROVALS.md.

## Reuse boundaries

Reuse original CSS verbatim, original decorative background, inline icon definitions and original dashboard/account-manager render markup. New offline adapters supply no customer records and no Firebase credentials. Preserve existing labels, empty UI, filters, sort, SMS-search dialog and APK-management forms as a disconnected development preview. No APK builder/repacker or child-device collector is introduced.
