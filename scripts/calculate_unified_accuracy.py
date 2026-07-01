import os
import json
import glob
from collections import defaultdict

# Exclude specific FOLIO problems (prefix-based to handle varying folder names)
EXCLUDE_FOLIO_PREFIXES = ("76_", "77_", "78_")

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
        except Exception:
            pass
    return results

def get_mcp_results(base_path):
    # provider -> benchmark -> problem -> list of solver results
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
        except Exception:
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
        except Exception:
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

def calculate_nesygma_results(sys1_results, mcp_results, confidence_data, threshold=75, use_fallback=True):
    # provider -> benchmark -> problem -> bool
    nesygma_res = defaultdict(lambda: defaultdict(dict))
    
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
                    if mcp_correct:
                        sweep_res = True
                    elif use_fallback and all_translator_failed:
                        sweep_res = sys1_correct
                    else:
                        sweep_res = False
                else:
                    # Accepted S1
                    sweep_res = sys1_correct
                    
                nesygma_res[provider][benchmark][problem] = sweep_res
                
    return nesygma_res

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys1_path = os.path.join(base_dir, "output_system1")
    mcp_path = os.path.join(base_dir, "output_mcp")
    switcher_path = os.path.join(base_dir, "output_switcher")
    
    sys1_results = get_system1_results(sys1_path)
    mcp_results = get_mcp_results(mcp_path)
    confidence_data = get_switcher_confidence(switcher_path)
    
    # Calculate NeSygma with no fallback at tau = 75
    nesygma_results = calculate_nesygma_results(sys1_results, mcp_results, confidence_data, threshold=75)
    
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
    
    # Define benchmarks to calculate
    benchmarks_list = ["ASPBench", "FOLIO", "agieval_lsat", "ALL"]
    
    # Provider -> Benchmark -> {"S1": acc, "S2": acc, "NeSygma": acc}
    accuracies = defaultdict(lambda: defaultdict(dict))
    
    # Populate S1, S2, NeSygma accuracies
    for provider in sorted_providers:
        for b_name in benchmarks_list:
            if b_name == "ALL":
                # System 1
                s1_correct = 0
                for b in EXPECTED_COUNTS:
                    s1_correct += sum(1 for is_c in sys1_results[provider][b].values() if is_c)
                s1_acc = s1_correct / TOTAL_EXPECTED * 100
                
                # S2 (MCP)
                s2_correct = 0
                for b in EXPECTED_COUNTS:
                    s2_correct += sum(1 for p_data in mcp_results[provider][b].values() if p_data.get('mcp_correct', False))
                s2_acc = s2_correct / TOTAL_EXPECTED * 100
                
                # NeSygma
                ns_correct = 0
                for b in EXPECTED_COUNTS:
                    ns_correct += sum(1 for is_c in nesygma_results[provider][b].values() if is_c)
                ns_acc = ns_correct / TOTAL_EXPECTED * 100
            else:
                expected = EXPECTED_COUNTS[b_name]
                s1_acc = sum(1 for is_c in sys1_results[provider][b_name].values() if is_c) / expected * 100
                s2_acc = sum(1 for p_data in mcp_results[provider][b_name].values() if p_data.get('mcp_correct', False)) / expected * 100
                ns_acc = sum(1 for is_c in nesygma_results[provider][b_name].values() if is_c) / expected * 100
                
            accuracies[provider][b_name] = {
                "S1": s1_acc,
                "S2": s2_acc,
                "NeSygma": ns_acc
            }
            
    # Calculate Rerata (Average) across all 12 models
    rerata = {}
    for b_name in benchmarks_list:
        rerata[b_name] = {
            "S1": sum(accuracies[p][b_name]["S1"] for p in sorted_providers) / len(sorted_providers),
            "S2": sum(accuracies[p][b_name]["S2"] for p in sorted_providers) / len(sorted_providers),
            "NeSygma": sum(accuracies[p][b_name]["NeSygma"] for p in sorted_providers) / len(sorted_providers)
        }
        
    # Generate LaTeX table rows
    rows = []
    for provider in sorted_providers:
        name = mapping[provider]
        row_cells = [name]
        
        for b_name in benchmarks_list:
            vals = accuracies[provider][b_name]
            s1_val = vals["S1"]
            s2_val = vals["S2"]
            ns_val = vals["NeSygma"]
            
            max_val = max(s1_val, s2_val, ns_val)
            
            # Format to 2 decimal places, and replace . with ,
            s1_str = f"{s1_val:.2f}"
            s2_str = f"{s2_val:.2f}"
            ns_str = f"{ns_val:.2f}"
            
            if s1_val == max_val:
                s1_str = f"\\textbf{{{s1_str}}}"
            if s2_val == max_val:
                s2_str = f"\\textbf{{{s2_str}}}"
            if ns_val == max_val:
                ns_str = f"\\textbf{{{ns_str}}}"
                
            
            row_cells.extend([s1_str, s2_str, ns_str])
            
        rows.append(" & ".join(row_cells) + " \\\\")
        
    # Generate Rerata row
    rerata_cells = ["\\textbf{Average}"]
    for b_name in benchmarks_list:
        vals = rerata[b_name]
        s1_val = vals["S1"]
        s2_val = vals["S2"]
        ns_val = vals["NeSygma"]
        
        max_val = max(s1_val, s2_val, ns_val)
        
        s1_str = f"{s1_val:.2f}"
        s2_str = f"{s2_val:.2f}"
        ns_str = f"{ns_val:.2f}"
        
        if s1_val == max_val:
            s1_str = f"\\textbf{{{s1_str}}}"
        if s2_val == max_val:
            s2_str = f"\\textbf{{{s2_str}}}"
        if ns_val == max_val:
            ns_str = f"\\textbf{{{ns_str}}}"
            
        
        rerata_cells.extend([s1_str, s2_str, ns_str])
        
    rerata_row = " & ".join(rerata_cells) + " \\\\"
    
    # Construct complete LaTeX table
    latex_table = f"""\\begin{{table}}[ht]
\t\\centering
\t\\caption{{Accuracy (\\%) of All Models and Strategies Across All Benchmarks.}}
\t\\label{{tab:unifiedAccuracy}}
\t\\scriptsize
\t\\setlength{{\\tabcolsep}}{{2.5pt}}
\t\\begin{{tabular}}{{l|ccc|ccc|ccc|ccc}}
\t\t\\hline
\t\t\\textbf{{Model}} & \\multicolumn{{3}}{{c|}}{{\\textbf{{ASPBench}}}} & \\multicolumn{{3}}{{c|}}{{\\textbf{{FOLIO}}}} & \\multicolumn{{3}}{{c|}}{{\\textbf{{AGIEval-LSAT}}}} & \\multicolumn{{3}}{{c}}{{\\textbf{{ALL}}}} \\\\
\t\t& S1 & S2 & NeSygma & S1 & S2 & NeSygma & S1 & S2 & NeSygma & S1 & S2 & NeSygma \\\\
\t\t\\hline
\t\t""" + "\n\t\t".join(rows) + f"""
\t\t\\hline
\t\t{rerata_row}
\t\t\\hline
\t\\end{{tabular}}
\\end{{table}}"""

    out_path = os.path.join(base_dir, "unified_accuracy_table.tex")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(latex_table)
    
    print("RECALCULATION COMPLETE.")
    print(f"LaTeX table saved to: {out_path}")
    print("\n--- LATEX TABLE CODE ---\n")
    print(latex_table)
    print("\n------------------------\n")

if __name__ == "__main__":
    main()
