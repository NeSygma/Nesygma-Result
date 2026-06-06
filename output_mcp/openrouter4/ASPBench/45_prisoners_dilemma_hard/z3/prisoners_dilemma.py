from z3 import *

# Create an optimizer
opt = Optimize()

# Strategy choice: 0=COOP, 1=DEFECT, 2=TFT
choice = Int('choice')
opt.add(choice >= 0)
opt.add(choice <= 2)

# Payoff matrix values per round:
# (Ego, Opponent) -> Ego's score for that round
# (C,C) = 3, (D,C) = 5, (C,D) = 0, (D,D) = 1

# Opponent counts
nA = 5  # type_A: Always Defect
nB = 3  # type_B: Tit-for-Tat
nC = 2  # type_C: Forgiving TFT

# --- Score against type_A (Always Defect) ---
# type_A always plays D in round 1 and round 2
# Ego COOP (0): R1: C vs D = 0, R2: C vs D = 0 => total 0
# Ego DEFECT (1): R1: D vs D = 1, R2: D vs D = 1 => total 2
# Ego TFT (2): R1: C vs D = 0, R2: copies opp's R1 = D, so D vs D = 1 => total 1
score_vs_A = If(choice == 0, 0,
                If(choice == 1, 2, 1))

# --- Score against type_B (Tit-for-Tat) ---
# type_B: R1: C, R2: copies Ego's R1
# Ego COOP (0): R1: C vs C = 3, R2: C vs (copies Ego R1 = C) = C vs C = 3 => total 6
# Ego DEFECT (1): R1: D vs C = 5, R2: D vs (copies Ego R1 = D) = D vs D = 1 => total 6
# Ego TFT (2): R1: C vs C = 3, R2: copies opp R1 = C, opp copies Ego R1 = C => C vs C = 3 => total 6
score_vs_B = If(choice == 0, 6,
                If(choice == 1, 6, 6))

# --- Score against type_C (Forgiving TFT) ---
# type_C: R1: C, R2: C (regardless)
# Ego COOP (0): R1: C vs C = 3, R2: C vs C = 3 => total 6
# Ego DEFECT (1): R1: D vs C = 5, R2: D vs C = 5 => total 10
# Ego TFT (2): R1: C vs C = 3, R2: copies opp R1 = C, opp C => C vs C = 3 => total 6
score_vs_C = If(choice == 0, 6,
                If(choice == 1, 10, 6))

# Total expected score
total_score = nA * score_vs_A + nB * score_vs_B + nC * score_vs_C

# Maximize the total score
opt.maximize(total_score)

# Check
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    chosen = m[choice].as_long()
    score_val = m.eval(total_score).as_long()
    
    # Map integer back to strategy name
    strategy_names = {0: "COOP", 1: "DEFECT", 2: "TFT"}
    best_strategy = strategy_names[chosen]
    
    print("STATUS: sat")
    print(f"best_strategy_choice={best_strategy}")
    print(f"expected_total_score={score_val}")
    
    # Also compute scores for all strategies for output
    print("\nExpected scores:")
    for c in [0, 1, 2]:
        name = strategy_names[c]
        # Compute score by substituting choice
        s = opt.model().eval(nA * score_vs_A + nB * score_vs_B + nC * score_vs_C).as_long()
        # But eval with substitution
        # Better to compute directly
        pass
    
    # Let's recompute all scores explicitly
    for c, name in [(0, "COOP"), (1, "DEFECT"), (2, "TFT")]:
        s_A = 0 if c == 0 else (2 if c == 1 else 1)
        s_B = 6
        s_C = 6 if c != 1 else 10
        total = nA * s_A + nB * s_B + nC * s_C
        print(f"  {name}: {total}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")