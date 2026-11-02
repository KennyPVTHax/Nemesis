# Button coverage and limits

The isolated component harness ran **55 checks**, with zero runtime errors and zero external requests. These are scenario checks, not a claim that 55 distinct sites were each tested once. Tests use explicitly marked synthetic accounts/devices and a harmless reminder string; fixtures are not imported into the shipped app.

| Executed check | Result |
|---|---|
| device-search: Local fixture name/ID query | PASS |
| filter-online: Selection applied; sensitive categories contain no data | PASS |
| filter-offline: Selection applied; sensitive categories contain no data | PASS |
| filter-upi: Selection applied; sensitive categories contain no data | PASS |
| filter-bank: Selection applied; sensitive categories contain no data | PASS |
| filter-card: Selection applied; sensitive categories contain no data | PASS |
| filter-all: Selection applied; sensitive categories contain no data | PASS |
| sort-old: Local ordering selection | PASS |
| sort-new: Local ordering selection | PASS |
| sort-name: Local ordering selection | PASS |
| sort-battery: Local ordering selection | PASS |
| saved-device: Local toggle affects saved filter without writing source credentials | PASS |
| Refresh dashboard: Responsive review dialog; no backend operation | PASS |
| Telegram support link: Responsive review dialog; no backend operation | PASS |
| Share merged accounts: Responsive review dialog; no backend operation | PASS |
| device-card: Card opens original-purpose details surface | PASS |
| safe-copy: Only the displayed synthetic identifier copied | PASS |
| drawer-Info: Section navigation preserved | PASS |
| drawer-Bank: Section navigation preserved | PASS |
| Refresh bank information: Responsive review dialog; no backend operation | PASS |
| Review financial information: Responsive review dialog; no backend operation | PASS |
| Copy restricted information: Responsive review dialog; no backend operation | PASS |
| drawer-Cards: Section navigation preserved | PASS |
| Refresh card information: Responsive review dialog; no backend operation | PASS |
| Reveal card information: Responsive review dialog; no backend operation | PASS |
| Copy restricted information: Responsive review dialog; no backend operation | PASS |
| drawer-SMS: Section navigation preserved | PASS |
| Refresh messages: Responsive review dialog; no backend operation | PASS |
| drawer-Auto Token: Section navigation preserved | PASS |
| Refresh token information: Responsive review dialog; no backend operation | PASS |
| Review financial information: Responsive review dialog; no backend operation | PASS |
| Copy restricted information: Responsive review dialog; no backend operation | PASS |
| drawer-Send SMS: Section navigation preserved | PASS |
| Use device number: Responsive review dialog; no backend operation | PASS |
| Send SMS: Responsive review dialog; no backend operation | PASS |
| sms-draft: SIM/recipient/message state works; submission cannot send | PASS |
| Copy restricted information: Responsive review dialog; no backend operation | PASS |
| Delete device: Responsive review dialog; no backend operation | PASS |
| drawer-back: Android-style Back closes drawer after review overlay dismissal | PASS |
| sms-search: Open/query/clear/close over isolated harmless fixture | PASS |
| Open merged accounts: Responsive review dialog; no backend operation | PASS |
| Legacy Firebase operation: Responsive review dialog; no backend operation | PASS |
| Copy connection link: Responsive review dialog; no backend operation | PASS |
| account-select-share-merge: Selection and share surface respond; no connection or credential link generated | PASS |
| Delete saved account — confirmation required: Responsive review dialog; no backend operation | PASS |
| Connect Firebase account: Responsive review dialog; no backend operation | PASS |
| APK inspection: Responsive review dialog; no backend operation | PASS |
| APK drop inspection: Responsive review dialog; no backend operation | PASS |
| Legacy Firebase operation: Responsive review dialog; no backend operation | PASS |
| account-form: Form/back/file chooser/unsupported connection all respond truthfully | PASS |
| cancel-account: Cancel returns to account list without saving credentials | PASS |
| viewport-320: No horizontal overflow | PASS |
| viewport-800: No horizontal overflow | PASS |
| dashboard-logout: Existing logout binding invoked; full auth suite checks server revocation | PASS |
| network-isolation: Zero external requests or runtime errors | PASS |

## Per-control evidence

| Matrix control | Coverage / limitation |
|---|---|
| ORIG-001: Copy information | SOURCE/SHARED HANDLER CHECKED; original APK-result/error display branch is conditional and was not fabricated/executed. |
| ORIG-002: Open saved account | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-003: Select account for merge | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-004: Share connection link | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-005: Delete saved account | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-006: Select/deselect all accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-007: Open merged accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-008: Share selected accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-009: New Account | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-010: Back to saved accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-011: APK drop zone | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-012: APK file chooser | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-013: Close APK error/result | SOURCE/SHARED HANDLER CHECKED; original APK-result/error display branch is conditional and was not fabricated/executed. |
| ORIG-014: Reset APK result | SOURCE/SHARED HANDLER CHECKED; original APK-result/error display branch is conditional and was not fabricated/executed. |
| ORIG-015: Database URL input | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-016: Database credential input | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-017: Add accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-018: Cancel account form | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-019: Share dialog backdrop | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-020: Share dialog event containment | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-021: Close connection link | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-022: Copy connection link | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-023: Reveal card information | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-024: Open device card | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-025: Save/unsave device | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-026: Open device details | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-027: Drawer backdrop | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-028: Drawer event containment | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-029: Delete device | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-030: Close drawer | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-1: Info | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-2: Bank | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-3: Cards | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-4: SMS | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-5: Auto Token | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-031-6: Send SMS | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-032: Refresh bank information | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-033: Refresh card information | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-034: Refresh messages | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-035: Copy bank token-labelled information | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-036: Copy card-labelled information | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-037-1: SIM 1 | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-037-2: SIM 2 | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-038: Recipient input | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-039: Message input | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-040: Send SMS | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-041: Use device number | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-042: Dismiss dashboard error | SOURCE/SHARED HANDLER CHECKED; original APK-result/error display branch is conditional and was not fabricated/executed. |
| ORIG-043: Device search | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-044: Dashboard logout | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-045: Share merged accounts | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-046: Telegram support | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-1: all | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-2: online | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-3: offline | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-4: saved | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-5: upi | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-6: bank | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-047-7: card | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-048: Open SMS search | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-049-1: Newest | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-049-2: Oldest | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-049-3: Name | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-049-4: Battery | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-050: Refresh dashboard | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-051: SMS search backdrop | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-052: SMS search event containment | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-053: Close SMS search | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-054: SMS search query | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| ORIG-055: Clear SMS search | COMPONENT SCENARIO / shared state handler verified; exact contextual cases listed above. Overlay containment/closers share tested handlers; not every backdrop coordinate was clicked. |
| WEB-GATE-70: Join Channel | STATIC ONLY: website-only gate intentionally not inserted into working Android authentication. |
| WEB-GATE-71: Continue after channel click | STATIC ONLY: website-only gate intentionally not inserted into working Android authentication. |
| APP-001: Login ID field | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-002: Password field | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-003: Show/hide password | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-004: Sign in | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-005: Six-digit OTP entry | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-006: Verify code | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-007: Restart login / Request another code | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-008: Refresh account | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-009: Settings logout | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-010: Check Firebase status | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-011: Request Firebase Link | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-012: View approved Firebase link | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-013: Application information | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-014: Close app | SOURCE PRESERVED; native exit prompt requires an actual Android device and was not executed. |
| APP-015: Stay here | SOURCE PRESERVED; native exit prompt requires an actual Android device and was not executed. |
| APP-016: APK Management | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-017: Monitoring | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-018: Future | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-019: Settings | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-020: Crimson | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-021: Amethyst | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-022: Emerald | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-023: Gold | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-024: Change password | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-025: Login activity history | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-026: Active sessions | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-027: Telegram account connection | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |
| APP-028: Two-step verification | EXISTING AUTH/API TESTS + FULL-APP BROWSER SCENARIOS; server responses intercepted and synthetic. |

No physical Android device was attached. Native IME, clipboard authorization on real devices, physical Back and actual authenticated production responses remain device/operator verification work. Browser tests simulate short viewports and panel:back; they do not prove native IME behavior. The keyboard/Keystore/branding/native/auth sources are byte-identical to the reviewed baseline. Original palettes/CSS/icons remain intact. The safe restored views reuse the panel design language; they do not import original privileged business logic.

No APK parse succeeded in tests: file selection and drop use harmless synthetic bytes and are ignored by the app. No successful credential share, financial retrieval, SMS send or deletion was simulated. Disabled operations only report unavailable/review status. No original website-only channel gate or customer-facing Firebase administrator controls were inserted.
