from z3 import *
import math

# Teams
teams = ['A', 'B', 'C', 'D', 'E', 'F']
T = len(teams)  # 6
R = 10  # rounds

# Team indices
team_idx = {t: i for i, t in enumerate(teams)}

# Coordinates
coords = {
    'A': (0, 0),
    'B': (10, 0),
    'C': (5, 8),
    'D': (0, 15),
    'E': (10, 15),
    'F': (15, 8)
}

# Distance matrix (scaled by 10, as given)
dist = {}
dist[('A','B')] = 100; dist[('B','A')] = 100
dist[('A','C')] = 94;  dist[('C','A')] = 94
dist[('A','D')] = 150; dist[('D','A')] = 150
dist[('A','E')] = 180; dist[('E','A')] = 180
dist[('A','F')] = 170; dist[('F','A')] = 170
dist[('B','C')] = 94;  dist[('C','B')] = 94
dist[('B','D')] = 180; dist[('D','B')] = 180
dist[('B','E')] = 150; dist[('E','B')] = 150
dist[('B','F')] = 94;  dist[('F','B')] = 94
dist[('C','D')] = 86;  dist[('D','C')] = 86
dist[('C','E')] = 86;  dist[('E','C')] = 86
dist[('C','F')] = 100; dist[('F','C')] = 100
dist[('D','E')] = 100; dist[('E','D')] = 100
dist[('D','F')] = 170; dist[('F','D')] = 170
dist[('E','F')] = 94;  dist[('F','E')] = 94

solver = Solver()

# Decision variables:
# For each round r (0..9) and each match slot m (0..2), we have home team h[r][m] and away team a[r][m]
h = [[Int(f'h_{r}_{m}') for m in range(3)] for r in range(R)]
a = [[Int(f'a_{r}_{m}') for m in range(3)] for r in range(R)]

# Domain: team indices 0..5
for r in range(R):
    for m in range(3):
        solver.add(h[r][m] >= 0, h[r][m] < T)
        solver.add(a[r][m] >= 0, a[r][m] < T)
        solver.add(h[r][m] != a[r][m])  # home != away

# Constraint 2: Each team plays exactly once per round
# For each round r and each team t, exactly one match slot has t as home or away
for r in range(R):
    for t in range(T):
        plays = Sum([If(h[r][m] == t, 1, 0) for m in range(3)] + [If(a[r][m] == t, 1, 0) for m in range(3)])
        solver.add(plays == 1)

# Constraint 1: Double round-robin - each ordered pair (t1, t2) with t1 != t2 plays exactly once
for t1 in range(T):
    for t2 in range(T):
        if t1 == t2:
            continue
        # Count matches where t1 is home and t2 is away
        count = Sum([If(And(h[r][m] == t1, a[r][m] == t2), 1, 0) for r in range(R) for m in range(3)])
        solver.add(count == 1)

# Constraint 4: No team may play more than 3 consecutive home games or 3 consecutive away games
# For each team t, for each starting round r (0..R-4), check the 4-round window
for t in range(T):
    for r in range(R - 3):
        home_count = Sum([If(Or([h[r+k][m] == t for m in range(3)]), 1, 0) for k in range(4)])
        away_count = Sum([If(Or([a[r+k][m] == t for m in range(3)]), 1, 0) for k in range(4)])
        solver.add(home_count <= 3)
        solver.add(away_count <= 3)

# Constraint 5: Rivalry constraint - A and B cannot play each other in round 1
# A=0, B=1, C=2, D=3
# Round 1 is index 0
solver.add(Not(Or([And(h[0][m] == 0, a[0][m] == 1) for m in range(3)])))
solver.add(Not(Or([And(h[0][m] == 1, a[0][m] == 0) for m in range(3)])))
# C and D cannot play each other in round 1
solver.add(Not(Or([And(h[0][m] == 2, a[0][m] == 3) for m in range(3)])))
solver.add(Not(Or([And(h[0][m] == 3, a[0][m] == 2) for m in range(3)])))

# Constraint 3: Stateful Travel - track location after each round
# location[r][t] = team t's location at the end of round r (0-indexed)
# We'll use integer encoding: 0=A, 1=B, 2=C, 3=D, 4=E, 5=F
loc = [[Int(f'loc_{r}_{t}') for t in range(T)] for r in range(R)]

# Initial location: before round 1, each team is at their home city
# So at the end of round 0, location depends on round 0 game
# Actually, we need location BEFORE round 0 (initial) and after each round.
# Let's define loc_before[r][t] = location at start of round r
# and loc_after[r][t] = location at end of round r
loc_before = [[Int(f'loc_before_{r}_{t}') for t in range(T)] for r in range(R)]
loc_after = [[Int(f'loc_after_{r}_{t}') for t in range(T)] for r in range(R)]

# Initial: before round 0, each team is at their home city
for t in range(T):
    solver.add(loc_before[0][t] == t)

# For each round r and each team t:
# If t plays home in round r, loc_after[r][t] = t (home city)
# If t plays away in round r, loc_after[r][t] = opponent's city
for r in range(R):
    for t in range(T):
        # Find the opponent in round r
        # t is home in some match m => opponent is a[r][m], location after = t
        # t is away in some match m => opponent is h[r][m], location after = opponent
        is_home = Or([And(h[r][m] == t) for m in range(3)])
        is_away = Or([And(a[r][m] == t) for m in range(3)])
        
        # If home: loc_after = t
        # If away: loc_after = opponent (the home team in that match)
        # We need to find the opponent when away
        away_opponent = Sum([If(And(a[r][m] == t), h[r][m], 0) for m in range(3)])
        
        solver.add(Implies(is_home, loc_after[r][t] == t))
        solver.add(Implies(is_away, loc_after[r][t] == away_opponent))
        
        # loc_before for next round = loc_after of current round
        if r < R - 1:
            solver.add(loc_before[r+1][t] == loc_after[r][t])

# Constraint 7: Travel Fatigue
# If a team travels distance > 140 to reach an away game, they must play home in the immediately following round
# Travel distance = distance from loc_before[r][t] to the away venue
# The away venue is the home team's city when t is away
FATIGUE_THRESHOLD = 140

for r in range(R):
    for t in range(T):
        # Check if t plays away in round r
        is_away = Or([And(a[r][m] == t) for m in range(3)])
        
        # If away, find the opponent (home team)
        opponent = Sum([If(And(a[r][m] == t), h[r][m], 0) for m in range(3)])
        
        # Travel distance from loc_before[r][t] to opponent's city
        # We need to encode distance using the distance matrix
        # Since distance is a constant for each pair of cities, we can use a lookup
        # But loc_before[r][t] is symbolic, so we need to encode the distance function
        
        # Create a Z3 function for distance
        # dist_func(i, j) = distance between city i and city j
        # We'll encode this as constraints
        
        # For each possible pair of cities (i, j), the distance is known
        # travel_dist = dist[loc_before[r][t]][opponent]
        # We need to encode: travel_dist > 140 => next round must be home
        
        # Using Or-loop pattern for each possible pair
        if r < R - 1:  # only if there's a next round
            # For each possible pair (from_city, to_city) where t is away
            for from_city in range(T):
                for to_city in range(T):
                    if from_city == to_city:
                        continue
                    d = dist[(teams[from_city], teams[to_city])]
                    if d > FATIGUE_THRESHOLD:
                        # If loc_before[r][t] == from_city AND opponent == to_city AND t is away
                        # Then t must play home in round r+1
                        condition = And(
                            loc_before[r][t] == from_city,
                            opponent == to_city,
                            is_away
                        )
                        # t must play home in round r+1
                        must_be_home_next = Or([h[r+1][m] == t for m in range(3)])
                        solver.add(Implies(condition, must_be_home_next))

# Constraint 6: Mandatory Break - each team must have at least one sequence of two consecutive home games
for t in range(T):
    # There exists some starting round r (0..R-2) where t plays home in both r and r+1
    has_home_stand = Or([
        And(
            Or([h[r][m] == t for m in range(3)]),
            Or([h[r+1][m] == t for m in range(3)])
        )
        for r in range(R - 1)
    ])
    solver.add(has_home_stand)

print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Schedule found!")
    for r in range(R):
        print(f"Round {r+1}:")
        for slot in range(3):
            home_team = teams[m[h[r][slot]].as_long()]
            away_team = teams[m[a[r][slot]].as_long()]
            print(f"  Match {slot+1}: {home_team} vs {away_team} (home: {home_team})")
        # Print locations after this round
        print(f"  Locations after round:")
        for t in range(T):
            loc_val = m[loc_after[r][t]].as_long()
            print(f"    {teams[t]} at {teams[loc_val]}")
else:
    print("STATUS: unsat")
    print("No valid schedule found.")