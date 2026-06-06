from z3 import *

BENCHMARK_MODE = True

num_teams = 6
num_rounds = 10
matches_per_round = 3

# Team indices: A0 B1 C2 D3 E4 F5

# Distance matrix scaled by 10
D = [
    [0, 100, 94, 150, 180, 170],
    [100, 0, 94, 180, 150, 94],
    [94, 94, 0, 86, 86, 100],
    [150, 180, 86, 0, 100, 170],
    [180, 150, 86, 100, 0, 94],
    [170, 94, 100, 170, 94, 0]
]

# Precompute pairs with distance > 140
big_pairs = [(i, j) for i in range(num_teams) for j in range(num_teams) if D[i][j] > 140]

solver = Solver()

# Variables: home and away teams for each round and match
h = [[Int(f"h_{r}_{m}") for m in range(matches_per_round)] for r in range(num_rounds)]
a = [[Int(f"a_{r}_{m}") for m in range(matches_per_round)] for r in range(num_rounds)]

# Home flag: 1 if team t plays home in round r, else 0
home_flag = [[Int(f"home_flag_{r}_{t}") for t in range(num_teams)] for r in range(num_rounds)]

# Opponent of team t in round r
opp = [[Int(f"opp_{r}_{t}") for t in range(num_teams)] for r in range(num_rounds)]

# Location of team t after round r (0..num_rounds)
loc = [[Int(f"loc_{r}_{t}") for t in range(num_teams)] for r in range(num_rounds+1)]

# Domain constraints for home/away teams
for r in range(num_rounds):
    for m in range(matches_per_round):
        solver.add(h[r][m] >= 0, h[r][m] < num_teams)
        solver.add(a[r][m] >= 0, a[r][m] < num_teams)
        solver.add(h[r][m] != a[r][m])

# Each round has 3 distinct teams (all 6 teams appear once)
for r in range(num_rounds):
    solver.add(Distinct([h[r][0], a[r][0], h[r][1], a[r][1], h[r][2], a[r][2]]))

# Home flag definition
for r in range(num_rounds):
    for t in range(num_teams):
        solver.add(home_flag[r][t] == If(Or([t == h[r][m] for m in range(matches_per_round)]), 1, 0))

# Opponent constraints
for r in range(num_rounds):
    for t in range(num_teams):
        solver.add(opp[r][t] >= 0, opp[r][t] < num_teams)
        for m in range(matches_per_round):
            solver.add(Implies(t == h[r][m], opp[r][t] == a[r][m]))
            solver.add(Implies(t == a[r][m], opp[r][t] == h[r][m]))

# Location updates
for t in range(num_teams):
    solver.add(loc[0][t] == t)  # start at home city
for r in range(num_rounds):
    for t in range(num_teams):
        solver.add(loc[r+1][t] == If(home_flag[r][t] == 1, t, opp[r][t]))

# Travel fatigue constraint
for r in range(1, num_rounds):
    for t in range(num_teams):
        travel_gt140 = Or([And(loc[r-1][t] == i, opp[r][t] == j) for (i, j) in big_pairs])
        solver.add(Implies(And(home_flag[r-1][t] == 0, travel_gt140), home_flag[r][t] == 1))

# Consecutive game limit: no more than 3 consecutive home or away
for t in range(num_teams):
    for r in range(num_rounds - 3):
        sum_home = home_flag[r][t] + home_flag[r+1][t] + home_flag[r+2][t] + home_flag[r+3][t]
        solver.add(sum_home != 0)  # not all away
        solver.add(sum_home != 4)  # not all home

# Mandatory break: at least one sequence of two consecutive home games
for t in range(num_teams):
    solver.add(Or([And(home_flag[r][t] == 1, home_flag[r+1][t] == 1) for r in range(num_rounds - 1)]))

# Rivalry constraints for round 1 (index 0)
for m in range(matches_per_round):
    solver.add(Not(And(h[0][m] == 0, a[0][m] == 1)))
    solver.add(Not(And(h[0][m] == 1, a[0][m] == 0)))
    solver.add(Not(And(h[0][m] == 2, a[0][m] == 3)))
    solver.add(Not(And(h[0][m] == 3, a[0][m] == 2)))

# Double round-robin: each ordered pair appears exactly once
for i in range(num_teams):
    for j in range(num_teams):
        if i == j:
            continue
        count = Sum([If(And(h[r][m] == i, a[r][m] == j), 1, 0) for r in range(num_rounds) for m in range(matches_per_round)])
        solver.add(count == 1)

# Check satisfiability
result = solver.check()

if result == sat:
    mod = solver.model()
    schedule = []
    for r in range(num_rounds):
        round_matches = []
        for m_idx in range(matches_per_round):
            home_val = mod[h[r][m_idx]].as_long()
            away_val = mod[a[r][m_idx]].as_long()
            round_matches.append((home_val, away_val))
        schedule.append(round_matches)
    print("STATUS: sat")
    print("schedule =", schedule)
    print("feasible = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")