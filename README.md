# Vorbis

Vorbis turns a software repository into a structured onboarding experience. This repository contains the first usable vertical slice: account and workspace setup, project creation, bounded ZIP indexing, language and symbol inventory, architecture summary, a role-aware three-day outline, and an evidence-linked mentor interface.

## Stack

- **Web:** React, TypeScript, Vite, lucide-react
- **API:** Python 3.11+, FastAPI, Pydantic, SQLAlchemy
- **Data:** PostgreSQL 16 in Compose; SQLite for local development
- **Authentication:** bcrypt password hashes and signed JWT access tokens
- **Delivery:** Docker Compose and GitHub Actions quality checks

## Run locally

1. Copy `.env.example` to `.env` and replace `SECRET_KEY` with a unique random value.
2. Install Python requirements with `pip install -e .`.
3. Start the API from the repository root: `uvicorn app.main:app --app-dir backend --reload`.
4. In a second terminal: `cd frontend && npm install && npm run dev`.
5. Open `http://localhost:5173`. API docs are at `http://localhost:8000/docs`.

For a containerized local deployment, run `docker compose up --build`. Set a non-default `POSTGRES_PASSWORD` and matching secrets in `.env` before exposing it outside a local machine. For production, terminate TLS at a trusted proxy and set `VITE_API_URL` to the externally reachable API URL at build time.

## Product flow

Register → create a project → upload a repository `.zip` → inspect the source inventory and architecture summary → open a role curriculum → ask a repository question and inspect its file/line citations.

The API is versioned under `/api/v1`. Project access is checked through organization membership; unknown and unauthorized project IDs share a 404 response. The upload path indexes archive entries in memory without extracting them to a filesystem.

## Current boundaries

This is a working product foundation, not completion of all 20 roadmap phases. The current architecture diagram groups paths and does not resolve import/call edges. Only Python uses a real AST; JS/TS, Java, Go, and C# symbols use a lightweight declaration matcher. The mentor is deterministic and evidence-selecting; no LLM provider is called. Git provider ingestion, invitations and role administration, antivirus integration, asynchronous workers, full graph/flow tracing, document/video generation, learner event tracking, diffs, audit events, telemetry, and manager dashboards remain future work. Read [the delivery plan](docs/DELIVERY_PLAN.md) before using this for real customer source.

## Engineering docs

- [Architecture and API](docs/ARCHITECTURE.md)
- [AI SDLC and contribution process](docs/AI_SDLC.md)
- [Security and operational limits](docs/SECURITY.md)
- [Delivery plan](docs/DELIVERY_PLAN.md)
