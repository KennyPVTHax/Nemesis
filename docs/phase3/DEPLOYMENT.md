# Prepared Ubuntu VPS installation and rollback

**Not executed on the VPS.** No service restart, Cloud provisioning, credential change or PR merge occurred in this development run. This tool is prepared for `/opt/nemesis/backend`, `/opt/nemesis/.venv`, `nemesis-api.service`, `nemesis-telegram.service` and existing Nginx HTTPS. Nginx and existing environment files are not edited.

The operator must verify the actual unit working directories and executables, service users/groups, baseline source hashes, database path and direct or HTTPS API health URL before approval. The tool checks both units' WorkingDirectory and ExecStart match the expected backend/venv. Unexpected production revisions (including the older vulnerable OTP verifier) are refused, not overwritten. Source/API configuration that differs from this reviewed baseline needs a separate diff review; do not bypass checks. No nano/vim editing is required.

Use a trusted root-controlled checkout of this feature branch. The installer verifies BACKEND_PAYLOAD.json against candidate and old source, checks current pip dependencies, and verifies current API/bot service activity and API health before stopping anything. Automatic creation is disabled without a valid protected profile and its explicit create flag. Supported credentials/IAM/bootstrap steps are in BOOTSTRAP.md.

After separate operator approval, copy-paste with the **verified** health URL (the example is the supplied HTTPS endpoint):

```sh
cd /ROOT_CONTROLLED_REVIEWED_CHECKOUT
sudo /opt/nemesis/.venv/bin/python deployment/install_firebase_manager.py check \
  --health-url https://nemesispanel.shop/health
sudo /opt/nemesis/.venv/bin/python deployment/install_firebase_manager.py apply \
  --health-url https://nemesispanel.shop/health
```

The first installation leaves the manager disabled. It prefetches wheels before service interruption, creates protected source, complete venv and SQLite online-backup snapshots under `/opt/nemesis/backups/firebase-manager`, stops only the two NEMESIS services, installs the reviewed Python files atomically, installs only additive Google SDK dependencies from local wheels, verifies pip/dependency imports/syntax, and applies the additive SQLite migration transactionally. It does not rewrite accounts, auth challenges, sessions, existing assigned_user_id or database URLs. It writes a small dedicated systemd drop-in per service (not the original unit/environment files), daemon-reloads and restarts those services. New code does not fetch credentials or provision Cloud resources at startup with the feature disabled.

Post-install checks require API HTTP 200 with expected health JSON and active units, plus a **new successful Telegram getUpdates heartbeat** in the manager metadata table. An active bot process alone is not treated as a successful new poll. This also checks disabled-manager startup without affecting existing registration/login. A healthy endpoint is availability evidence, not a live Firebase isolation test.

Then perform the protected project/credential bootstrap in BOOTSTRAP.md. Once the service identity, IAM inheritance/policy fingerprint, Cloud billing/quota, region, instance cap and approved deny-all Rules are reviewed:

```sh
sudo /opt/nemesis/.venv/bin/python deployment/install_firebase_manager.py apply \
  --enable-manager --health-url https://nemesispanel.shop/health
```

A missing/invalid project profile refuses activation and restores the prior source/dependencies. An empty alias map permits only the owner dashboard; no project can be created or registered. Actual Google checks run during confirmed jobs and must pass before availability. Per-profile `create_enabled` and `billing_acknowledged` remain required even after the manager is enabled. Direct client access remains denied. The separate limited preferences gateway stays disabled by the installer; device data/monitoring remains outside scope.

Repeated installation of exactly the same payload/flag is a health-checked no-op (no new source/venv backup, service interruption or provisioning). Each real change reports its protected backup directory. No backups, wheels, environment files, data or keys belong in Git. Protect enough disk for the source/venv/DB backup and wheels; failures before replacement leave the old source intact. File replacement retains service-readable ownership; original units and drop-ins are backed up privately. Credential/bootstrap files are never copied into Android.

## Rollback

On installation, dependency, migration or post-install health failure, automatic recovery attempts to restore the previous source, venv and dedicated drop-ins, then restarts the API/bot. Manual rollback uses the **exact protected directory printed by apply**:

```sh
sudo /opt/nemesis/.venv/bin/python deployment/install_firebase_manager.py rollback \
  --backup /opt/nemesis/backups/firebase-manager/firebase-manager-EXACT_REPORTED_DIRECTORY \
  --health-url https://nemesispanel.shop/health
```

Unknown later source edits or unprotected/symlink backup directories are refused. Repeated rollback of already-restored healthy source is a no-op. Source/dependencies revert, but the live SQLite database is **not automatically restored**: new registrations/renewals may have committed since restart. Additive tables and permanent assignment guards remain compatible with the old source. Unverified/stale manager rows are made inactive before restarting the old allocator, so rollback cannot silently bypass new verification. Assignment values and customer records remain intact. The protected DB snapshot is disaster-recovery material only; using it requires a separate private reconciliation/review to avoid losing new customer activity.

Cloud resources created before a failure/rollback remain recorded in durable jobs and are **never automatically deleted, released or recycled**. Review project inventory and resume the same persisted operation after recovery. No secrets or customer records are printed by the tool. Actual systemd/dependency/network failures must be inspected privately on the server, not pasted into a public issue.

Old bot versions do not emit the new heartbeat, so rollback checks old-unit activity/API health and requires an operator `/status`/registration smoke test in the private bot. After activation use a dedicated test customer for creation, distinct allocations, approval/denial, expiry/renewal, and real unprivileged cross-tenant denial. Do not paste real passwords, OTPs, bearer tokens, service-account JSON or database contents into shell arguments/logs/reports.
