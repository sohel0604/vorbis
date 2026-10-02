# Infrastructure

The local container stack is defined in the repository root `docker-compose.yml` (web, API, PostgreSQL). Production infrastructure is intentionally unspecified until deployment region, identity, object storage, encryption, retention, and availability requirements are known. Use managed secrets and database services, and do not expose the local Compose defaults publicly.
