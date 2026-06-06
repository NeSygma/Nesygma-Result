from z3 import *

# Teams: A=0, B=1, C=2, D=3, E=4
teams = ['A', 'B', 'C', 'D', 'E']
n = len(teams)

# Match results: (winner, loser) pairs
matches = [
    (0, 1),  # A beat B
    (1, 2),  # B beat C
    (2, 0),  # C beat A (cycle!)
    (0, 3),  # A beat D
    (3, 4),  # D beat E
    (4, 2),  # E beat C
    (1, 4),  # B beat E
    (3, 2),  # D beat C
    (0, 4),  # A beat E
    (1, 3),  # B beat D
]

# Create optimizer
opt = Optimize()

# Rank variables: rank[i] = position of team i (1 = best, 5 = worst)
rank = [Int(f'rank_{teams[i]}') for i in range(n)]

# Constraint 1: Each team has a unique rank between 1 and 5
for i in range(n):
    opt.add(rank[i] >= 1, rank[i] <= n)
opt.add(Distinct(rank))

# Violation indicator for each match
# A violation occurs when winner is ranked LOWER (higher number) than loser
violations = []
for idx, (w, l) in enumerate(matches):
    v = Int(f'violation_{idx}')
    # v = 1 if winner ranked lower (higher number) than loser, else 0
    opt.add(v == If(rank[w] > rank[l], 1, 0))
    opt.add(v >= 0, v <= 1)
    violations.append(v)

# Total violations
total_violations = Sum(violations)
opt.add(total_violations >= 0, total_violations <= len(matches))

# Objective: minimize total violations
opt.minimize(total_violations)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract ranking
    rank_values = []
    for i in range(n):
        rank_values.append((teams[i], m[rank[i]].as_long()))
    
    # Sort by rank (ascending = best first)
    rank_values.sort(key=lambda x: x[1])
    
    print("Optimal Ranking (1st to 5th):")
    for pos, (team, r) in enumerate(rank_values, 1):
        print(f"  Position {pos}: Team {team} (rank={r})")
    
    # Count violations
    total_v = m.eval(total_violations).as_long()
    print(f"\nTotal Violations: {total_v}")
    
    # Show which matches are violations
    print("\nViolation Details:")
    for idx, (w, l) in enumerate(matches):
        v_val = m.eval(violations[idx]).as_long()
        if v_val == 1:
            print(f"  {teams[w]} beat {teams[l]} -> VIOLATION (winner {teams[w]} ranked lower)")
    
    print(f"\nvalid: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")