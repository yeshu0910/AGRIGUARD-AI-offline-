# Feature Specification: Offline LLM Recommendations

## Feature Overview

Generate structured, actionable treatment recommendations using a local LLM
(Phi-3 Mini GGUF via llama.cpp) running entirely on CPU without internet.

## Problem Statement

Cloud-dependent LLM APIs are unavailable in rural areas. Farmers need locally
generated, expert-quality advice for crop disease treatment.

## Goals

- Generate structured JSON treatment plans using local LLM
- Fallback to curated knowledge base when LLM unavailable
- Support 14+ crop-disease combinations

## Non Goals

- Multi-turn conversation — single-prompt generation only
- Fine-tuning — uses pre-trained Phi-3 Mini

## Functional Requirements

- FR-1: Load Phi-3 Mini GGUF model via llama.cpp on CPU
- FR-2: Generate JSON with severity, affected_area, recommendation
- FR-3: Fallback to FALLBACK_REPORTS dict when LLM unavailable
- FR-4: Handle malformed JSON output gracefully

## Non Functional Requirements

- NFR-1: CPU-only inference (n_gpu_layers=0)
- NFR-2: Max 2048 context window
- NFR-3: Fallback must have 100% coverage for known diseases

## Acceptance Criteria

- Given LLM available, when generate_report is called, then return structured JSON
- Given LLM unavailable, when generate_report is called, then return fallback report
- Given malformed LLM output, when generate_report is called, then return fallback

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM loading failure | No AI advice | Fallback to curated knowledge base |
| Hallucinated treatments | Dangerous advice | JSON schema validation + fallback |

## Dependencies

- llama-cpp-python
- Phi-3 Mini GGUF model file (~2GB)
