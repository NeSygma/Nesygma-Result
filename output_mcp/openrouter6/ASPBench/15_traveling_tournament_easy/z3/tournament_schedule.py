from z3 import *

# Teams and coordinates
teams = ['A', 'B', 'C', 'D']
team_coords = [(0,0), (3,4), (6,0), (2,8)]
team_index = {t: i for i, t in enumerate(teams)}

# Distance matrix (given)
dist = [
    [0, 5, 6, 8.2],
    [5, 0, 5, 5.7],
    [6, 5, 0, 10],
    [8.2, 5.7, 10, 0]
]

# Generate all possible round configurations (12 total)
# Each configuration is a tuple of two matches: (home0, away0), (home1, away1)
configs = []

# Pairings: (0,1) vs (2,3), (0,2) vs (1,3), (0,3) vs (1,2)
pairings = [
    [(0,1), (2,3)],
    [(0,2), (1,3)],
    [(0,3), (1,2)]
]

for pairing in pairings:
    (p0a, p0b), (p1a, p1b) = pairing
    # Four home/away assignments for this pairing
    configs.append(((p0a, p0b), (p1a, p1b)))  # both first teams home
    configs.append(((p0a, p0b), (p1b, p1a)))  # first match home, second match swapped
    configs.append(((p0b, p0a), (p1a, p1b)))  # first match swapped, second home
    configs.append(((p0b, p0a), (p1b, p1a)))  # both swapped

print(f"Total configurations: {len(configs)}")

# Create solver
solver = Optimize()

# Variables: which configuration for each round (0-5)
config_vars = [Int(f'config_{r}') for r in range(6)]
for cv in config_vars:
    solver.add(cv >= 0, cv <= 11)

# Helper to get match details from config index
def get_matches(config_idx):
    home0, away0 = configs[config_idx][0]
    home1, away1 = configs[config_idx][1]
    return home0, away0, home1, away1

# For each round, define home/away teams using config
home0 = [Int(f'home0_{r}') for r in range(6)]
away0 = [Int(f'away0_{r}') for r in range(6)]
home1 = [Int(f'home1_{r}') for r in range(6)]
away1 = [Int(f'away1_{r}') for r in range(6)]

# Link config vars to match variables
for r in range(6):
    # For each possible config, enforce equality if config_vars[r] equals that config
    # Use Or over all configs
    solver.add(Or([
        And(config_vars[r] == c,
            home0[r] == configs[c][0][0],
            away0[r] == configs[c][0][1],
            home1[r] == configs[c][1][0],
            away1[r] == configs[c][1][1])
        for c in range(12)
    ]))

# Constraint: each team plays exactly once per round
for r in range(6):
    teams_in_round = [home0[r], away0[r], home1[r], away1[r]]
    solver.add(Distinct(teams_in_round))

# Count occurrences of each pair (i,j) with i home, j away
pair_counts_home = {}
pair_counts_away = {}
for i in range(4):
    for j in range(4):
        if i != j:
            pair_counts_home[(i,j)] = Sum([If(And(home0[r] == i, away0[r] == j), 1, 0) +
                                           If(And(home1[r] == i, away1[r] == j), 1, 0)
                                           for r in range(6)])
            pair_counts_away[(i,j)] = Sum([If(And(home0[r] == j, away0[r] == i), 1, 0) +
                                           If(And(home1[r] == j, away1[r] == i), 1, 0)
                                           for r in range(6)])

# Double round-robin: each unordered pair plays exactly twice (once each direction)
for i in range(4):
    for j in range(i+1, 4):
        # Total games between i and j should be 2
        total_games = Sum([If(Or(And(home0[r] == i, away0[r] == j),
                                 And(home0[r] == j, away0[r] == i),
                                 And(home1[r] == i, away1[r] == j),
                                 And(home1[r] == j, away1[r] == i)), 1, 0)
                           for r in range(6)])
        solver.add(total_games == 2)
        # Each direction exactly once
        solver.add(pair_counts_home[(i,j)] == 1)
        solver.add(pair_counts_home[(j,i)] == 1)

# Consecutive limits: no more than 2 consecutive home/away games
# For each team, track home/away status per round
is_home = [[Bool(f'home_{t}_{r}') for r in range(6)] for t in range(4)]
is_away = [[Bool(f'away_{t}_{r}') for r in range(6)] for t in range(4)]

for t in range(4):
    for r in range(6):
        # Team t is home if they appear as home0 or home1 in round r
        solver.add(is_home[t][r] == Or(home0[r] == t, home1[r] == t))
        # Team t is away if they appear as away0 or away1 in round r
        solver.add(is_away[t][r] == Or(away0[r] == t, away1[r] == t))
        # Each team plays exactly once per round, so exactly one of home/away is true
        solver.add(is_home[t][r] != is_away[t][r])

# Consecutive home limit: no three consecutive home games
for t in range(4):
    for r in range(4):  # r, r+1, r+2
        solver.add(Not(And(is_home[t][r], is_home[t][r+1], is_home[t][r+2])))
        solver.add(Not(And(is_away[t][r], is_away[t][r+1], is_away[t][r+2])))

# Objective: minimize total travel distance
total_distance = Real('total_distance')
distance_expr = RealVal(0)
for r in range(6):
    # Distance for first match
    d0 = RealVal(0)
    solver.add(Or([And(home0[r] == i, away0[r] == j, d0 == dist[i][j])
                   for i in range(4) for j in range(4) if i != j]))
    # Distance for second match
    d1 = RealVal(0)
    solver.add(Or([And(home1[r] == i, away1[r] == j, d1 == dist[i][j])
                   for i in range(4) for j in range(4) if i != j]))
    distance_expr = distance_expr + d0 + d1

solver.add(total_distance == distance_expr)
solver.minimize(total_distance)

# Check
result = solver.check()
print(f"Solver result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nOptimal schedule:")
    total_dist = 0
    for r in range(6):
        cfg = m.evaluate(config_vars[r]).as_long()
        h0, a0, h1, a1 = get_matches(cfg)
        print(f"Round {r+1}: {teams[h0]} vs {teams[a0]} (home: {teams[h0]}), {teams[h1]} vs {teams[a1]} (home: {teams[h1]})")
        total_dist += dist[h0][a0] + dist[h1][a1]
    print(f"\nTotal travel distance: {total_dist}")
    print(f"Expected optimal: 75")
    # Check if constraints satisfied
    feasible = True
    # Verify pair counts
    for i in range(4):
        for j in range(i+1, 4):
            count = 0
            for r in range(6):
                cfg = m.evaluate(config_vars[r]).as_long()
                h0, a0, h1, a1 = get_matches(cfg)
                if (h0 == i and a0 == j) or (h0 == j and a0 == i) or (h1 == i and a1 == j) or (h1 == j and a1 == i):
                    count += 1
            if count != 2:
                feasible = False
                print(f"ERROR: Pair {teams[i]}-{teams[j]} plays {count} times, expected 2")
    print(f"Feasible: {feasible}")
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found")
else:
    print("STATUS: unknown")