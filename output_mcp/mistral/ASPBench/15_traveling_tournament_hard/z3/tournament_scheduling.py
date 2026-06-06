from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Team identifiers: 0=A, 1=B, 2=C, 3=D, 4=E, 5=F
teams = list(range(6))
team_names = ['A', 'B', 'C', 'D', 'E', 'F']

# Team home locations (x, y) - scaled by 10
locations = {
    0: (0, 0),   # A
    1: (10, 0),  # B
    2: (5, 8),   # C
    3: (0, 15),  # D
    4: (10, 15), # E
    5: (15, 8)   # F
}

# Precomputed Euclidean distances (scaled by 10)
distances = {
    (0, 1): 100, (0, 2): 94, (0, 3): 150, (0, 4): 180, (0, 5): 170,
    (1, 0): 100, (1, 2): 94, (1, 3): 180, (1, 4): 150, (1, 5): 94,
    (2, 0): 94, (2, 1): 94, (2, 3): 86, (2, 4): 86, (2, 5): 100,
    (3, 0): 150, (3, 1): 180, (3, 2): 86, (3, 4): 100, (3, 5): 170,
    (4, 0): 180, (4, 1): 150, (4, 2): 86, (4, 3): 100, (4, 5): 94,
    (5, 0): 170, (5, 1): 94, (5, 2): 100, (5, 3): 170, (5, 4): 94
}

# Initialize solver
solver = Solver()

# Decision variables
# schedule[round][match] = (home, away) represented as two separate Int variables
# home_vars[r][m] = home team in round r, match m
# away_vars[r][m] = away team in round r, match m
home_vars = [[Int(f'home_r{r}_m{m}') for m in range(3)] for r in range(10)]
away_vars = [[Int(f'away_r{r}_m{m}') for m in range(3)] for r in range(10)]

# Team location at the end of each round
# location[team][round] = (x, y) where round in [0,10]
# round 0 is initial location (before any games)
# round 10 is final location (after all games)
location = [[[Int(f'loc_{t}_r{r}_x'), Int(f'loc_{t}_r{r}_y')] for r in range(11)] for t in teams]

# Initialize team locations at round 0 (before any games) to their home cities
for t in teams:
    solver.add(location[t][0][0] == locations[t][0])
    solver.add(location[t][0][1] == locations[t][1])

# Team consecutive home/away counts at the end of each round
# consecutive[t][r] = number of consecutive home (if positive) or away (if negative) games
# 0 means last game was neither home nor away (shouldn't happen) or streak reset
consecutive = [[Int(f'cons_{t}_r{r}') for r in range(10)] for t in teams]

# Track whether each team has had a mandatory break (at least one HH sequence)
has_break = [Bool(f'has_break_{t}') for t in teams]

# ============================================================================
# Constraint 1: Double Round-Robin
# Each ordered pair (i,j) with i≠j must play exactly once (home=i, away=j)
# ============================================================================
for i in teams:
    for j in teams:
        if i != j:
            # Count how many times team i plays home against team j
            count = Sum([If(And(home_vars[r][m] == i, away_vars[r][m] == j), 1, 0) for r in range(10) for m in range(3)])
            solver.add(count == 1)

# ============================================================================
# Constraint 2: Round Structure
# Each round has exactly 3 matches, all teams play exactly once per round
# ============================================================================
for r in range(10):
    # All teams play exactly once per round
    for t in teams:
        # Team t appears exactly once in the round as either home or away
        appears = Sum([If(Or(home_vars[r][m] == t, away_vars[r][m] == t), 1, 0) for m in range(3)])
        solver.add(appears == 1)
    
    # No duplicate matches in the same round
    for m1 in range(3):
        for m2 in range(m1+1, 3):
            # No two matches can have the same home-away pair
            solver.add(Not(And(
                home_vars[r][m1] == home_vars[r][m2],
                away_vars[r][m1] == away_vars[r][m2]
            )))
            # No match can be the reverse of another in the same round
            solver.add(Not(And(
                home_vars[r][m1] == away_vars[r][m2],
                away_vars[r][m1] == home_vars[r][m2]
            )))

# ============================================================================
# Constraint 3: Stateful Travel
# Update team locations based on match outcomes
# ============================================================================
for r in range(10):
    for t in teams:
        for m in range(3):
            # If team t is home in this match, their location stays at home
            solver.add(Implies(
                home_vars[r][m] == t,
                And(
                    location[t][r+1][0] == locations[t][0],
                    location[t][r+1][1] == locations[t][1]
                )
            ))
            # If team t is away in this match, their location becomes the home of the home team
            solver.add(Implies(
                away_vars[r][m] == t,
                And(
                    location[t][r+1][0] == locations[home_vars[r][m]][0],
                    location[t][r+1][1] == locations[home_vars[r][m]][1]
                )
            ))

# ============================================================================
# Constraint 4: Consecutive Game Limit
# No team may play more than 3 consecutive home or away games
# ============================================================================
for t in teams:
    for r in range(10):
        # Determine if team t's game in round r was home or away
        is_home = [Bool(f'is_home_{t}_r{r}_m{m}') for m in range(3)]
        for m in range(3):
            solver.add(is_home[m] == (home_vars[r][m] == t))
        
        # Team t plays exactly once per round, so exactly one is_home[m] is True
        solver.add(Sum([If(is_home[m], 1, 0) for m in range(3)]) == 1)
        
        # Set consecutive count based on previous round
        if r == 0:
            # First round: consecutive count is 1 if home, -1 if away
            for m in range(3):
                solver.add(Implies(is_home[m], consecutive[t][r] == 1))
                solver.add(Implies(Not(is_home[m]), consecutive[t][r] == -1))
        else:
            # Subsequent rounds: update consecutive count
            for m in range(3):
                solver.add(Implies(
                    is_home[m],
                    consecutive[t][r] == consecutive[t][r-1] + 1
                ))
                solver.add(Implies(
                    Not(is_home[m]),
                    consecutive[t][r] == consecutive[t][r-1] - 1
                ))
        
        # Enforce limit: |consecutive[t][r]| <= 3
        solver.add(consecutive[t][r] <= 3)
        solver.add(consecutive[t][r] >= -3)

# ============================================================================
# Constraint 5: Rivalry Constraint
# Teams A and B cannot play each other in round 1
# Teams C and D cannot play each other in round 1
# ============================================================================
for m in range(3):
    # A vs B not in round 0
    solver.add(Not(And(
        Or(home_vars[0][m] == 0, away_vars[0][m] == 0),
        Or(home_vars[0][m] == 1, away_vars[0][m] == 1)
    )))
    # C vs D not in round 0
    solver.add(Not(And(
        Or(home_vars[0][m] == 2, away_vars[0][m] == 2),
        Or(home_vars[0][m] == 3, away_vars[0][m] == 3)
    )))

# ============================================================================
# Constraint 6: Mandatory Break
# Each team must have at least one sequence of two consecutive home games
# ============================================================================
for t in teams:
    # Track if we've seen HH sequence
    seen_HH = [Bool(f'seen_HH_{t}_r{r}') for r in range(9)]
    
    # Initialize
    for r in range(9):
        # Check if rounds r and r+1 are both home for team t
        is_home_r = [Bool(f'is_home_{t}_r{r}_m{m}') for m in range(3)]
        is_home_r1 = [Bool(f'is_home_{t}_r{r+1}_m{m}') for m in range(3)]
        
        # If any match in round r is home for t and any match in round r+1 is home for t, then seen_HH[r] is True
        solver.add(seen_HH[r] == Or([And(is_home_r[m1], is_home_r1[m2]) for m1 in range(3) for m2 in range(3)]))
        
        # Propagate seen_HH
        if r == 0:
            pass  # already set above
        else:
            solver.add(seen_HH[r] == Or(seen_HH[r-1], seen_HH[r]))
    
    # At least one HH sequence must exist
    solver.add(Or(seen_HH))
    # Set the has_break flag
    solver.add(has_break[t] == Or(seen_HH))

# ============================================================================
# Constraint 7: Travel Fatigue
# If a team travels > 140 to reach an away game, they must play at home in the next round
# ============================================================================
for t in teams:
    for r in range(9):  # Can't apply to round 10 (no next round)
        # Find the match where team t played in round r
        # Team t could be home or away in round r
        is_home_r = [Bool(f'is_home_{t}_r{r}_m{m}') for m in range(3)]
        is_away_r = [Bool(f'is_away_{t}_r{r}_m{m}') for m in range(3)]
        
        for m in range(3):
            # If team t is away in round r, calculate travel distance from their location at end of round r to away venue
            # Location at end of round r is location[t][r]
            # Away venue is location[away_vars[r][m]]
            # But we need the coordinates of the away venue, which is the home of the away team
            # So we use locations[away_vars[r][m]]
            travel_dist_sq = (
                (location[t][r][0] - locations[away_vars[r][m]][0])**2 +
                (location[t][r][1] - locations[away_vars[r][m]][1])**2
            )
            # travel_dist = sqrt(travel_dist_sq) > 140
            # To avoid sqrt, we use travel_dist_sq > 140**2
            solver.add(Implies(
                And(is_away_r[m], travel_dist_sq > 140**2),
                Or([home_vars[r+1][m2] == t for m2 in range(3)])  # Must be home in next round
            ))

# ============================================================================
# Check satisfiability
# ============================================================================
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract and print the schedule
    print("\nSchedule found:")
    for r in range(10):
        print(f"\nRound {r+1}:")
        for m in range(3):
            home_val = model[home_vars[r][m]]
            away_val = model[away_vars[r][m]]
            home_name = team_names[home_val.as_long()]
            away_name = team_names[away_val.as_long()]
            print(f"  Match {m+1}: {home_name} vs {away_name}")
    
    # Print team locations at each round
    print("\nTeam locations (end of each round):")
    for t in teams:
        print(f"\nTeam {team_names[t]}:")
        for r in range(11):
            x = model[location[t][r][0]]
            y = model[location[t][r][1]]
            print(f"  Round {r}: ({x}, {y})")
    
    # Print consecutive home/away streaks
    print("\nConsecutive home/away streaks:")
    for t in teams:
        print(f"\nTeam {team_names[t]}:")
        for r in range(10):
            c = model[consecutive[t][r]]
            print(f"  Round {r+1}: {c}")
    
    # Print mandatory breaks
    print("\nMandatory breaks satisfied:")
    for t in teams:
        hb = model[has_break[t]]
        print(f"  Team {team_names[t]}: {'Yes' if hb else 'No'}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")