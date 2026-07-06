import json
import os
from pathlib import Path

def main():
    PROVIDERS = {
        "google": "Gemini 3.1 Flash Lite",
        "openrouter": "GPT OSS 120B",
        "openrouter2": "GPT OSS 20B",
        "openrouter3": "Mimo V2 Flash Non Reasoning",
        "openrouter6": "Mimo V2 Flash Reasoning",
        "openrouter4": "Deepseek V4 Flash High Reasoning",
        "openrouter5": "Deepseek V4 Flash Non Reasoning",
        "mistral": "Mistral Small 4 High Reasoning",
        "mistral2": "Mistral Small 4 Non Reasoning",
        "xiaomi2": "Mimo V2.5 Pro Reasoning",
        "xiaomi": "Mimo V2.5 Pro Non Reasoning",
        "nvidia": "Nvidia Nemotron Nano 30B A3B Reasoning",
    }

    base_dir = Path("output_mcp")
    
    # Excluded FOLIO problems
    excluded_folio = ["76_story_368_ex_76", "77_story_368_ex_77", "78_story_368_ex_78"]
    
    if not base_dir.exists():
        print(f"Directory {base_dir} does not exist.")
        return

    providers = [p for p in base_dir.iterdir() if p.is_dir()]
    
    for provider in providers:
        total_problems = 0
        failed_problems = 0
        
        benchmarks = [b for b in provider.iterdir() if b.is_dir()]
        for benchmark in benchmarks:
            problems = [prob for prob in benchmark.iterdir() if prob.is_dir()]
            for problem in problems:
                
                if benchmark.name.lower() == "folio" and problem.name in excluded_folio:
                    continue
                
                total_problems += 1
                
                solvers = [s for s in problem.iterdir() if s.is_dir()]
                if not solvers:
                    continue
                
                all_solvers_failed = True
                has_any_result = False
                
                for solver in solvers:
                    result_file = solver / "result.jsonl"
                    if result_file.exists():
                        has_any_result = True
                        with open(result_file, "r", encoding="utf-8") as f:
                            try:
                                data = json.loads(f.readline())
                                model_answer = data.get("model_answer", "")
                                if model_answer:
                                    if "Translator failed after 4 iterations." not in model_answer:
                                        all_solvers_failed = False
                                else:
                                    all_solvers_failed = False
                            except Exception:
                                all_solvers_failed = False
                    else:
                        all_solvers_failed = False
                        
                if has_any_result and all_solvers_failed:
                    failed_problems += 1
        
        if total_problems > 0:
            percentage = (failed_problems / total_problems) * 100
            model_name = PROVIDERS.get(provider.name, provider.name)
            print(f"Model: {model_name:<35} | Failed: {failed_problems}/{total_problems} ({percentage:.2f}%)")
        else:
            model_name = PROVIDERS.get(provider.name, provider.name)
            print(f"Model: {model_name:<35} | No problems found.")

if __name__ == "__main__":
    main()
