from z3 import *

# Teams
teams = ['A','B','C','D','E']
# Create rank variables for each team (1..5)
rank = {t: Int(f'rank_{t}') for t in teams}

solver = Optimize()
# Domain constraints
for t in teams:
    solver.add(rank[t] >= 1, rank[t] <= 5)
# All different ranks
solver.add(Distinct([rank[t] for t in teams]))

# Match results list of (winner, loser)
matches = [
    ('A','B'),
    ('B','C'),
    ('C','A'),
    ('A','D'),
    ('D','E'),
    ('E','C'),
    ('B','E'),
    ('D','C'),
    ('A','E'),
    ('B','D')
]
# Violation indicator for each match
viols = []
for w,l in matches:
    v = If(rank[w] > rank[l], 1, 0)
    viols.append(v)
# Total violations
total_viol = Sum(viols)
# Minimize
solver.minimize(total_viol)

result = solver.check()
if result == sat:
    m = solver.model()
    # Extract ranking order
    ranking = sorted(teams, key=lambda t: m[rank[t]].as_long())
    violations = m.eval(total_viol).as_long()
    print("STATUS: sat")
    print("ranking =", ranking)
    print("violations =", violations)
    print("valid =", True)
else:
    print("STATUS: unsat")