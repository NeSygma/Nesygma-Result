from z3 import *

# Define teams indices
teams = ['A', 'B', 'C', 'D', 'E']
team_index = {name: i for i, name in enumerate(teams)}

# Match results: (winner, loser)
matches = [
    (team_index['A'], team_index['B']),
    (team_index['B'], team_index['C']),
    (team_index['C'], team_index['A']),
    (team_index['A'], team_index['D']),
    (team_index['D'], team_index['E']),
    (team_index['E'], team_index['C']),
    (team_index['B'], team_index['E']),
    (team_index['D'], team_index['C']),
    (team_index['A'], team_index['E']),
    (team_index['B'], team_index['D']),
]

# Create solver
opt = Optimize()

# Position of each team in ranking (0 = first place)
pos = [Int(f'pos_{i}') for i in range(len(teams))]
for p in pos:
    opt.add(p >= 0, p <= len(teams)-1)
opt.add(Distinct(pos))

# Violations variable
violations = Int('violations')
# Compute violations as sum of 1 for each match where loser ranked higher
violation_terms = []
for winner, loser in matches:
    # violation if pos[loser] < pos[winner]
    violation_terms.append(If(pos[loser] < pos[winner], 1, 0))
opt.add(violations == Sum(violation_terms))

# Objective: minimize violations
opt.minimize(violations)

# Check and get model
result = opt.check()
if result == sat:
    model = opt.model()
    # Extract ranking list from positions
    ranking = [None]*len(teams)
    for t in range(len(teams)):
        p_val = model[pos[t]].as_long()
        ranking[p_val] = teams[t]
    # Compute violations value
    viol_val = model[violations].as_long()
    print("STATUS: sat")
    print("ranking = [" + ", ".join(ranking) + "]")
    print("violations =", viol_val)
    print("valid = true")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("STATUS: unknown")