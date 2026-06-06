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

# Create solver
solver = Optimize()

# For each round, we have 2 matches: (home0, away0) and (home1, away1)
# Each is a team index 0-3
home0 = [Int(f'home0_{r}') for r in range(6)]
away0 = [Int(f'away0_{r}') for r in range(6)]
home1 = [Int(f'home1_{r}') for r in range(6)]
away1 = [Int(f'away1_{r}') for r in range(6)]

# Domain constraints: each team index 0-3
for r in range(6):
    solver.add(home0[r] >= 0, home0[r] <= 3)
    solver.add(away0[r] >= 0, away0[r] <= 3)
    solver.add(home1[r] >= 0, home1[r] <= 3)
    solver.add(away1[r] >= 0, away1[r] <= 3)
    # No team plays itself
    solver.add(home0[r] != away0[r])
    solver.add(home1[r] != away1[r])
    # All 4 teams play exactly once per round
    solver.add(Distinct([home0[r], away0[r], home1[r], away1[r]]))

# Double round-robin: each unordered pair plays exactly twice (once each direction)
# Count home-away occurrences for each ordered pair
for i in range(4):
    for j in range(4):
        if i != j:
            # Count how many times i hosts j
            count_home = Sum([If(And(home0[r] == i, away0[r] == j), 1, 0) +
                              If(And(home1[r] == i, away1[r] == j), 1, 0)
                              for r in range(6)])
            solver.add(count_home == 1)

# Consecutive limits: no more than 2 consecutive home/away games
# For each team, track home/away status per round
for t in range(4):
    for r in range(6):
        # Team t is home if they appear as home0 or home1 in round r
        is_home = Or(home0[r] == t, home1[r] == t)
        # Team t is away if they appear as away0 or away1 in round r
        is_away = Or(away0[r] == t, away1[r] == t)
        # Each team plays exactly once per round
        solver.add(is_home != is_away)
    
    # Consecutive home limit: no three consecutive home games
    for r in range(4):
        is_home_r = Or(home0[r] == t, home1[r] == t)
        is_home_r1 = Or(home0[r+1] == t, home1[r+1] == t)
        is_home_r2 = Or(home0[r+2] == t, home1[r+2] == t)
        solver.add(Not(And(is_home_r, is_home_r1, is_home_r2)))
        
        # Consecutive away limit
        is_away_r = Or(away0[r] == t, away1[r] == t)
        is_away_r1 = Or(away0[r+1] == t, away1[r+1] == t)
        is_away_r2 = Or(away0[r+2] == t, away1[r+2] == t)
        solver.add(Not(And(is_away_r, is_away_r1, is_away_r2)))

# Objective: minimize total travel distance
# Use a simpler approach: create distance variables for each match
total_dist = Real('total_dist')
dist_sum = RealVal(0)

for r in range(6):
    # For match 0
    d0 = Real(f'd0_{r}')
    # For match 1
    d1 = Real(f'd1_{r}')
    
    # Set d0 based on the match
    for i in range(4):
        for j in range(4):
            if i != j:
                solver.add(Implies(And(home0[r] == i, away0[r] == j), d0 == dist[i][j]))
    
    # Set d1 based on the match
    for i in range(4):
        for j in range(4):
            if i != j:
                solver.add(Implies(And(home1[r] == i, away1[r] == j), d1 == dist[i][j]))
    
    dist_sum = dist_sum + d0 + d1

solver.add(total_dist == dist_sum)
solver.minimize(total_dist)

# Check
result = solver.check()
print(f"Solver result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nOptimal schedule:")
    total_dist_val = 0
    for r in range(6):
        h0 = m.evaluate(home0[r]).as_long()
        a0 = m.evaluate(away0[r]).as_long()
        h1 = m.evaluate(home1[r]).as_long()
        a1 = m.evaluate(away1[r]).as_long()
        print(f"Round {r+1}: {teams[h0]} vs {teams[a0]} (home: {teams[h0]}), {teams[h1]} vs {teams[a1]} (home: {teams[h1]})")
        total_dist_val += dist[h0][a0] + dist[h1][a1]
    print(f"\nTotal travel distance: {total_dist_val}")
    print(f"Expected optimal: 75")
    
    # Verify constraints
    feasible = True
    # Check pair counts
    for i in range(4):
        for j in range(i+1, 4):
            count = 0
            for r in range(6):
                h0 = m.evaluate(home0[r]).as_long()
                a0 = m.evaluate(away0[r]).as_long()
                h1 = m.evaluate(home1[r]).as_long()
                a1 = m.evaluate(away1[r]).as_long()
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