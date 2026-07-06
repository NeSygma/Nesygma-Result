import csv
import json
import os
import re
import sys
import logging
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- Configuration & Constants ----------------------------------------------
CATEGORIES = {
    "google": {"reasoning": "Reasoning", "size": "Medium", "provider": "Google"},
    "openrouter": {"reasoning": "Reasoning", "size": "Medium", "provider": "OpenAI"},
    "openrouter2": {"reasoning": "Reasoning", "size": "Small", "provider": "OpenAI"},
    "openrouter3": {"reasoning": "Non Reasoning", "size": "Large", "provider": "Xiaomi"},
    "openrouter6": {"reasoning": "Reasoning", "size": "Large", "provider": "Xiaomi"},
    "openrouter4": {"reasoning": "Reasoning", "size": "Large", "provider": "Deepseek"},
    "openrouter5": {"reasoning": "Non Reasoning", "size": "Large", "provider": "Deepseek"},
    "mistral": {"reasoning": "Reasoning", "size": "Medium", "provider": "Mistral"},
    "mistral2": {"reasoning": "Non Reasoning", "size": "Medium", "provider": "Mistral"},
    "xiaomi2": {"reasoning": "Reasoning", "size": "Frontier", "provider": "Xiaomi"},
    "xiaomi": {"reasoning": "Non Reasoning", "size": "Frontier", "provider": "Xiaomi"},
    "nvidia": {"reasoning": "Reasoning", "size": "Small", "provider": "Nvidia"},
}

PROVIDERS_ORDER = [
    "google", "openrouter", "openrouter2", "openrouter3", "openrouter4",
    "openrouter5", "openrouter6", "mistral", "mistral2",
    "xiaomi", "xiaomi2", "nvidia",
]

PROVIDER_LABELS = {
    "google": "Gemini 3.1 Flash Lite Medium Reasoning",
    "openrouter": "GPT OSS 120B Medium Reasoning",
    "openrouter2": "GPT OSS 20B Medium Reasoning",
    "openrouter3": "Mimo V2 Flash Non Reasoning 309 B",
    "openrouter6": "Mimo V2 Flash Reasoning 309 B",
    "openrouter4": "Deepseek V4 Flash High Reasoning 284B",
    "openrouter5": "Deepseek V4 Flash Non Reasoning 284B",
    "mistral": "Mistral Small 4 High Reasoning 119B",
    "mistral2": "Mistral Small 4 Non Reasoning 119B",
    "xiaomi2": "Mimo V2.5 Pro Reasoning 1T",
    "xiaomi": "Mimo V2.5 Pro Non Reasoning 1T",
    "nvidia": "Nvidia Nemotron Nano 30B A3B Reasoning",
}

BENCHMARK_ORDER = ["agieval_lsat", "FOLIO", "ASPBench"]
SOLVER_ORDER = ["z3", "clingo", "vampire"]

STATUS_ORDER = ["success", "syntax_error", "semantic_error", "overthinking"]
ALL_STATUSES = STATUS_ORDER + ["translator_failed"]

ROOT = Path(".")
OUTPUT_MCP = ROOT / "output_mcp"


# --- Data Models ------------------------------------------------------------
@dataclass
class RunRecord:
    provider: str
    benchmark: str
    problem: str
    solver: str
    status: str
    detail: str = ""
    is_translator_failed: bool = False
    iteration_statuses: list[str] = field(default_factory=list)


# --- Classifiers ------------------------------------------------------------
class BaseSolverClassifier:
    """Base class for parsing result blocks and determining statuses."""
    def __init__(self, full_text: str):
        self.full_text = full_text
        self.payloads = self._extract_payloads()

    def _has_overthinking(self) -> bool:
        return "[OVERTHINKING]" in self.full_text

    def _extract_payloads(self) -> list[dict[str, Any]]:
        blocks: list[str] = []
        pattern = re.compile(
            r"####\s*Result\s*\n+(.*?)(?=\n##|\nTOKEN USAGE|\n\[NOTE\]|\n\[LSAT\]|\n\[FOLIO\]|\Z)",
            re.DOTALL,
        )
        for m in pattern.finditer(self.full_text):
            blocks.append(m.group(1).strip())
        
        payloads = []
        for block in blocks:
            p = self._parse_tool_result_payload(block)
            if p:
                payloads.append(p)
        return payloads

    def _parse_tool_result_payload(self, block: str) -> Optional[dict[str, Any]]:
        m = re.search(r"'text':\s*'(\{.*?\})'", block, re.DOTALL)
        if not m:
            m = re.search(r'"text":\s*"(\{.*?\})"', block, re.DOTALL)
        if not m:
            m = re.search(r'\{["\']status["\'].*?\}', block)
            if m:
                try:
                    return json.loads(m.group(0).replace("'", '"'))
                except json.JSONDecodeError:
                    pass
            return None

        raw = m.group(1)
        
        try: return json.loads(raw)
        except json.JSONDecodeError: pass

        raw_fixed = raw.replace("\\'", "'")
        try: return json.loads(raw_fixed)
        except json.JSONDecodeError: pass

        raw_fixed = raw_fixed.replace('\\"', '"')
        try: return json.loads(raw_fixed)
        except json.JSONDecodeError: pass

        sm = re.search(r'"status"\s*:\s*"([^"]+)"', raw)
        if sm:
            stdout_m = re.search(r'"stdout"\s*:\s*"((?:[^"\\]|\\.)*)"', raw)
            stderr_m = re.search(r'"stderr"\s*:\s*"((?:[^"\\]|\\.)*)"', raw)
            result = {"status": sm.group(1)}
            if stdout_m:
                result["stdout"] = stdout_m.group(1).replace("\\\\r\\\\n", "\n").replace("\\\\n", "\n")
            if stderr_m:
                result["stderr"] = stderr_m.group(1)
            return result
        return None

    def classify_run(self) -> tuple[str, str]:
        """Returns (status, detail). Should be overridden by subclasses."""
        raise NotImplementedError
    
    def classify_payload(self, payload: dict) -> str:
        """Returns status for a single iteration payload. Should be overridden."""
        raise NotImplementedError


class Z3Classifier(BaseSolverClassifier):
    def classify_run(self) -> tuple[str, str]:
        if self._has_overthinking():
            return "overthinking", "output tokens exceeded threshold"

        if not self.payloads:
            if "Translator failed" in self.full_text:
                return "translator_failed", "no payloads, translator failed"
            return "semantic_error", "no result payloads found"

        has_error = False
        has_refinement = False
        has_success_terminal = False
        has_timeout = False

        for p in self.payloads:
            status = str(p.get("status", "")).lower().strip()
            stdout = str(p.get("stdout", "") or "").lower()
            stderr = str(p.get("stderr", "") or "").lower()
            combined = f"{stdout}\n{stderr}"

            if status in ("error", "syntax_error"):
                has_error = True
                continue
            if status == "timeout":
                has_timeout = True
                continue
            if status == "success":
                if "refine:" in stdout or "refine:" in combined:
                    has_refinement = True
                    continue
                if "status: unsat" in combined and "refine" in combined:
                    has_refinement = True
                    continue
                if "status: sat" in combined or "answer:" in combined or "answer :" in combined:
                    has_success_terminal = True
                elif re.search(r'(?:^|\n)\s*[A-E]\s*(?:$|\n)', stdout):
                    has_success_terminal = True
                elif "true" in combined or "false" in combined or "uncertain" in combined:
                    has_success_terminal = True
                else:
                    has_success_terminal = True

        if "Translator failed" in self.full_text:
            if has_error and not has_success_terminal:
                return "syntax_error", "error status + translator failed"
            if has_refinement:
                return "semantic_error", "refinement loops -> translator failed"
            if has_timeout and not has_success_terminal:
                return "semantic_error", "timeout + translator failed"
            return "translator_failed", "translator failed"

        last = self.payloads[-1]
        last_status = str(last.get("status", "")).lower().strip()
        if last_status in ("error", "syntax_error"):
            return "syntax_error", f"final iteration error: {str(last.get('stderr', last.get('error', '')))[:80]}"
        if last_status == "timeout":
            if has_success_terminal:
                return "success", "recovered from timeout"
            return "semantic_error", "z3 timeout (encoding too complex)"

        if has_success_terminal and not has_refinement:
            return "success", "terminal success"
        if has_refinement and has_success_terminal:
            return "semantic_error", "refinement triggered (not real success)"
        if has_refinement:
            return "semantic_error", "refinement without terminal success"
        if has_error and has_success_terminal:
            return "success", "recovered from error"
        if has_error:
            return "syntax_error", "error without recovery"
        if has_timeout:
            return "semantic_error", "z3 timeout"

        return "success", "default success"

    def classify_payload(self, p: dict) -> str:
        s = str(p.get("status", "")).lower().strip()
        stdout = str(p.get("stdout", "") or "").lower()
        stderr = str(p.get("stderr", "") or "").lower()
        combined = f"{stdout}\n{stderr}"

        if s == "error": 
            return "syntax_error"
        if s == "success":
            if "refine:" in stdout or "refine:" in combined:
                return "semantic_error"
            if "status: unsat" in combined:
                return "semantic_error"
            return "success"
        return "semantic_error"


class ClingoClassifier(BaseSolverClassifier):
    def classify_run(self) -> tuple[str, str]:
        if self._has_overthinking():
            return "overthinking", "output tokens exceeded threshold"

        if not self.payloads:
            if "Translator failed" in self.full_text:
                return "translator_failed", "no payloads, translator failed"
            return "semantic_error", "no result payloads found"

        has_error = False
        has_unsat = False
        has_sat = False
        has_refinement = False
        has_timeout = False
        has_unknown = False

        for p in self.payloads:
            status = str(p.get("status", "")).lower().strip()
            if status in ("error", "syntax_error"):
                has_error = True
            elif status == "unsatisfiable":
                has_unsat = True
            elif status in ("satisfiable", "optimum_found"):
                has_sat = True
            elif status in ("timeout", "grounding_timeout"):
                has_timeout = True
            elif status == "unknown":
                has_unknown = True
            
            stdout = str(p.get("stdout", "") or "")
            if "refine" in stdout.lower():
                has_refinement = True

        if "Translator failed" in self.full_text:
            if has_error and not has_sat:
                return "syntax_error", "error + translator failed"
            if has_unsat and not has_sat:
                return "semantic_error", "unsatisfiable -> translator failed (bad encoding)"
            if has_refinement:
                return "semantic_error", "refinement -> translator failed"
            if has_timeout and not has_sat:
                return "semantic_error", "timeout + translator failed (encoding too complex)"
            if has_unknown and not has_sat:
                return "semantic_error", "unknown + translator failed"
            return "translator_failed", "translator failed"

        last = self.payloads[-1]
        last_status = str(last.get("status", "")).lower().strip()

        if last_status in ("error", "syntax_error"):
            error_detail = str(last.get('error', last.get('stderr', '')))[:80]
            return "syntax_error", f"clingo error: {error_detail}"
        if last_status == "unsatisfiable":
            if has_sat:
                return "success", "recovered from unsat"
            return "semantic_error", "clingo returned unsatisfiable"
        if last_status in ("satisfiable", "optimum_found"):
            return "success", "clingo satisfiable"
        if last_status in ("timeout", "grounding_timeout"):
            if has_sat:
                return "success", "recovered from timeout"
            return "semantic_error", f"clingo {last_status} (encoding too complex)"
        if last_status == "unknown":
            if has_sat:
                return "success", "recovered from unknown"
            return "semantic_error", "clingo unknown status"

        if has_sat:
            return "success", "found satisfiable in iterations"
        if has_unsat:
            return "semantic_error", "only unsatisfiable results"
        if has_error:
            return "syntax_error", "only errors"
        if has_timeout:
            return "semantic_error", "only timeouts"
        if has_unknown:
            return "semantic_error", "only unknown results"

        return "semantic_error", f"unknown clingo status: {last_status}"

    def classify_payload(self, p: dict) -> str:
        s = str(p.get("status", "")).lower()
        if s == "syntax_error": return "syntax_error"
        if s in ("satisfiable", "optimum_found"): return "success"
        return "semantic_error"


class VampireClassifier(BaseSolverClassifier):
    def classify_run(self) -> tuple[str, str]:
        if self._has_overthinking():
            return "overthinking", "output tokens exceeded threshold"

        if not self.payloads:
            if "Translator failed" in self.full_text:
                return "translator_failed", "no payloads, translator failed"
            return "semantic_error", "no result payloads found"

        has_error = False
        has_success = False
        has_timeout = False
        has_unknown = False

        valid_szs = {"theorem", "unsatisfiable", "satisfiable", "countersatisfiable"}

        for p in self.payloads:
            pos = p.get("positive", {}) if isinstance(p.get("positive"), dict) else {}
            neg = p.get("negative", {}) if isinstance(p.get("negative"), dict) else {}
            ps = str(pos.get("status", "")).lower().strip()
            ns = str(neg.get("status", "")).lower().strip()
            p_szs = str(pos.get("szs_status", "")).lower().strip().replace("_", "")
            n_szs = str(neg.get("szs_status", "")).lower().strip().replace("_", "")

            if ps == "error" or ns == "error": has_error = True
            if ps == "success" or ns == "success":
                if p_szs in valid_szs or n_szs in valid_szs:
                    has_success = True
            if ps == "timeout" or ns == "timeout" or "timeout" in p_szs or "timeout" in n_szs:
                has_timeout = True
            if p_szs == "unknown" or n_szs == "unknown":
                has_unknown = True

        last = self.payloads[-1]
        positive = last.get("positive", {}) if isinstance(last.get("positive"), dict) else {}
        negative = last.get("negative", {}) if isinstance(last.get("negative"), dict) else {}

        pos_status = str(positive.get("status", "")).lower().strip()
        neg_status = str(negative.get("status", "")).lower().strip()
        pos_szs = str(positive.get("szs_status", "")).lower().strip().replace("_", "")
        neg_szs = str(negative.get("szs_status", "")).lower().strip().replace("_", "")

        if pos_status == "error" or neg_status == "error":
            pos_stderr = str(positive.get("stderr", "") or "")
            neg_stderr = str(negative.get("stderr", "") or "")
            if "syntax" in pos_stderr.lower() or "syntax" in neg_stderr.lower():
                return "syntax_error", "vampire syntax error in stderr"
            if "syntaxerror" in pos_szs or "syntaxerror" in neg_szs:
                return "syntax_error", "vampire SZS SyntaxError"
            if has_success:
                return "syntax_error", "vampire error (regression from earlier success)"
            return "syntax_error", "vampire error status"

        if pos_status == "timeout" or neg_status == "timeout":
            if has_success:
                return "success", "recovered from timeout in earlier iteration"
            return "semantic_error", f"vampire timeout: pos={pos_szs}, neg={neg_szs}"

        if "syntaxerror" in pos_szs or "syntaxerror" in neg_szs:
            return "syntax_error", f"SZS SyntaxError: pos={pos_szs}, neg={neg_szs}"
        if pos_szs == "contradictoryaxioms" or neg_szs == "contradictoryaxioms":
            return "semantic_error", f"ContradictoryAxioms: pos={pos_szs}, neg={neg_szs}"

        decisive = {"theorem", "unsatisfiable"}
        if pos_szs in decisive and neg_szs in decisive:
            return "semantic_error", f"inconsistent premises: pos={pos_szs}, neg={neg_szs}"

        if pos_szs in valid_szs or neg_szs in valid_szs:
            return "success", f"pos={pos_szs}, neg={neg_szs}"

        if "timeout" in pos_szs or "timeout" in neg_szs:
            if has_success:
                return "success", "recovered from SZS timeout in earlier iteration"
            if "Translator failed" in self.full_text:
                return "semantic_error", f"timeout + translator failed: pos={pos_szs}, neg={neg_szs}"
            return "semantic_error", f"timeout: pos={pos_szs}, neg={neg_szs}"

        if pos_szs == "unknown" or neg_szs == "unknown":
            if has_success:
                return "success", "recovered from unknown in earlier iteration"
            if "Translator failed" in self.full_text:
                return "semantic_error", f"unknown + translator failed: pos={pos_szs}, neg={neg_szs}"
            return "semantic_error", f"unknown szs: pos={pos_szs}, neg={neg_szs}"

        if "Translator failed" in self.full_text:
            if has_error and not has_success:
                return "syntax_error", "error + translator failed"
            if has_timeout and not has_success:
                return "semantic_error", "timeout + translator failed"
            if has_unknown and not has_success:
                return "semantic_error", "unknown + translator failed"
            return "translator_failed", f"translator failed: pos={pos_szs}, neg={neg_szs}"

        if pos_szs or neg_szs:
            return "semantic_error", f"non-decisive szs: pos={pos_szs}, neg={neg_szs}"

        raw_status = str(last.get("status", "")).lower().strip()
        if raw_status == "success": return "success", "simple vampire success"
        if raw_status == "error": return "syntax_error", "simple vampire error"
        if raw_status == "timeout": return "semantic_error", "simple vampire timeout"

        return "semantic_error", "unparseable vampire result"

    def classify_payload(self, p: dict) -> str:
        pos = p.get("positive", {}) if isinstance(p.get("positive"), dict) else {}
        neg = p.get("negative", {}) if isinstance(p.get("negative"), dict) else {}
        ps = str(pos.get("status", "")).lower().strip()
        ns = str(neg.get("status", "")).lower().strip()
        p_szs = str(pos.get("szs_status", "")).lower().strip().replace("_", "")
        n_szs = str(neg.get("szs_status", "")).lower().strip().replace("_", "")

        valid_szs = {"theorem", "unsatisfiable", "satisfiable", "countersatisfiable"}
        if ps == "success" or ns == "success":
            if p_szs in valid_szs or n_szs in valid_szs:
                return "success"
        if ps == "error" or ns == "error":
            return "syntax_error"
        return "semantic_error"


class FallbackClassifier(BaseSolverClassifier):
    def classify_run(self) -> tuple[str, str]:
        if "Translator failed" in self.full_text:
            return "translator_failed", "unknown solver"
        if self.payloads:
            last_status = str(self.payloads[-1].get("status", "")).lower()
            if last_status == "error":
                return "syntax_error", "error status"
            return "success", "has payloads"
        return "semantic_error", "unknown solver, no payloads"
    
    def classify_payload(self, p: dict) -> str:
        ps = str(p.get("status", "")).lower()
        return "syntax_error" if ps == "error" else "success"


def get_classifier(solver: str, text: str) -> BaseSolverClassifier:
    solver_lower = solver.lower().strip()
    if solver_lower == "z3": return Z3Classifier(text)
    if solver_lower == "clingo": return ClingoClassifier(text)
    if solver_lower == "vampire": return VampireClassifier(text)
    return FallbackClassifier(text)


def classify_iterations(solver: str, path: Path) -> list[str]:
    """Extract and classify every #### Result block in a file for iteration-level tracking."""
    if not path.exists(): return []
    text = path.read_text(encoding="utf-8", errors="replace")
    
    matches = list(re.finditer(r'#### Result\s+(.*?)\s+(?=#### Result|###|$)', text, re.DOTALL))
    classifier = get_classifier(solver, text)
    solver_lower = solver.lower().strip()
    
    statuses = []
    for i, match in enumerate(matches):
        block = match.group(1)
        payload = classifier._parse_tool_result_payload(block)
        if not payload:
            continue
            
        status = classifier.classify_payload(payload)
        
        # Iteration-level refinement overrides for Z3 and Clingo
        if status == "success":
            start_next = matches[i+1].start() if i+1 < len(matches) else len(text)
            after_text = text[match.end():start_next]
            if solver_lower == "clingo":
                if any(x in after_text for x in ["Refining to find", "intersection yielded", "Refinement triggered", "Refine:"]):
                    status = "semantic_error"
            elif solver_lower == "z3":
                if any(x in after_text for x in ["Refinement triggered", "Refine:", "Refining to find"]):
                    status = "semantic_error"
        
        statuses.append(status)
    
    if classifier._has_overthinking():
        statuses.append("overthinking")
        
    return statuses


# --- Scanning Logic ---------------------------------------------------------
class ResultScanner:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def scan_all(self) -> list[RunRecord]:
        records: list[RunRecord] = []
        if not self.root_dir.exists():
            print(f"[ERROR] directory not found at {self.root_dir.resolve()}", file=sys.stderr)
            sys.exit(1)

        for provider_dir in sorted(self.root_dir.iterdir()):
            if not provider_dir.is_dir(): continue
            provider = provider_dir.name

            for bench_dir in sorted(provider_dir.iterdir()):
                if not bench_dir.is_dir(): continue
                benchmark = bench_dir.name

                for problem_dir in sorted(bench_dir.iterdir()):
                    if not problem_dir.is_dir(): continue
                    problem = problem_dir.name

                    for solver_dir in sorted(problem_dir.iterdir()):
                        if not solver_dir.is_dir(): continue
                        solver = solver_dir.name

                        index_path = solver_dir / "index.md"
                        result_jsonl_path = solver_dir / "result.jsonl"
                        
                        is_translator_failed = self._check_translator_failed(result_jsonl_path)
                        iteration_statuses = classify_iterations(solver, index_path)
                        status, detail = self._classify_run(solver, index_path)
                        
                        records.append(RunRecord(
                            provider=provider, benchmark=benchmark,
                            problem=problem, solver=solver,
                            status=status, detail=detail,
                            is_translator_failed=is_translator_failed,
                            iteration_statuses=iteration_statuses,
                        ))
        return records

    def _check_translator_failed(self, jsonl_path: Path) -> bool:
        if jsonl_path.exists():
            try:
                with open(jsonl_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            if "Translator failed" in str(data.get("model_answer", "") or ""):
                                return True
                            break
            except Exception as e:
                print(f"[WARN] Failed to parse {jsonl_path}: {e}")
        return False

    def _classify_run(self, solver: str, index_path: Path) -> tuple[str, str]:
        if not index_path.exists():
            return "semantic_error", "index.md not found"
        try:
            text = index_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return "semantic_error", f"read error: {e}"
        if not text.strip():
            return "semantic_error", "empty file"

        classifier = get_classifier(solver, text)
        return classifier.classify_run()


# --- Report Generators ------------------------------------------------------
def _pad(s: str, width: int) -> str: return s.ljust(width)
def _rpad(s: str, width: int) -> str: return s.rjust(width)

class ConsoleReporter:
    def __init__(self, records: list[RunRecord]):
        self.records = records

    def print_summary_table(self, group_key: str, title: str, group_order: list[str] | None = None):
        counter: dict[str, Counter] = defaultdict(Counter)
        for r in self.records:
            key = getattr(r, group_key)
            counter[key][r.status] += 1

        if group_order:
            keys = [k for k in group_order if k in counter]
            keys += [k for k in sorted(counter) if k not in keys]
        else:
            keys = sorted(counter)

        group_width = max(len(title), max((len(k) for k in keys), default=10))
        col_width = max(12, max(len(s) for s in STATUS_ORDER))

        header = _pad(title, group_width)
        for s in STATUS_ORDER: header += " | " + _rpad(s, col_width)
        header += " | " + _rpad("TOTAL", col_width)
        
        print("\n" + header)
        print("-" * len(header))

        for k in keys:
            row = _pad(k, group_width)
            total = 0
            for s in STATUS_ORDER:
                count = counter[k].get(s, 0)
                total += count
                row += " | " + _rpad(str(count), col_width)
            row += " | " + _rpad(str(total), col_width)
            print(row)

        print("-" * len(header))
        row = _pad("TOTAL", group_width)
        grand = 0
        for s in STATUS_ORDER:
            col_total = sum(counter[k].get(s, 0) for k in keys)
            grand += col_total
            row += " | " + _rpad(str(col_total), col_width)
        row += " | " + _rpad(str(grand), col_width)
        print(row)

    def print_hierarchical_report(self):
        tree: dict[str, dict[str, dict[str, Counter]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(Counter))
        )
        for r in self.records:
            tree[r.provider][r.benchmark][r.solver][r.status] += 1

        col_width = max(10, max(len(s) for s in STATUS_ORDER))
        status_header = " | ".join(_rpad(s, col_width) for s in STATUS_ORDER)
        full_header_width = 40 + 3 + len(status_header) + 3 + col_width

        providers = [p for p in PROVIDERS_ORDER if p in tree]
        providers += [p for p in sorted(tree) if p not in providers]

        for provider in providers:
            label = PROVIDER_LABELS.get(provider, provider)
            print(f"\n{'=' * full_header_width}")
            print(f"  PROVIDER: {provider} ({label})")
            print(f"{'=' * full_header_width}")

            benchmarks = [b for b in BENCHMARK_ORDER if b in tree[provider]]
            benchmarks += [b for b in sorted(tree[provider]) if b not in benchmarks]

            for benchmark in benchmarks:
                print(f"\n  +- Benchmark: {benchmark}")
                print(f"  |  {'Solver':<34} | {status_header} | {'TOTAL':>{col_width}}")
                print(f"  |  {'-' * 34}-+-{'-' * len(status_header)}-+-{'-' * col_width}")

                solvers = [s for s in SOLVER_ORDER if s in tree[provider][benchmark]]
                solvers += [s for s in sorted(tree[provider][benchmark]) if s not in solvers]

                bench_totals: Counter = Counter()
                for solver in solvers:
                    cnts = tree[provider][benchmark][solver]
                    total = sum(cnts.values())
                    cols = " | ".join(_rpad(str(cnts.get(s, 0)), col_width) for s in STATUS_ORDER)
                    print(f"  |  {solver:<34} | {cols} | {_rpad(str(total), col_width)}")
                    bench_totals += cnts

                total = sum(bench_totals.values())
                cols = " | ".join(_rpad(str(bench_totals.get(s, 0)), col_width) for s in STATUS_ORDER)
                print(f"  |  {'-' * 34}-+-{'-' * len(status_header)}-+-{'-' * col_width}")
                print(f"  +- {'SUBTOTAL':<34} | {cols} | {_rpad(str(total), col_width)}")

    def print_error_details(self, all_records: list[RunRecord], max_per_status: int = 5):
        by_status: dict[str, list[RunRecord]] = defaultdict(list)
        for r in all_records:
            if r.status != "success":
                by_status[r.status].append(r)

        print(f"\n{'=' * 80}")
        print(f"  ERROR / NON-SUCCESS SAMPLE DETAILS (up to {max_per_status} samples each)")
        print(f"{'=' * 80}")

        for status in STATUS_ORDER:
            if status == "success": continue
            recs = by_status.get(status, [])
            if not recs: continue

            print(f"\n  -- {status.upper()} ({len(recs)} total) --")
            for r in recs[:max_per_status]:
                print(f"     {r.provider}/{r.benchmark}/{r.problem}/{r.solver}")
                detail_safe = r.detail.encode("ascii", errors="replace").decode("ascii")
                print(f"       -> {detail_safe[:120]}")

    def print_quick_summary(self, all_records: list[RunRecord]):
        total_runs = len(all_records)
        trans_failed = sum(1 for r in all_records if r.is_translator_failed)
        
        all_iterations = []
        for r in all_records:
            if r.status != "translator_failed":
                all_iterations.extend(r.iteration_statuses)
        
        total_iters = len(all_iterations)
        counts = Counter(all_iterations)

        print(f"\n{'=' * 60}")
        print("  QUICK SUMMARY (ITERATION LEVEL)")
        print(f"{'=' * 60}")
        print(f"  Total runs:          {total_runs:>6}")
        print(f"  Translator failed:   {trans_failed:>6}  ({100*trans_failed/total_runs:.1f}% of runs)")
        print(f"  Total iterations:    {total_iters:>6}  (excl. plain translator failures)")
        print(f"  {'---':>23}")
        for s in STATUS_ORDER:
            c = counts.get(s, 0)
            pct = 100 * c / total_iters if total_iters > 0 else 0
            label = s.replace("_", " ").title()
            print(f"  {label + ':':<23}{c:>6}  ({pct:.1f}%)")
        print(f"{'=' * 60}")
        print("\n  NOTE: 'translator_failed' rate is from result.jsonl.")
        print("        'overthinking' is counted in main status bars from index.md.")
        print("        'semantic_error' includes refinement loops, unsatisfiable,")
        print("        timeout, unknown, and any run where the solver logic was wrong.")


class MarkdownReportGenerator:
    def __init__(self, records: list[RunRecord]):
        self.records = records

    def generate(self, out_dir: Path):
        df = pd.DataFrame([vars(r) for r in self.records])
        if df.empty: return
            
        df["status_normalized"] = df["status"]
        df["Model"] = df["provider"].map(PROVIDER_LABELS)
        
        df["Reasoning"] = df["provider"].map(lambda x: CATEGORIES.get(x, {}).get("reasoning", "Unknown"))
        df["Size"] = df["provider"].map(lambda x: CATEGORIES.get(x, {}).get("size", "Unknown"))
        df["ProviderGroup"] = df["provider"].map(lambda x: CATEGORIES.get(x, {}).get("provider", "Unknown"))
        df["All Models"] = "All Models"
        
        aggs = ["All Models", "Reasoning", "Size", "ProviderGroup"]
        
        report_path = out_dir / "mcp_status_detailed_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# MCP Status Detailed Report\n")
            
            solvers = ["clingo", "vampire", "z3", "ALL"]
            for solver in solvers:
                f.write(f"\n## Solver: {solver}\n")
                
                if solver == "ALL": df_solver = df.copy()
                else: df_solver = df[df["solver"] == solver].copy()
                    
                if df_solver.empty:
                    f.write("No data for this solver.\n")
                    continue
                    
                for agg in aggs:
                    f.write(f"\n### Aggregated by {agg}\n")
                    unique_vals = df_solver[agg].unique()
                    
                    for val in unique_vals:
                        sub_df = df_solver[df_solver[agg] == val].copy()
                        if sub_df.empty: continue
                            
                        f.write(f"\n#### {agg}: {val}\n\n")
                    
                        agg_df = sub_df.groupby(["Model"]).agg(
                            total_runs=("provider", "count")
                        ).reset_index()
                        
                        status_pivot = sub_df.pivot_table(index="Model", columns="status", aggfunc="size", fill_value=0)
                        merged = agg_df.set_index("Model").join(status_pivot).fillna(0)
                        
                        status_cols = ["success", "semantic_error", "syntax_error", "overthinking"]
                        for col in status_cols:
                            if col not in merged.columns: merged[col] = 0
                                
                        merged["total_for_status"] = merged[status_cols].sum(axis=1)
                        
                        merged["Success %"] = (merged["success"] / merged["total_for_status"] * 100).round(2)
                        merged["Semantic Error %"] = (merged["semantic_error"] / merged["total_for_status"] * 100).round(2)
                        merged["Syntax Error %"] = (merged["syntax_error"] / merged["total_for_status"] * 100).round(2)
                        merged["Overthinking %"] = (merged["overthinking"] / merged["total_for_status"] * 100).round(2)
                        
                        merged = merged.reset_index()
                        
                        outcomes_cols = ["Model", "Success %", "Semantic Error %", "Syntax Error %", "Overthinking %"]
                        outcomes_table = merged[outcomes_cols].copy()
                        
                        avg_row_outcomes = {"Model": "Average"}
                        for col in outcomes_cols[1:]:
                            avg_row_outcomes[col] = outcomes_table[col].mean().round(2)
                        outcomes_table = pd.concat([outcomes_table, pd.DataFrame([avg_row_outcomes])], ignore_index=True)
                        
                        f.write("#### Execution Outcomes\n")
                        f.write(outcomes_table.to_markdown(index=False) + "\n\n")


class CSVExporter:
    @staticmethod
    def export(records: list[RunRecord], output_path: Path):
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["provider", "benchmark", "problem", "solver", "status", "detail"])
            for r in records:
                writer.writerow([r.provider, r.benchmark, r.problem, r.solver, r.status, r.detail])
        print(f"\n[INFO] Full CSV exported to: {output_path}")


# --- Main -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Analyze MCP solver status across providers/benchmarks/solvers.")
    parser.add_argument("--provider", type=str, help="Analyze only this provider (e.g. 'google').")
    parser.add_argument("--csv", type=str, default="analysis_outputs/mcp_status_report.csv", help="CSV output path")
    parser.add_argument("--errors", action="store_true", help="Show sample error details.")
    args = parser.parse_args()

    print("[INFO] Scanning output_mcp directory tree...")
    scanner = ResultScanner(OUTPUT_MCP)
    all_records = scanner.scan_all()

    if args.provider:
        all_records = [r for r in all_records if r.provider == args.provider]
        if not all_records:
            print(f"[WARN] No records found for provider '{args.provider}'.")
            return

    print(f"[INFO] Found {len(all_records)} solver runs across all providers.\n")

    # Separate translator_failed from result records for main status tables
    result_records = [r for r in all_records if r.status != "translator_failed"]
    trans_failed_count = len(all_records) - len(result_records)
    print(f"[INFO] Result runs: {len(result_records)} | Translator failed: {trans_failed_count}\n")

    reporter = ConsoleReporter(result_records)
    reporter.print_summary_table("provider", "PROVIDER", PROVIDERS_ORDER)
    reporter.print_summary_table("benchmark", "BENCHMARK", BENCHMARK_ORDER)
    reporter.print_summary_table("solver", "SOLVER", SOLVER_ORDER)
    reporter.print_hierarchical_report()

    if args.errors:
        reporter.print_error_details(all_records)

    csv_path = Path(args.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    CSVExporter.export(all_records, csv_path)

    md_generator = MarkdownReportGenerator(all_records)
    md_generator.generate(csv_path.parent)

    ConsoleReporter(all_records).print_quick_summary(all_records)


if __name__ == "__main__":
    main()
