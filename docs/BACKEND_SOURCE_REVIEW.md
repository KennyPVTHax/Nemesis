# Deployed backend source review

All ten Python modules match the supplied SHA256SUMS.txt byte-for-byte; no backend implementation or API/schema changed. main.py includes auth, registration and Firebase routers. The export has no requirements lock, systemd/nginx units, databases, environment files, Firebase Rules or service accounts. New requirements-review.txt is a locally tested dependency selection, not a recovered production lock.

No inlined credential values were found in the inspected modules. Telegram token is read from the server environment. Database/service-account paths are configuration references, not included credentials. Originals remain outside the repository at /workspace/private-source-review/backend-original; no redacted backend copy was needed.

**Confirmed defect requiring separate approval:** auth_api.verify increments attempts inside a SQLite connection context and then raises HTTPException on a wrong code. The context rolls back the increment. The strict expected-failure regression reproduces this locally. The existing code is preserved, not fixed or redeployed. Do not assert the advertised three-attempt protection is verified. Review transaction handling and add an approved fix before relying on it. Bot /help text also incorrectly says registration is future functionality despite implemented commands; source retained unchanged.

Firebase modules manage inventory, allocation and approved URL disclosure. URLs do not confer authorization. There is no Firebase Rules source or live Firebase connectivity test in the export. Operator CLI validation is not a replacement for deployment OS permissions. No CLI, bot poller or production process was run here. main.py has import-time initialization: tests must redirect account_store.DB_PATH to temporary storage before importing it. Do not run it against production paths during review.

Initial review documentation from source-review-2026-11-02 is preserved in prior-review/ and its existing commits remain ancestors of this branch.
