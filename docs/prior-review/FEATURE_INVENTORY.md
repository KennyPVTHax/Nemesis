# NEMESIS feature inventory

> **Status: provisional project requirements, NOT a source audit.**
> The original website/Android archives and the running VPS source must be reviewed before any item can be confirmed as present or preserved.

| Area | Expected behavior | Source location | State | Verification |
|---|---|---|---|---|
| Authentication | Login ID + password | TBD | Reported working; source not imported | Android end-to-end reported |
| Authentication | Telegram six-digit OTP | TBD | Reported working; source not imported | Android end-to-end reported |
| Accounts | Customer key redemption and registration | TBD | Reported working; source not imported | Backend/customer test reported |
| Accounts | 30-day customer access; owner unlimited | TBD | Expected, source not audited | Pending automated test |
| Android | Four-tab navigation: builder, monitoring, placeholder, settings | TBD | Expected; source not imported | Pending UI regression |
| Android | Keyboard resizing avoids black screen | TBD | Expected; source not imported | Pending physical-device visual check |
| Website | Original monitoring UI/features unchanged | TBD | Source not imported | Pending source comparison |
| Firebase | Owner-assigned per-customer database | TBD | Planned/not verified | Pending allocation tests |
| Firebase | Customer may request Firebase URL with owner approval | TBD | Planned/not verified | Pending authorization tests |
| Firebase | Bring-your-own Firebase option | TBD | Planned/not verified | Pending integration |
| Build | Customer APK/Firebase configuration workflow | TBD | Planned/not verified | Pending build test |
| Settings | Account/session and logout controls | TBD | Source not imported | Pending UI test |

## Audit procedure

For each **actual** feature in the original sources, add:
- Stable feature ID, entry point, dependent files, and screen/API route
- Whether original implementation is retained byte-for-byte, migrated, or awaiting review
- Exact feature flag/build condition when disabled
- Security/permission considerations and a functional regression test
- Commit hash or archived SHA-256 source snapshot

**Do not classify a feature as 'preserved' until its code or verifiable archived snapshot exists.** Do not reconstruct features from memory if original code is available.
