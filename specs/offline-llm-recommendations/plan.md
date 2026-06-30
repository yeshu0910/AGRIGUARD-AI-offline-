# Implementation Plan: Offline LLM Recommendations

## Architecture

The recommendation system has two layers:
1. Primary: Local LLM (Phi-3 Mini) via llama-cpp-python
2. Fallback: Curated dictionary FALLBACK_REPORTS in llm.py

## Components

| Component | File | Responsibility |
|-----------|------|----------------|
| LLM Client | `llm.py` | Phi-3 Mini inference wrapper |
| Fallback | `llm.py` | FALLBACK_REPORTS dictionary |
| Prompt Template | `llm.py` | Structured JSON prompt |

## LLM Configuration

- Model: Phi-3 Mini 4k (ggmlv3-q4.gguf)
- Context: 2048 tokens
- Device: CPU only (n_gpu_layers=0)
- Temperature: 0.1 for deterministic output