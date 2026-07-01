import os
import json
import glob
from collections import defaultdict

# Exclude specific problems (prefix-based to handle varying folder names)
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

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys1_path = os.path.join(base_dir, "output_system1")
    mcp_path = os.path.join(base_dir, "output_mcp")
    switcher_path = os.path.join(base_dir, "output_switcher")
    
    sys1_results = get_system1_results(sys1_path)
    mcp_results = get_mcp_results(mcp_path)
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
    
    print("=========================================================================")
    print(f"CALCULATING FALLBACK RATE TO SYSTEM 1 (Threshold = {threshold}%)")
    print("=========================================================================\n")
    
    # provider -> benchmark -> metrics
    fallback_stats = defaultdict(lambda: defaultdict(dict))
    
    for provider in sorted_providers:
        print(f"Model: {mapping[provider]}")
        
        # Overall totals for this provider
        overall_total = 0
        overall_escalated = 0
        overall_fallback = 0
        
        for benchmark, expected in EXPECTED_COUNTS.items():
            problems = set(sys1_results[provider][benchmark].keys())
            total = len(problems)
            if total == 0:
                total = expected  # Fallback to expected if empty
            
            escalated = 0
            fallback = 0
            
            for problem in problems:
                conf = confidence_data[provider][benchmark].get(problem, 0.0)
                mcp_data = mcp_results[provider][benchmark].get(problem, {})
                all_translator_failed = mcp_data.get('all_translator_failed', False)
                
                should_escalate = (conf <= threshold)
                
                if should_escalate:
                    escalated += 1
                    if all_translator_failed:
                        fallback += 1
            
            esc_rate = (escalated / total * 100) if total > 0 else 0.0
            fb_overall_rate = (fallback / total * 100) if total > 0 else 0.0
            fb_esc_rate = (fallback / escalated * 100) if escalated > 0 else 0.0
            
            fallback_stats[provider][benchmark] = {
                "total": total,
                "escalated": escalated,
                "fallback": fallback,
                "esc_rate": esc_rate,
                "fb_overall_rate": fb_overall_rate,
                "fb_esc_rate": fb_esc_rate
            }
            
            print(f"  {benchmark}:")
            print(f"    Total Evaluated       : {total}")
            print(f"    Escalated (<= {threshold}%) : {escalated} ({esc_rate:.2f}%)")
            print(f"    Fallback to System 1  : {fallback} (Overall: {fb_overall_rate:.2f}%, Of Escalated: {fb_esc_rate:.2f}%)")
            
            overall_total += total
            overall_escalated += escalated
            overall_fallback += fallback
            
        overall_esc_rate = (overall_escalated / overall_total * 100) if overall_total > 0 else 0.0
        overall_fb_overall_rate = (overall_fallback / overall_total * 100) if overall_total > 0 else 0.0
        overall_fb_esc_rate = (overall_fallback / overall_escalated * 100) if overall_escalated > 0 else 0.0
        
        fallback_stats[provider]["ALL"] = {
            "total": overall_total,
            "escalated": overall_escalated,
            "fallback": overall_fallback,
            "esc_rate": overall_esc_rate,
            "fb_overall_rate": overall_fb_overall_rate,
            "fb_esc_rate": overall_fb_esc_rate
        }
        
        print(f"  ALL Benchmarks:")
        print(f"    Total Evaluated       : {overall_total}")
        print(f"    Escalated (<= {threshold}%) : {overall_escalated} ({overall_esc_rate:.2f}%)")
        print(f"    Fallback to System 1  : {overall_fallback} (Overall: {overall_fb_overall_rate:.2f}%, Of Escalated: {overall_fb_esc_rate:.2f}%)")
        print("-" * 50)
        
    # Generate Rerata (Average) across all models
    rerata = {}
    benchmarks_list = ["ASPBench", "FOLIO", "agieval_lsat", "ALL"]
    for benchmark in benchmarks_list:
        avg_esc_rate = sum(fallback_stats[p][benchmark]["esc_rate"] for p in sorted_providers) / len(sorted_providers)
        avg_fb_overall = sum(fallback_stats[p][benchmark]["fb_overall_rate"] for p in sorted_providers) / len(sorted_providers)
        avg_fb_esc = sum(fallback_stats[p][benchmark]["fb_esc_rate"] for p in sorted_providers) / len(sorted_providers)
        
        rerata[benchmark] = {
            "esc_rate": avg_esc_rate,
            "fb_overall_rate": avg_fb_overall,
            "fb_esc_rate": avg_fb_esc
        }
        
    # Generate LaTeX table
    latex_rows = []
    for prov in sorted_providers:
        name = mapping[prov]
        stats = fallback_stats[prov]["ALL"]
        
        esc_str = f"{stats['esc_rate']:.2f}\\%"
        fb_overall_str = f"{stats['fb_overall_rate']:.2f}\\%"
        fb_esc_str = f"{stats['fb_esc_rate']:.2f}\\%"
        
        row_str = f"{name} & {stats['total']} & {stats['escalated']} ({esc_str}) & {stats['fallback']} ({fb_overall_str}) & {fb_esc_str} \\\\"
        latex_rows.append(row_str)
        
    avg_esc_str = f"{rerata['ALL']['esc_rate']:.2f}\\%"
    avg_fb_overall_str = f"{rerata['ALL']['fb_overall_rate']:.2f}\\%"
    avg_fb_esc_str = f"{rerata['ALL']['fb_esc_rate']:.2f}\\%"
    
    latex_table = f"""\\begin{{table}}[ht]
\t\\centering
\t\\caption{{Escalation and Fallback Rate to System 1 in the NeSygma Architecture ($\\tau = {threshold}\\%$).}}
\t\\label{{tab:fallbackRates}}
\t\\small
\t\\begin{{tabular}}{{l|c|c|c|c}}
\t\t\\hline
\t\t\\textbf{{Model}} & \\textbf{{Total Problems}} & \\textbf{{Escalation (\\%)}} & \\textbf{{Fallback vs Total (\\%)}} & \\textbf{{Fallback vs Escalation (\\%)}} \\\\
\t\t\\hline
\t\t""" + "\n\t\t".join(latex_rows) + f"""
\t\t\\hline
\t\t\\textbf{{Average}} & {int(sum(fallback_stats[p]['ALL']['total'] for p in sorted_providers)/len(sorted_providers))} & \\textbf{{{avg_esc_str}}} & \\textbf{{{avg_fb_overall_str}}} & \\textbf{{{avg_fb_esc_str}}} \\\\
\t\t\\hline
\t\\end{{tabular}}
\\end{{table}}"""

    out_path = os.path.join(base_dir, "fallback_rate_table.tex")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(latex_table)
        
    print(f"\nLaTeX table saved to: {out_path}")
    print("\n--- LATEX TABLE CODE ---\n")
    print(latex_table)
    print("\n------------------------\n")

if __name__ == "__main__":
    main()
