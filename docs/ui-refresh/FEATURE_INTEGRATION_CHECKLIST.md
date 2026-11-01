Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# Preserved-feature comparison — 0.3.0

| Feature | Current result |
|---|---|
| Existing project | Updated in place; prior source/APK archives remain intact |
| Original supplied website / production services | No modification, deployment or publication |
| Extracted original dashboard and APK/account UI | Original JSX/CSS/icons/provenance byte-for-byte unchanged; scoped visual overlay only |
| Dashboard filters, navigation, buttons, SMS modal, animations | Retained; browser search/modal/Back checks passed |
| Monitoring/customer data integration | Still disconnected, as in Step 22; no invented data or new collector |
| APK/Firebase interface and reserved builder | Preserved; backend integration and child-APK builder remain outside this build |
| Four primary tabs | Exactly APK Management, Monitoring, Future, Settings |
| Future | Reserved placeholder; no invented functionality |
| Login/Telegram OTP | Enabled, exact production route/response mappings, no mock fallback |
| Password visibility/errors/loading | Preserved and restyled with comfortable controls |
| Account expiry | Nullable owner expiry and finite customer expiry correctly handled |
| Account details / refresh | Real `/auth/me` fields only; session expiry separate from account expiry |
| Logout / revocation | Real bearer endpoint, secure local erasure, honest failure notice |
| Saved Android session | New owner-requested Keystore-backed encryption; server revalidation required on restore |
| Change password, history, active-session list, Telegram linking, 2SV settings | Existing sections retained as expandable descriptions; operations remain unavailable because no corresponding API contract was supplied |
| Themes | All four original theme choices retained |
| Keyboard, safe areas, Back | Existing single-owner resize fix retained; no additional IME margins/height hacks |
| Logo | Owner-authorized generated crimson N replaces prior crop in current branding; original supplied JPG remains unchanged |
| Launcher/adaptive icons/splash | Density-correct new mark; existing splash references updated foreground assets |

The owner approved the proposed visual direction and requested a new self-designed logo and APK, then supplied the exact production auth response contract and requested secure Android session storage. These authorize the changes above. There is no further design-approval gate for this build.

The preservation comparison is against the already delivered Step 22 app, not a claim that every disconnected feature in the original website is newly operational. Firebase/APK-building and monitoring integrations remain outside the owner's narrowed build scope. Historical feature inventories are retained in `../FEATURE_PRESERVATION_CHECKLIST.md` and `../phase2/PRESERVED_FEATURE_COMPARISON.md`.
