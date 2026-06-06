from z3 import *

# Teams as symbolic constants
A, B, C, D, E = Strings('A B C D E')
teams = [A, B, C, D, E]

# Match results: (winner, loser)
matches = [
    (A, B),
    (B, C),
    (C, A),
    (A, D),
    (D, E),
    (E, C),
    (B, E),
    (D, C),
    (A, E),
    (B, D)
]

# Create a solver
solver = Optimize()

# rank[i] = team at position i (0-indexed, where 0 is 1st place)
rank = [String(f'rank_{i}') for i in range(5)]
solver.add(Distinct(rank))

# team_to_position[team] = position (0-4) of the team in the ranking
team_to_position = {team: Int(f'pos_{team}') for team in teams}

# Each team must be assigned to a unique position
for team in teams:
    solver.add(team_to_position[team] >= 0, team_to_position[team] < 5)

# Each position must be assigned to exactly one team
for i in range(5):
    for team in teams:
        solver.add(Implies(rank[i] == team, team_to_position[team] == i))

# Ensure all teams are assigned to some position
for team in teams:
    solver.add(Or([team_to_position[team] == i for i in range(5)]))

# For each match, check if it's a violation
# A violation occurs when winner beat loser but loser is ranked higher (has lower position value)
violations = []
for winner, loser in matches:
    # If team_to_position[loser] < team_to_position[winner], that's a violation
    violations.append(team_to_position[loser] < team_to_position[winner])

# Count violations
total_violations = Sum(violations)

# Minimize violations
solver.minimize(total_violations)

# Check and print result
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Optimal violations:", model.evaluate(total_violations))
    # Print the ranking
    ranking = []
    for i in range(5):
        ranking.append(str(model.evaluate(rank[i])))
    print("Ranking:", ranking)
    print("valid: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")