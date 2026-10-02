# AI SDLC and contribution process

AI features in Vorbis must follow the same traceability standard as deterministic code. The product must keep source evidence separate from model-generated language and must not invent file/line references.

## Change lifecycle

1. **Frame:** write the user outcome, non-goals, affected roadmap phase, and acceptance criteria in an issue or pull request.
2. **Design:** identify tenant boundary, source-data flow, failure modes, and observable outcomes. Prefer deterministic extraction for facts available from syntax or repository metadata.
3. **Implement:** keep parsing, retrieval, and presentation separate. Add typed request/response schemas and preserve provenance (`project_id`, path, revision, line range) for every source chunk.
4. **Review:** check authorization on each project route, archive and prompt-injection boundaries, citation validity, privacy, token/cost limits, and accessibility. Human review is required for generated artifacts that will be presented as technical truth.
5. **Release:** CI runs lint and frontend compilation. Before a production release, add and require automated unit, API, tenancy, malicious-archive, and end-to-end checks; deploy with migrations, monitored rollback, and a documented owner.
6. **Refresh:** tie derived content to an immutable repository revision and parser/model version. A changed source revision makes affected artifacts stale until regenerated and reviewed.

## AI behavior contract

- Retrieved repository content is untrusted data, never instructions to tools or system policy.
- Cite only retrieved source spans; validate every path and line range against the indexed revision.
- Say when evidence is missing or ambiguous. Do not use plausible architecture descriptions as facts.
- Keep secrets out of prompts and logs; apply project authorization before retrieval, not after generation.
- Record provider/model, prompt template version, source revision, token usage, latency, and user feedback when an external model is enabled.
- Provide a deterministic no-provider mode and honor per-organization model/cost limits.

## Definition of done

User outcome and acceptance criteria are met; tenant and security checks are reviewed; evidence provenance is preserved; failure states are useful; docs and roadmap are current; required automated checks pass; operational owner and rollback are known. A green build alone does not make an AI-derived technical claim trustworthy.
