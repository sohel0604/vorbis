# Delivery plan

The supplied master roadmap spans a full enterprise product. This repository starts as a greenfield vertical slice; checkboxes below record implementation evidence in the current code, not aspiration.

## Delivered foundation

- [x] Product structure for frontend, backend, docs, infrastructure, workers, and CI.
- [x] Workspace registration/login, organization membership, and tenant-scoped project APIs.
- [x] ZIP validation and indexed source inventory with language and symbol extraction.
- [x] Initial component grouping, role curriculum outline, evidence citation envelope, and readiness scaffold.
- [x] Local Docker Compose deployment path and AI SDLC/security docs.

## Roadmap state

- [ ] RBAC administration, invitations, password recovery, and production session lifecycle.
- [ ] GitHub/GitLab/Azure ingestion; asynchronous, isolated workers; antivirus scanning; object-store retention.
- [ ] Complete language AST adapters and import/call/API/database/event relationship graph.
- [ ] Revision-aware journey tracing, architecture/document generation, and grounded LLM provider integration.
- [ ] Reviewed video/TTS generation, quiz and task execution, learner events, calibrated readiness, incremental diff and stale-content handling.
- [ ] Audit log, cost/latency telemetry, policy controls, manager dashboard, production migrations and release operations.

## Suggested next slices

1. **Harden operations:** Alembic, managed Postgres, object storage, isolated worker queue, rate limiting, audit events, CI tests, deploy previews.
2. **Make indexing trustworthy:** tree-sitter language adapters, package/framework detectors, import resolution, source revision IDs, parser fixtures, full indexing job state.
3. **Ground learning content:** graph schema, retriever with line-accurate chunks, optional provider interface with citations validated after generation, feedback and cost metering.
4. **Close the onboarding loop:** learner progress events, quizzes/tasks tied to evidence, rubric-based readiness, source-diff refresh and manager views.

Update this document as each slice is built and accepted. Never mark a roadmap capability complete based only on a UI placeholder or an unvalidated model output.
