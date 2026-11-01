# Owner command and inline workflow reference

Only the private linked active NemesisOwner may use these operations. Start with /firebase. All menus are inline keyboards with short-lived single-use callbacks.

| Command | Workflow |
|---|---|
| /firebase | Counts, recent audit, Add/Create, Pool, Assignments, Requests, Test, Disable, Audit and Jobs buttons |
| /firebase_add | Send label, send HTTPS URL, select configured alias; validation queues; approve separate registration confirmation |
| /firebase_create | Select alias, send label, confirm billed creation; inspect /firebase → Provisioning Jobs |
| /firebase_list | Paginated labels, assignments and states |
| /firebase_assign LABEL LOGIN | Confirm permanent assignment; only eligible/unassigned customer and verified free instance |
| /firebase_requests | Pending customers with Approve/Deny buttons; click then confirm decision |
| /firebase_approve LOGIN | Confirm approval of the current pending revision |
| /firebase_deny LOGIN | Confirm denial of the current pending revision |
| /firebase_disable LABEL | Shows affected customer; confirm to pause backend access/new allocation, retaining data and assignment |
| /firebase_enable LABEL [ALIAS] | Confirm fresh verification; only succeeds with active Cloud resource and required isolation |
| /firebase_test LABEL [ALIAS] | Select alias if absent, confirm connectivity/Rules/unprivileged-denial verification; failed validation blocks access |
| /firebase_audit | Paginated administrative audit history |
| /cancel | Cancels an owner wizard and preserves existing registration cancel behavior |

Original /start, /help, /status, /link, /newkey, /redeem, /setid, /registration, /setup and /cancel remain. Existing owner CLI remains available as an operator fallback, but added entries need verification before allocation and approvals require a verified assignment. Bot callbacks never accept credential JSON. Use server alias setup below; do not paste credentials into a chat. Expired confirmations require reopening the manager. Creation registration failure is not success: review the persisted job/diagnostic, repair configuration and retry the same label/alias. No database deletion or reassignment command exists.

Customer: existing authenticated Settings → Check Firebase status → Request Firebase Link. Owner receives Approve/Deny inline buttons. The customer gets a linked-account Telegram decision notification and can refresh authenticated status; approved-link retrieval exposes only their assigned URL. Customer requests are limited to 10 per 15 minutes. Disabled/unverified resources return a validation-required/unavailable status rather than a privileged credential. No regular customer can enter an owner menu or choose another customer's database.
