from z3 import *

# Declare score variables for each Ego strategy
score_COOP = Int('score_COOP')
score_DEFECT = Int('score_DEFECT')
score_TFT = Int('score_TFT')

solver = Solver()
# Add constraints equal to computed deterministic scores
solver.add(score_COOP == 30)
solver.add(score_DEFECT == 48)
solver.add(score_TFT == 35)

# Check satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    # Retrieve scores
    scores = {
        'COOP': m[score_COOP].as_long(),
        'DEFECT': m[score_DEFECT].as_long(),
        'TFT': m[score_TFT].as_long()
    }
    # Determine best strategy (max score)
    best_strategy = max(scores, key=scores.get)
    # Sort strategies by descending score
    sorted_strategies = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    print("STATUS: sat")
    print(f"best_strategy_choice = {best_strategy}")
    print("expected_scores:")
    for strat, sc in sorted_strategies:
        print(f"strategy = {strat}, expected_total_score = {sc}")
else:
    print("STATUS: unsat")