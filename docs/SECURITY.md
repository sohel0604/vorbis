# Security and operational limits

## Implemented safeguards

- Passwords are stored as bcrypt hashes; API sessions use signed, expiring JWTs.
- Project reads and writes require organization membership. Unauthorized IDs return 404.
- ZIP upload size, entry count, individual uncompressed file size, aggregate expanded bytes, and compression ratio are bounded.
- Absolute paths, traversal segments, backslashes, and symbolic links are rejected; ignored build/dependency folders are omitted; archives are indexed without extraction.
- Binary files are not decoded as source. Indexed text snippets are capped at 1 MiB per file.

## Required before production

- Configure a high-entropy `SECRET_KEY`, TLS, secure proxy headers, strict CORS, rate limiting, login abuse controls, and secret rotation.
- Add antivirus or content scanning appropriate to the deployment; the current validator is not malware detection.
- Add Alembic migrations and backup/restore drills. `create_all` is only a development bootstrap, not a schema migration strategy.
- Add invite/role management and verify role policy for each operation. Current role checks only prevent viewer ZIP uploads.
- Define data retention, deletion, residency, encryption-at-rest, access logging, and incident response requirements.
- Move upload processing to an isolated worker with CPU/time/memory limits and persistent object storage for large repositories.
- Add adversarial archive, authentication, authorization, privacy, and dependency scanning checks to required CI.

Do not upload confidential or regulated repositories to an exposed deployment until these controls are addressed.
