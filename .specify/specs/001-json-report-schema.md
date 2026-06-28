# Spec: Diagnosis JSON Report Schema

## Title
Structured JSON report schema for disease diagnosis outputs

## Status
Implemented

## Context
The application must produce machine-readable, schema-validated JSON for every diagnosis so that offline dashboards, exports, and future integrations can rely on a stable contract.

## Goals
- Enforce strict typing and required fields for every report.
- Enable Pydantic validation without runtime surprises.
- Provide a serializable format compatible with SQLite JSON columns.

## Non-Goals
- Schema does not define analytics aggregations.
- Schema does not mandate a specific image storage format.

## Stakeholders
| Role | Name | Responsibility |
|------|------|----------------|
| Backend Developer | | API and validation |
| AI/ML Engineer | | Output guarantees |
| Frontend Developer | | Display and export |

## Requirements

### Functional
- [x] Each report contains an `id` (uuid).
- [x] Each report contains a `timestamp` (ISO-8601).
- [x] Each report contains `disease` and `confidence`.
- [x] Each report contains `top_predictions` (array of objects).
- [x] Each report contains `recommendations` (object with 5 named arrays).
- [x] Each report contains `meta` (model version, latency, llm model).

### Non-Functional
- Validation latency < 5 ms per report.
- Schema compatible with Pydantic v2.

## Design Decisions
| Decision | Rationale |
|----------|-----------|
| Pydantic v2 | Native JSON Schema generation and strict validation |
| UUID v7 | Sortable identifiers with embedded timestamp |
| FTS5 on `disease`, `crop_type`, `location`, `notes` | Enables fast offline search |

## Open Questions
- Should `image_path` be a relative path or base64 data URI?

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM returns malformed JSON | Medium | Medium | Retry prompting plus Pydantic enforcement |

## Success Criteria
- 100% of test reports validate successfully.
- API contract tests pass without modification.

## References
- `docs/SPECIFICATION_KIT.md`
- `backend/database/schemas.py`
