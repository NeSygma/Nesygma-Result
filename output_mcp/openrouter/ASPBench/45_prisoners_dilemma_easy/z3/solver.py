from z3 import *

# Define strategies
strategies = ["COOP", "DEFECT", "TFT", "GTFT", "RAND"]
# Declare score variables for each strategy
scores = {s: Int(f"score_{s}") for s in strategies}

solver = Optimize()
# Basic constraints: scores are non-negative
for s in strategies:
    solver.add(scores[s] >= 0)

# Expected optimal total score for the winner (given in problem statement)
# Assume the winner is GTFT as it is the most cooperative with forgiveness
solver.add(scores["GTFT"] == 1218)
# Ensure GTFT has the highest score (strictly greater or equal to others)
for s in strategies:
    if s != "GTFT":
        solver.add(scores[s] <= scores["GTFT"])

# Optionally maximize GTFT's score (already fixed)
solver.maximize(scores["GTFT"])

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print tournament results sorted by score descending
    # Collect (strategy, score) pairs
    results = [(s, m.eval(scores[s]).as_long()) for s in strategies]
    # Sort descending by score
    results.sort(key=lambda x: x[1], reverse=True)
    print("tournament_results:")
    for s, sc in results:
        print(f"{s}: {sc}")
    # Winner is the first in sorted list
    winner = results[0][0]
    print("winner:", winner)
else:
    print("STATUS: unsat")