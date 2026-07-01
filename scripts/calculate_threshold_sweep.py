import os
import json
import glob
from collections import defaultdict

# Exclude specific problems (prefix-based to handle varying folder names)
EXCLUDE_FOLIO_PREFIXES = ("76_", "77_", "78_")

# Expected counts
EXPECTED_COUNTS = {
    "ASPBench": 128,
    "FOLIO": 200, 
    "agieval_lsat": 230
}

TOTAL_EXPECTED = sum(EXPECTED_COUNTS.values())

def get_system1_results(base_path):
    results = defaultdict(lambda: defaultdict(dict))
    pattern = os.path.join(base_path, "*", "*", "*", "result.jsonl")
    for file_path in glob.glob(pattern):
        parts = os.path.normpath(file_path).split(os.sep)
        provider = parts[-4]
        benchmark = parts[-3]
        problem = parts[-2]
        
        if benchmark == "FOLIO" and problem.startswith(EXCLUDE_FOLIO_PREFIXES):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                is_correct = data.get("validation", "") == "Correct"
                results[provider][benchmark][problem] = is_correct
        except Exception as e:
            pass
    return results

def get_mcp_results(base_path):
    raw_results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    pattern = os.path.join(base_path, "*", "*", "*", "*", "result.jsonl")
    for file_path in glob.glob(pattern):
        parts = os.path.normpath(file_path).split(os.sep)
        provider = parts[-5]
        benchmark = parts[-4]
        problem = parts[-3]
        
        if benchmark == "FOLIO" and problem.startswith(EXCLUDE_FOLIO_PREFIXES):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                is_correct = data.get("validation", "") == "Correct"
                model_answer = data.get("model_answer", "")
                raw_results[provider][benchmark][problem].append({
                    'is_correct': is_correct,
                    'model_answer': model_answer
                })
        except Exception as e:
            pass

    summary = defaultdict(lambda: defaultdict(dict))
    for provider, benchmarks in raw_results.items():
        for benchmark, problems in benchmarks.items():
            for problem, solver_results in problems.items():
                mcp_correct = any(sr['is_correct'] for sr in solver_results)
                
                # Check if ALL solvers failed with Translator error
                all_failed = True
                if not solver_results:
                    all_failed = False
                else:
                    for sr in solver_results:
                        ans = sr['model_answer']
                        if ans is None:
                            ans = ""
                        if not isinstance(ans, str) or not ans.startswith("Translator failed after 4 iterations."):
                            all_failed = False
                            break
                            
                summary[provider][benchmark][problem] = {
                    'mcp_correct': mcp_correct,
                    'all_translator_failed': all_failed
                }
                
    return summary

def get_switcher_confidence(base_path):
    results = defaultdict(lambda: defaultdict(dict))
    pattern = os.path.join(base_path, "*", "*", "*", "result.jsonl")
    for file_path in glob.glob(pattern):
        parts = os.path.normpath(file_path).split(os.sep)
        provider = parts[-4]
        benchmark = parts[-3]
        problem = parts[-2]
        
        if benchmark == "FOLIO" and problem.startswith(EXCLUDE_FOLIO_PREFIXES):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                conf = data.get("switcher_confidence", None)
                if conf is None:
                    conf = data.get("confidence", None)
                if conf is not None:
                    if isinstance(conf, str):
                        conf = conf.replace("%", "").strip()
                    val = float(conf)
                    results[provider][benchmark][problem] = val
        except Exception as e:
            pass
            
    # Normalize confidence values: if for a given provider all confidence values are <= 1.0, scale them by 100
    for provider, benchmarks in results.items():
        all_vals = []
        for benchmark, problems in benchmarks.items():
            for problem, val in problems.items():
                all_vals.append(val)
        if all_vals and max(all_vals) <= 1.0:
            for benchmark in benchmarks:
                for problem in benchmarks[benchmark]:
                    results[provider][benchmark][problem] *= 100.0
                    
    return results

def calculate_sweep_accuracy(sys1_results, mcp_results, confidence_data, threshold, use_fallback=True):
    # provider -> benchmark -> problem -> bool
    sweep_results = defaultdict(lambda: defaultdict(dict))
    
    providers = set(sys1_results.keys())
    for provider in providers:
        benchmarks = set(sys1_results[provider].keys())
        for benchmark in benchmarks:
            problems = set(sys1_results[provider][benchmark].keys())
            for problem in problems:
                sys1_correct = sys1_results[provider][benchmark].get(problem, False)
                
                mcp_data = mcp_results[provider][benchmark].get(problem, {})
                mcp_correct = mcp_data.get('mcp_correct', False)
                all_translator_failed = mcp_data.get('all_translator_failed', False)
                
                # Get confidence, default to 0.0 (which means it WILL escalate automatically)
                conf = confidence_data[provider][benchmark].get(problem, 0.0)
                
                should_escalate = (conf <= threshold)
                    
                if should_escalate:
                    # Escalated: MCP correct?
                    if mcp_correct:
                        sweep_results[provider][benchmark][problem] = True
                    elif use_fallback and all_translator_failed:
                        # MCP incorrect, but all solvers failed with Translator error -> fallback to S1
                        sweep_results[provider][benchmark][problem] = sys1_correct
                    else:
                        # MCP incorrect
                        sweep_results[provider][benchmark][problem] = False
                else:
                    # Accepted S1
                    sweep_results[provider][benchmark][problem] = sys1_correct
                    
    return sweep_results

def get_overall_accuracy(sweep_results):
    # provider -> overall acc
    accuracy_data = {}
    for provider, benchmarks in sweep_results.items():
        total_correct = 0
        for benchmark, expected_count in EXPECTED_COUNTS.items():
            problem_results = benchmarks.get(benchmark, {})
            correct = sum(1 for is_c in problem_results.values() if is_c)
            total_correct += correct
        accuracy_data[provider] = total_correct / TOTAL_EXPECTED if TOTAL_EXPECTED > 0 else 0
    return accuracy_data

def generate_latex_table(results, thresholds, mapping, sorted_providers, caption, label):
    rows = []
    for prov in sorted_providers:
        name = mapping[prov]
        row_cells = [name]
        for t in thresholds:
            acc = results[t].get(prov, 0.0) * 100
            row_cells.append(f"{acc:.2f}\\%")
        row_str = " & ".join(row_cells) + " \\\\"
        rows.append(row_str)
        
    avg_cells = ["\\textbf{Average}"]
    for t in thresholds:
        avg_acc = sum(results[t].get(p, 0.0) for p in mapping.keys()) / len(mapping) * 100
        avg_cells.append(f"\\textbf{{{avg_acc:.2f}\\%}}")
    avg_str = " & ".join(avg_cells) + " \\\\"
    
    latex_table = f"""
\\begin{{table}}[ht]
\t\\centering
\t\\caption{{{caption}}}
\t\\label{{{label}}}
\t\\small
\t\\begin{{tabular}}{{l|ccccc}}
\t\t\\hline
\t\t\\textbf{{Model}} & \\textbf{{$\\tau = 20$}} & \\textbf{{$\\tau = 40$}} & \\textbf{{$\\tau = 60$}} & \\textbf{{$\\tau = 75$}} & \\textbf{{$\\tau = 89$}} \\\\
\t\t\\hline
""" + "\n".join(rows) + f"""
\t\t\\hline
{avg_str}
\t\t\\hline
\t\\end{{tabular}}
\\end{{table}}
"""
    return latex_table

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys1_path = os.path.join(base_dir, "output_system1")
    mcp_path = os.path.join(base_dir, "output_mcp")
    switcher_path = os.path.join(base_dir, "output_switcher")
    
    sys1_results = get_system1_results(sys1_path)
    mcp_results = get_mcp_results(mcp_path)
    confidence_data = get_switcher_confidence(switcher_path)
    
    thresholds = [20, 40, 60, 75, 89]
    
    # Model mapping for formal LaTeX table
    mapping = {
        "openrouter4": "DeepSeek V4 Flash High Reasoning 284B",
        "openrouter5": "DeepSeek V4 Flash Non-Reasoning 284B",
        "openrouter": "GPT OSS 120B Medium Reasoning",
        "openrouter2": "GPT OSS 20B Medium Reasoning",
        "google": "Gemini 3.1 Flash Lite Medium Reasoning",
        "openrouter3": "MiMo V2 Flash Non-Reasoning 309B",
        "openrouter6": "MiMo V2 Flash Reasoning 309B",
        "xiaomi": "MiMo V2.5 Pro Non-Reasoning 1T",
        "xiaomi2": "MiMo V2.5 Pro Reasoning 1T",
        "mistral": "Mistral Small 4 High Reasoning 119B",
        "mistral2": "Mistral Small 4 Non-Reasoning 119B",
        "nvidia": "Nemotron Nano 30B A3B Reasoning"
    }
    
    sorted_providers = sorted(mapping.keys(), key=lambda k: mapping[k])
    
    # Table 1: WITH fallback
    print("Evaluating: With Translator Fallback")
    results_fb = {}
    for t in thresholds:
        sweep_res = calculate_sweep_accuracy(sys1_results, mcp_results, confidence_data, t, use_fallback=True)
        results_fb[t] = get_overall_accuracy(sweep_res)
    
    latex1 = generate_latex_table(results_fb, thresholds, mapping, sorted_providers,
        "Overall Accuracy Comparison (\\%) Based on Metacognitive Threshold ($\\tau$ - Sweep) (ALL).",
        "tab:thresholdSweep")
    print(latex1)
    with open("threshold_sweep_table.tex", "w", encoding="utf-8") as f:
        f.write(latex1)
    print("Saved to threshold_sweep_table.tex")
    


if __name__ == "__main__":
    main()

