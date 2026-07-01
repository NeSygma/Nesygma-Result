# NeSygma Evaluation Scripts

This directory contains the Python scripts used to evaluate the performance, routing behavior, and token costs of the NeSygma framework compared to baseline approaches (System 1 and System 2). 

These scripts parse the JSON logs from the `output_system1`, `output_switcher`, `output_selector`, and `output_mcp` directories and automatically generate formatted LaTeX tables for inclusion in research papers.

## Available Scripts

### 1. Accuracy Analysis
- **`calculate_unified_accuracy.py`**
  Calculates the main accuracy comparisons between **S1**, **S2** (Selector + MCP), and **NeSygma**. It dynamically checks if NeSygma should fall back to System 2 based on the confidence threshold (default: 75), and falls back automatically if the switcher fails.
- **`calculate_oracle.py`**
  Calculates the **Oracle (Upper Bound) Accuracy**. It considers a problem correctly solved if *either* System 1 *or* at least one solver in the System 2 MCP framework gets the correct answer. It outputs a table comparing NeSygma against this theoretical upper bound.

### 2. Routing & Confidence Analysis
- **`calculate_fallback_rate.py`**
  Analyzes the routing behavior of the Switcher. Calculates exactly how often NeSygma decides to escalate a problem to System 2 (i.e., fallback rate) across different models and benchmarks.
- **`calculate_threshold_sweep.py`**
  Evaluates how the confidence threshold affects NeSygma's accuracy. It tests different threshold values to show the trade-off between fallback rate (cost) and final accuracy.

### 3. Token Cost Analysis
These scripts calculate the token consumption of each strategy to demonstrate the cost-efficiency of NeSygma. NeSygma only consumes System 2 (Selector + MCP) tokens if the Switcher escalates the problem.
- **`calculate_input_tokens.py`**: Calculates total input tokens across all evaluated problems.
- **`calculate_output_tokens.py`**: Calculates total output tokens across all evaluated problems.
- **`calculate_total_tokens.py`**: Calculates the total overall tokens (Input + Output).

## How to Run

Ensure that you have Python installed. You can run any of these scripts directly from the terminal. 

For example, to generate the unified accuracy table:
```bash
python calculate_unified_accuracy.py
```

### Outputs
Upon successful execution, each script will print the results to the standard output and write a formatted `.tex` file (e.g., `unified_accuracy_table.tex`, `total_tokens_table.tex`) into the parent directory, which can be directly imported into LaTeX.

## Notes on Dataset
- The scripts dynamically extract results by parsing the directory structure (`provider/benchmark/problem/result.jsonl`).
- By default, the scripts exclude 3 specific prefix problems from the FOLIO benchmark (`76_`, `77_`, `78_`) to maintain consistency in dataset sizing (200 problems total).
