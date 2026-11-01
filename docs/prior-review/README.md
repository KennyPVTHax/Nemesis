# NEMESIS — source preservation

This repository is the intended source-control home for the NEMESIS Android app, website, FastAPI API and Telegram registration/authentication bridge.

**Import status: INITIALIZED — SOURCE NOT YET IMPORTED.** No Android, website, API or bot source has been uploaded from the VPS or source archives at this point. Do not interpret these preservation documents as evidence that feature implementations have been backed up.

## Preservation policy

- The running website must remain functional and independent from the Android app.
- Do not delete original features, controls, bindings, or workflows merely because they have not been migrated.
- Record each actual feature and its original file location in `docs/FEATURE_INVENTORY.md` after examining the original source.
- Preserve untouched source snapshots in a restricted archival location before modifying code; include SHA-256 manifests. Avoid committing secrets, user content, APKs or service credentials.
- Inactive yet implemented functions should use **explicitly false feature flags** or build exclusions; retain their source and test coverage when appropriate. A code comment is *not* a security boundary.
- Never make an unsupported component active merely because it appears in archived source. Review authorization, consent, security and functionality first.
- Require a pull request and an inventory update for any intentional behavior change.

## Security notice

**This repository is currently public.** A GitHub account that is not advertised does not make its public repositories confidential. Do not commit Telegram bot tokens, Firebase admin keys, user/customer databases, HMAC secrets, signing keys, password material, logs, personal data, or sensitive device content. `.gitignore` is only a safety net, not proof a commit is safe.

Recommended: make the repository private **before importing project source**; use local encrypted backups for the full untouched archive. If credentials have ever been committed to a public repository, remove/rewrite exposed history and rotate them.

## Next import stage

1. Back up the current VPS and original Android/website archives privately.
2. Run a source-only inventory and secret scan; inspect its findings.
3. Import clean app/backend/website source on a review branch.
4. Audit preserved legacy features against the original.
5. Validate reproducible build, auth/OTP, and website regressions before merge.

See [feature inventory](docs/FEATURE_INVENTORY.md) and [import checklist](docs/SOURCE_IMPORT_CHECKLIST.md).
