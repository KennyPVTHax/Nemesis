# Restricted source evidence

Nothing in this directory is an executable original monitoring module. Public files contain metadata, schemas, hashes, references and redacted findings only. Two nonsecret deployment files are preserved byte-for-byte under legacy/preserved-features/original-deployment.

Private area: `/workspace/private-source-review/original-recovery/` mode 0700.

- `sealed-originals.tar.gz`: exact uploaded bytes sealed with AES-256-GCM, plus a private metadata manifest. It contains no encryption key.
- `restricted-review.tar.gz`: HTML text review copies with embedded bot credentials and recipient identifiers masked. Sensitive message/financial/control implementation remains inside this restricted archive; it is not published.
- `keys/`: separate read-only encryption key, never printed, published, or included in either archive.
- `sealed/` and `review/`: read-only encrypted inputs and plain-text review files. All evidence files are mode 0400. Uploaded originals were read without mutation.

The byte-exact uploaded source contains an embedded credential; preserving that identity without exposing plaintext credentials requires the separate sealed store. The review archive contains no unmasked embedded bot token or recipient identifier. Do not put either sensitive source archive or its key into GitHub, APKs, web roots, messaging channels, or build inputs. Transfer them separately into owner-controlled durable restricted storage; local workspace retention alone is not an offsite backup. Verify recorded hashes after transfer.

Inspect masked files as text or with a trusted static parser only. Do not open them in a browser, import/evaluate scripts, run anti-inspection behavior, follow source URLs, test credentials, send messages, queue device commands or deploy recovered Rules/code. No real messages, financial records, passwords, PIN/CVV/OTP values or customer database export was acquired during this task. Source constants/patterns and schema references are not captured customer records.

The embedded token must be treated as exposed and reviewed for rotation using the existing private server procedure. Rotation was not performed. Financial/PIN/CVV/credential-forwarding paths require separate security remediation and explicit reviewed activation; possession of source is not permission to activate it.
