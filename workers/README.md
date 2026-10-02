# Worker boundary

ZIP indexing currently runs in the API request process. This directory is reserved for the next operational slice: move validation and parsing into isolated, queued jobs before accepting large or untrusted customer repositories. A worker job must carry an authorized project ID, an immutable source revision, bounded resource limits, retry/idempotency keys, and explicit `queued → running → complete/failed` state. Do not run repository scripts or install packages from uploaded source.
