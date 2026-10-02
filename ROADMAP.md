# Vorbis (`vorbis.in`) — AI Software Knowledge Transfer Platform
## Master Engineering Roadmap

**Vorbis** is an enterprise-grade AI-powered **Software Knowledge Transfer OS**.
It turns complex software repositories (ZIP, GitHub, GitLab, Azure DevOps) into a structured, interactive **2–3 day engineering onboarding experience**, answering:
*"What does a new engineer need to understand to become productive on this codebase?"*

---

## 🎯 Master Architecture Blueprint

```
Software Project Input (ZIP / Git / Docs / OpenAPI / DB Schema / Infrastructure)
    ↓
Phase 4 & 5: Ingestion & AST Code Intelligence Engine
    ├── Language / Framework Detection (TS/JS, Python, Java, Go, C#)
    ├── AST Parsing & Relationship Extraction (Imports, Calls, Implements, Extends, DependsOn)
    └── Structural Component Classification (Frontend, API, Service, Repository, Database, Queue)
    ↓
Phase 6 & 7: Project Knowledge Graph & Automatic Architecture Discovery
    ├── Interactive Dependency Graph & ER Diagrams
    └── Service Topologies & Flowcharts
    ↓
Phase 8: Feature Journey Engine
    └── End-to-End Tracer: User Action → React → API → Service → DB → Event → 3rd Party
    ↓
Phase 9 & 10: Role-Based 2–3 Day KT Curriculum & Evidence-Based Documentation
    └── Role Adaptation: Backend, Frontend, Full Stack, DevOps, QA, Tech Lead
    ↓
Phase 11 & 12: AI Mentor & Low-Cost Visual Video Engine
    ├── Evidence-Grounded Q&A (Every answer cites exact file/line AST references)
    └── Video Generator: Script → Scene Planner → Diagrams + Code + Narration (TTS)
    ↓
Phase 13 & 14: Interactive In-Code Quizzes & Hands-on First Tasks
    └── Project-Specific Practice Tasks & First Contribution Guidance
    ↓
Phase 15, 16 & 17: Employee Readiness Scoring, Knowledge Freshness & "What Changed?"
    ├── Dynamic Readiness Signals (Architecture, Backend, Security, Hands-on)
    └── Incremental Git Diff Analysis: Code changes → Auto-updates affected KT modules
    ↓
Phase 18, 19 & 20: Enterprise Security, AI Cost Tracking & Manager Dashboard
```

---

## 🗺️ Phased Implementation Schedule

- [ ] **Phase 0: Product Foundation** — Clean monorepo architecture (`frontend`, `backend`, `ai`, `workers`, `infrastructure`, `docs`, `tests`). The initial folder contained only this roadmap; a starter monorepo now exists, but AI and infrastructure modules are not complete.
- [ ] **Phase 1: Vorbis Website (`vorbis.in`)** — High-converting technical landing page, Hostinger DNS guide, interactive KT sandbox, role curriculum visualizer. Not implemented in this repository yet.
- [ ] **Phase 2: Authentication & Organizations** — Multi-tenant RBAC (Owner, Admin, Manager, Engineer, Viewer), JWT auth, protected routes
- [ ] **Phase 3: Project Management** — Project creation workspace, ZIP upload endpoints, future-ready Git provider interfaces
- [ ] **Phase 4: Secure ZIP Ingestion Pipeline** — Sandboxed unzip, virus/path-traversal scanning, file indexer, ignore filters (`.git`, `node_modules`, `dist`)
- [ ] **Phase 5: Code Intelligence Engine** — Deterministic AST parsing (TS/JS, Python, Java, Go), symbol extraction, dependency graph builder
- [ ] **Phase 6: Project Knowledge Graph** — Multi-dimensional relational graph (`IMPORTS`, `CALLS`, `EXPOSES_API`, `USES_DATABASE`, `PUBLISHES_EVENT`)
- [ ] **Phase 7: Automatic Architecture Discovery** — Auto-generated Mermaid system, service, DB ER diagrams, and auth flowcharts
- [ ] **Phase 8: Feature Journey Engine** — Business flow tracer (e.g., Order Creation: UI $\rightarrow$ Controller $\rightarrow$ Service $\rightarrow$ DB $\rightarrow$ Kafka)
- [ ] **Phase 9: KT Curriculum Generator** — Role-adapted 2–3 day onboarding curricula with milestones and learning objectives
- [ ] **Phase 10: Document Generation Engine** — Evidence-backed technical guides (Architecture, APIs, Database, Setup, First Contribution)
- [ ] **Phase 11: AI Mentor** — Conversational engineer mentor with mandatory file/line AST evidence citations
- [ ] **Phase 12: Low-Cost Video Engine** — Scene planner, syntax-highlighted code slides, flow animations, and TTS narration
- [ ] **Phase 13: Interactive Learning** — Codebase-specific comprehension quizzes and evaluation checkpoints
- [ ] **Phase 14: Hands-on Tasks** — Project-specific first contribution challenges with file references and automated PR checks
- [ ] **Phase 15: Employee Readiness Score** — Granular onboarding signal (Architecture %, Backend %, Security %, Hands-on %)
- [ ] **Phase 16: Knowledge Freshness** — Incremental repository diff engine detecting stale KT modules when code updates
- [ ] **Phase 17: "What Changed?" Experience** — Delta intelligence showing modified features, affected videos, and updated docs
- [ ] **Phase 18: Enterprise Security** — Data isolation, least-privilege LLM retrieval, prompt injection defense, audit logs
- [ ] **Phase 19: Observability & AI Cost Controls** — Per-project token and audio cost metering, latency tracking, OpenTelemetry
- [ ] **Phase 20: Engineering Manager Dashboard** — Team onboarding health, KT completion rates, knowledge gaps, and employee readiness

> Implementation status: see [`docs/DELIVERY_PLAN.md`](docs/DELIVERY_PLAN.md). The checkboxes above describe verified product capability in this repository. A scaffold or placeholder does not count as a completed phase.
