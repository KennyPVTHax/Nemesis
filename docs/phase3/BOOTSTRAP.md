# One-time Google Cloud and credential bootstrap — operator actions only

Nothing in this file was executed against Google Cloud or the production VPS. Provisioning remains disabled until configured and explicitly enabled. Do not put keys, customer data, environment files or private IAM policy bodies into GitHub, APKs, chat or logs.

## IAM, APIs and billing

Use an existing authorized Firebase-enabled Cloud project on Blaze with billing enabled. Operator/bootstrap permissions to enable APIs/manage roles are separate from the runtime identity. Enable firebasedatabase.googleapis.com, cloudresourcemanager.googleapis.com, iam.googleapis.com and cloudbilling.googleapis.com through your approved Google Cloud administration process; do not grant project Owner/Editor to the bot or Android app.

Create a custom role `projects/PROJECT_ID/roles/nemesisFirebaseManager` containing exactly these runtime permissions (the provider verifies its definition):

- firebasedatabase.instances.get
- firebasedatabase.instances.list
- firebasedatabase.instances.create
- firebasedatabase.instances.update
- resourcemanager.projects.get
- resourcemanager.projects.getIamPolicy
- iam.roles.get

The existing/creation operations use get/list/update and creation additionally uses create. The complete manager role includes create even while the per-profile creation flag is off. Billing read uses resourcemanager.projects.get; billing attachment/update permission is not required or granted. No delete, disable, undelete, billing mutation, service-account key creation or IAM policy mutation is used at runtime. REST Rules/data access uses firebase.database + userinfo.email scopes; management uses cloud-platform scope. IAM, not OAuth scope alone, controls permissions.

Example operator commands, using actual verified placeholders on a trusted administrative machine:

```sh
gcloud iam roles create nemesisFirebaseManager --project=PROJECT_ID \
  --title='NEMESIS Firebase Manager' \
  --permissions=firebasedatabase.instances.get,firebasedatabase.instances.list,firebasedatabase.instances.create,firebasedatabase.instances.update,resourcemanager.projects.get,resourcemanager.projects.getIamPolicy,iam.roles.get \
  --stage=GA
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='serviceAccount:RUNTIME_SERVICE_ACCOUNT_EMAIL' \
  --role='projects/PROJECT_ID/roles/nemesisFirebaseManager'
```

Use workload identity with service-account impersonation where available. Limit impersonation to this dedicated identity; any workloadIdentityUser/token-creation grant belongs on that service account, not broad project administration. Server ADC must resolve to the configured service-account email; user ADC and mismatched identities are rejected. Review all inherited organization/folder grants privately: project getIamPolicy cannot prove their absence. The provider rejects extra direct project roles for this principal and any extra permissions in the custom role. The approved project-policy SHA-256 must match on each operation; legitimate IAM changes require review and a refreshed fingerprint.

If workload identity is unavailable, install a dedicated service-account file outside the repository using a private transfer and a copy-paste command on the VPS, never Telegram:

```sh
sudo install -d -o root -g nemesis -m 0750 /etc/nemesis/firebase
sudo install -o root -g nemesis -m 0640 /PRIVATE_TRANSFER_PATH/service-account.json /etc/nemesis/firebase/manager.json
```

Do not print that file. Verify actual service users/groups and grant read access only to the API/bot identity. Credential paths must be absolute under /etc/nemesis/firebase; symlinks and other-readable files are refused. A path is not a credential alias sent to users: Telegram sees only the configured alias.

## Protected profile creation, no text editor needed

First install the code/dependencies with the manager disabled using DEPLOYMENT.md. In the trusted reviewed checkout, obtain a fingerprint with the **same service identity** used by the API/bot (the command prints only the hash):

```sh
sudo -u nemesis /opt/nemesis/.venv/bin/python deployment/bootstrap_firebase_profile.py fingerprint \
  --alias primary --project-id PROJECT_ID --project-number PROJECT_NUMBER \
  --region us-central1 --max-instances 20 \
  --runtime-service-account RUNTIME_SERVICE_ACCOUNT_EMAIL \
  --credential-file /etc/nemesis/firebase/manager.json
```

Omit --credential-file only when verified ADC/workload identity is configured for that service user. After privately reviewing project and inherited IAM, write the alias using the printed hash:

```sh
sudo /opt/nemesis/.venv/bin/python deployment/bootstrap_firebase_profile.py write \
  --alias primary --project-id PROJECT_ID --project-number PROJECT_NUMBER \
  --region us-central1 --max-instances 20 \
  --runtime-service-account RUNTIME_SERVICE_ACCOUNT_EMAIL \
  --credential-file /etc/nemesis/firebase/manager.json \
  --iam-policy-sha256 REVIEWED_POLICY_SHA256
```

This creates/updates root-owned mode-0640 /etc/nemesis/firebase-manager.json atomically. --group selects the verified common service group if not nemesis. Creation is disabled by default. After billing/quota/budget review, repeat write with `--enable-create --billing-acknowledged`. No Cloud resource is created by profile write. Profiles support us-central1, europe-west1 and asia-southeast1; use a distinct alias per approved region. Confirm project ID/number association. All aliases for one project should use the same cap. Start with a cap of 20 for the initial 10–20-instance pool; raise to at least 50 only after quota/cost review. Google validateOnly and creation responses enforce actual availability/quota. Local caps are safeguards, not authoritative Google quota estimates or budget enforcement against other administrators.

Profiles expire their IAM attestation after a year. Update/review fingerprints after IAM changes. No automatic project creation, Blaze upgrade, billing attachment or per-registration provisioning occurs. The project cap counts remote resources plus known local resources to handle listing lag. Jobs reserve deterministic IDs and serialize cloud work. Google quota, billing propagation, timeout or permission failures remain persisted errors/retries; never bypass them by marking an instance available manually.

## Rules and rotation

For existing instances, first review the backend-mediated architecture. The manager will only register an instance with exact deny-all client Rules and validated project identity; it does not rewrite existing Rules. Apply reviewed firebase-security/database.rules.json through the owner's existing approved Firebase deployment process for that exact instance, preserving any necessary private source backups. Do not apply Rules to an unrelated shared production database. New instances created by this manager receive that Rules configuration before becoming available.

Rotate service credentials through the existing secure process: revoke compromised key/impersonation access in Google, install replacement at the same protected path (no chat transfer), review IAM/fingerprint, test /firebase_test for every affected alias and verify real unprivileged denial. Never return plaintext passwords, service-account JSON or long-lived admin tokens to customers. Profile/identity failures pause operations safely; existing assignments are not recycled. Telegram token rotation remains the existing BotFather/server-environment process; never paste it into the repository. No credential rotation was performed in this execution.
