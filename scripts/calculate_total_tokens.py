import os
import json
import glob
from collections import defaultdict

EXCLUDE_FOLIO_PREFIXES = ("76_", "77_", "78_")

def get_tokens(base_path, token_key, multiple_solvers=False):
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    if multiple_solvers:
        pattern = os.path.join(base_path, "*", "*", "*", "*", "result.jsonl")
    else:
        pattern = os.path.join(base_path, "*", "*", "*", "result.jsonl")
        
    for file_path in glob.glob(pattern):
        parts = os.path.normpath(file_path).split(os.sep)
        if multiple_solvers:
            provider = parts[-5]
            benchmark = parts[-4]
            problem = parts[-3]
        else:
            provider = parts[-4]
            benchmark = parts[-3]
            problem = parts[-2]
            
        if benchmark == "FOLIO" and problem.startswith(EXCLUDE_FOLIO_PREFIXES):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.loads(f.read().strip())
                tokens = data.get(token_key, 0)
                if not isinstance(tokens, (int, float)):
                    tokens = 0
                results[provider][benchmark][problem] += int(tokens)
        except Exception:
            pass
    return results

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

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys1_path = os.path.join(base_dir, "output_system1")
    mcp_path = os.path.join(base_dir, "output_mcp")
    switcher_path = os.path.join(base_dir, "output_switcher")
    selector_path = os.path.join(base_dir, "output_selector")
    
    token_key = "total_tokens"
    label_prefix = "Total"
    
    sys1_tokens = get_tokens(sys1_path, token_key)
    switcher_tokens = get_tokens(switcher_path, token_key)
    selector_tokens = get_tokens(selector_path, token_key)
    mcp_tokens = get_tokens(mcp_path, token_key, multiple_solvers=True)
    
    confidence_data = get_switcher_confidence(switcher_path)
    threshold = 75
    
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
    benchmarks_list = ["ASPBench", "FOLIO", "agieval_lsat", "ALL"]
    
    token_counts = defaultdict(lambda: defaultdict(dict))
    
    for provider in sorted_providers:
        for b_name in benchmarks_list:
            if b_name == "ALL":
                b_keys = ["ASPBench", "FOLIO", "agieval_lsat"]
            else:
                b_keys = [b_name]
                
            s1_total = 0
            s2_total = 0
            ns_total = 0
            
            for b in b_keys:
                problems = set(sys1_tokens[provider][b].keys()) | set(selector_tokens[provider][b].keys()) | set(mcp_tokens[provider][b].keys()) | set(switcher_tokens[provider][b].keys())
                for problem in problems:
                    t_s1 = sys1_tokens[provider][b].get(problem, 0)
                    t_sw = switcher_tokens[provider][b].get(problem, 0)
                    t_sel = selector_tokens[provider][b].get(problem, 0)
                    t_mcp = mcp_tokens[provider][b].get(problem, 0)
                    
                    conf = confidence_data[provider][b].get(problem, 0.0)
                    escalates = (conf <= threshold)
                    
                    s1_total += t_s1
                    s2_total += (t_sel + t_mcp)
                    
                    ns_total += (t_s1 + t_sw)
                    if escalates:
                        ns_total += (t_sel + t_mcp)
                        
            token_counts[provider][b_name] = {
                "S1": s1_total,
                "S2": s2_total,
                "NeSygma": ns_total
            }
            
    # Rerata (Average) across models
    rerata = {}
    for b_name in benchmarks_list:
        rerata[b_name] = {
            "S1": sum(token_counts[p][b_name]["S1"] for p in sorted_providers) / len(sorted_providers),
            "S2": sum(token_counts[p][b_name]["S2"] for p in sorted_providers) / len(sorted_providers),
            "NeSygma": sum(token_counts[p][b_name]["NeSygma"] for p in sorted_providers) / len(sorted_providers)
        }
        
    rows = []
    for provider in sorted_providers:
        name = mapping[provider]
        if name.startswith(" DeepSeek"):
            name = name.strip()
        row_cells = [name]
        
        for b_name in benchmarks_list:
            vals = token_counts[provider][b_name]
            s1_str = f"{vals['S1']:,}"
            s2_str = f"{vals['S2']:,}"
            ns_str = f"{vals['NeSygma']:,}"
            row_cells.extend([s1_str, s2_str, ns_str])
            
        rows.append(" & ".join(row_cells) + " \\\\")
        
    rerata_cells = ["\\textbf{Average}"]
    for b_name in benchmarks_list:
        vals = rerata[b_name]
        s1_str = f"{int(vals['S1']):,}"
        s2_str = f"{int(vals['S2']):,}"
        ns_str = f"{int(vals['NeSygma']):,}"
        rerata_cells.extend([s1_str, s2_str, ns_str])
        
    rerata_row = " & ".join(rerata_cells) + " \\\\"
    
    latex_table = "\\begin{table}[ht]\n\t\\centering\n\t\\caption{Total Tokens of All Models and Strategies Across All Benchmarks.}\n\t\\label{tab:" + label_prefix + "Tokens}\n\t\\scriptsize\n\t\\setlength{\\tabcolsep}{2.5pt}\n\t\\begin{tabular}{l|ccc|ccc|ccc|ccc}\n\t\t\\hline\n\t\t\\textbf{Model} & \\multicolumn{3}{c|}{\\textbf{ASPBench}} & \\multicolumn{3}{c|}{\\textbf{FOLIO}} & \\multicolumn{3}{c|}{\\textbf{AGIEval-LSAT}} & \\multicolumn{3}{c}{\\textbf{ALL}} \\\\\n\t\t& S1 & S2 & NeSygma & S1 & S2 & NeSygma & S1 & S2 & NeSygma & S1 & S2 & NeSygma \\\\\n\t\t\\hline\n\t\t" + "\n\t\t".join(rows) + "\n\t\t\\hline\n\t\t" + rerata_row + "\n\t\t\\hline\n\t\\end{tabular}\n\\end{table}"

    out_path = os.path.join(base_dir, f"total_tokens_table.tex")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(latex_table)
    
    print("CALCULATION COMPLETE.")
    print(f"LaTeX table saved to: {out_path}")

if __name__ == "__main__":
    main()
