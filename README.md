# NeSygma Results Repository

## Overview

This repository contains the experimental results and analysis scripts for the **NeSygma** Architecture. It evaluates various Language Models across different reasoning strategies (System 1, System 2, and the NeSygma approach) on reasoning benchmarks.

## Repository Structure

Distinct execution steps store their logs independently for tracing and evaluation:
- `output_system1/`: System 1 Component Result.
- `output_switcher/`: Metacognition Component Result
- `output_selector/`: Selector Component
- `output_mcp/`: Solver Component Result.

## Supported Providers

The analysis evaluates the following providers/models. Each provider writes its own analysis bundle under `output_system1/<provider>/<benchmark_name>/problem_number`. For example `output_system1/google/FOLIO/problem_1/`.

Inside this directory, you will find:
- `index.md`: Contains the raw LLM output.
- `result.jsonl`: Contains the validation result indicating whether the output is `true` or `false`.

For System 2 execution (`output_mcp`), the structure is similar but includes an additional subdirectory for each solver used. For example, `output_mcp/<provider>/<benchmark_name>/problem_number/<solver>/`. If multiple solvers (e.g., `clingo`, `z3`, `vampire`) are utilized for a single problem, each will have its own dedicated folder containing its respective `index.md` and `result.jsonl` files.

| Provider | Label |
| --- | --- |
| `google` | Gemini 3.1 Flash Lite Medium Reasoning |
| `openrouter` | GPT OSS 120B Medium Reasoning |
| `openrouter2` | GPT OSS 20B Medium Reasoning |
| `openrouter3` | Mimo V2 Flash Non Reasoning 309B A15b |
| `openrouter6` | Mimo V2 Flash Reasoning 309B A15b |
| `openrouter4` | Deepseek v4 flash High Reasoning 284B A13b |
| `openrouter5` | Deepseek v4 flash Non Reasoning 284B A13b |
| `mistral` | Mistral Small 4 119B A6b High Reasoning |
| `mistral2` | Mistral Small 4 119B A6b Non Reasoning |
| `xiaomi` | Mimo V2.5 Pro Non reasoning 1T 42b |
| `xiaomi2` | Mimo V2.5 Pro Reasoning 1T 42b |
| `nvidia` | Nvidia Nemotron Nano 30B A3b Reasoning |


## Evaluated Benchmarks
- AGIEVAL_LSAT
- FOLIO
- ASPBench
