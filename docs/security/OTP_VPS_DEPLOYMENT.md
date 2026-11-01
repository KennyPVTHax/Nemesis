# Prepared VPS patch — do not execute until separately approved

This runbook changes only `/opt/nemesis/backend/auth_api.py`. The script and unified diff are prepared for review; **neither has been executed on the VPS**. No bot, registration, Firebase, proxy, environment, dependency installation or database/schema operation is included. The CLI does not guess service names, interpreters or ports.

## Preconditions

An operator must verify the actual systemd API unit, the Python executable used by that unit, and its direct loopback `/health` URL. These are not in the source export. Confirm the chosen unit owns **all API workers** using this file; do not select the Telegram polling unit. Review any automatic reload/supervisor behavior and arrange the API restart window. Existing sessions and database contents are intentionally not changed. Service restart may interrupt in-flight requests; the client can restart login subject to normal server limits.

Use a trusted, root-controlled checkout of this security branch containing the candidate `backend/auth_api.py`, script and checksum metadata together. Verify the reviewed commit before proceeding. Do not use a directory writable by other users. The file must be a regular non-symlink at the exact production path, without group/world write permission. The script refuses any source hash other than the original baseline or this reviewed patch, so a different production revision requires a newly reviewed diff, not bypassing the guard.

The backup directory `/opt/nemesis/backups/otp-attempt-rollback` must be root-owned mode 0700 and have no symlink path components; the script creates it if absent and refuses an incompatible existing directory. Backups are source-only, mode 0600, verified and fsynced before replacement. They do not contain a database snapshot or runtime credentials. Keep them private and outside Git.

## Commands to prepare on the VPS, after approval

Replace all angle-bracket placeholders with verified local values. Do not paste environment contents, passwords, codes, tokens or logs into the PR. Running `check` invokes local dependency/unit checks and loopback health but does not replace source or restart a service. It has not been run here.

```sh
cd <ROOT_CONTROLLED_REVIEWED_CHECKOUT>
sudo <API_PYTHON_ABSOLUTE_PATH> deployment/deploy_otp_fix.py check \
  --service <VERIFIED_API_UNIT.service> \
  --python <API_PYTHON_ABSOLUTE_PATH> \
  --health-url <VERIFIED_LOOPBACK_HEALTH_URL>
```

Preflight checks the unit is loaded, imports FastAPI/Pydantic/Argon2/httpx/SQLite with the supplied production interpreter, runs its `pip check`, and compiles the candidate source without importing the application or touching its configured database. Missing/broken dependencies stop deployment; nothing is automatically installed or upgraded. Health requires active systemd state, HTTP 200, and the expected `status: online` / `service: NEMESIS Backend` JSON. Only credential-free loopback HTTP/HTTPS `/health` URLs are allowed, redirects are rejected, and normal TLS verification remains enabled for HTTPS.

After successful preflight and explicit deployment approval:

```sh
sudo <API_PYTHON_ABSOLUTE_PATH> deployment/deploy_otp_fix.py apply \
  --service <VERIFIED_API_UNIT.service> \
  --python <API_PYTHON_ABSOLUTE_PATH> \
  --health-url <VERIFIED_LOOPBACK_HEALTH_URL>
```

Apply uses a protected deployment lock, verifies the original checksum, creates and validates a durable private backup, atomically installs the reviewed bytes while retaining file ownership/mode, fsyncs the directory, restarts only the specified API unit, and checks health. It reports the backup filename. Reapplying the same patch verifies dependencies/health but creates no new backup and performs no restart. Unknown source/candidate drift is refused. The unified `deployment/otp-attempt-rollback.patch` is for diff review; do not apply it directly and bypass these guards.

If replacement/restart/postdeployment health fails after installation, the script attempts automatic restoration of the verified original file, restarts the same API unit and rechecks health. It returns failure even if recovery succeeds. If an unknown concurrent source edit is detected, it refuses to overwrite it. If rollback fails, stop and recover locally using the verified backup; do not rerun with disabled checks. Command output is suppressed rather than leaking possible service/runtime details.

## Explicit rollback

Use the exact backup path reported by apply. A backup outside the protected directory, a symlink, or one with an unexpected hash is refused. Healthy, already-restored baseline source is a no-op. Rollback intentionally restores the original OTP defect and is only an availability contingency; schedule the reviewed security repair again after resolving the deployment problem.

```sh
sudo <API_PYTHON_ABSOLUTE_PATH> deployment/deploy_otp_fix.py rollback \
  --backup <EXACT_BACKUP_PATH_FROM_APPLY> \
  --service <VERIFIED_API_UNIT.service> \
  --python <API_PYTHON_ABSOLUTE_PATH> \
  --health-url <VERIFIED_LOOPBACK_HEALTH_URL>
```

No automatic session/challenge deletion, password changes, database rollback or key rotation is performed. A healthy endpoint confirms service availability, not OTP correctness; conduct a separate authorized test-account check of three wrong codes followed by a correct code and a fresh successful login after deployment. Use a dedicated test account and keep its secrets out of shell arguments, logs and public reports. The local regression suite already checks these cases without production access.
