# Source import gate

## Prior to public push

- [ ] Confirm owner has approved public release of all source included. Strongly prefer a private repository first.
- [ ] Preserve an encrypted, off-server full backup with checksums before changing files.
- [ ] Identify original Android/website archives and the live VPS source paths.
- [ ] Exclude all runtime databases, customer data, logs, tokens, private certificates, signing keys, build outputs, and cache directories.
- [ ] Inspect filenames AND content for secrets, hardcoded Firebase URLs, tokens and customer/device information. Check history too.
- [ ] Never use `git add -f` to override ignored secret files without review.
- [ ] Compare source manifests and original features; document differences and disabled feature flags.
- [ ] Push initial imports to a review branch and inspect the complete staged diff.
- [ ] Run tests for website independence, APK auth/OTP, backend auth/session, customer registration, and Firebase authorization before merge.

## Inactive feature rules

Commenting out code does not enforce permission boundaries. Prefer an explicit `false` feature flag for incomplete UI features, or exclude modules from the production build. Keep original implementations in history or in clearly marked retained legacy source when safe. Do not deploy unfinished privileged endpoints.

## Deployment

Do not deploy directly from the public GitHub branch to the production VPS without code review, deterministic dependencies, secrets injection, a working rollback and a verified database backup.
