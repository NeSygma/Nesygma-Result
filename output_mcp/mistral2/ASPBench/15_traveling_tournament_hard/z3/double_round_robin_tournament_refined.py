from z3 import *

# Constants for teams and rounds
TEAMS = ['A', 'B', 'C', 'D', 'E', 'F']
NUM_TEAMS = len(TEAMS)
ROUNDS = 10
MATCHES_PER_ROUND = 3

# Team coordinates (scaled by 10)
team_coords = {
    'A': (0, 0),
    'B': (10, 0),
    'C': (5, 8),
    'D': (0, 15),
    'E': (10, 15),
    'F': (15, 8)
}

# Helper function to calculate Euclidean distance
def euclidean_distance(c1, c2):
    return int(((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)**0.5)

# Precompute distance matrix for all team pairs
distance_matrix = {}
for t1 in TEAMS:
    for t2 in TEAMS:
        if t1 != t2:
            distance_matrix[(t1, t2)] = euclidean_distance(team_coords[t1], team_coords[t2])

# Initialize solver
solver = Solver()

# Decision variables
# matches[round][match_index] = (home, away)
# Use Int for home and away teams
matches = [[[Int(f"match_r{r}_m{m}_home"), Int(f"match_r{r}_m{m}_away")] for m in range(MATCHES_PER_ROUND)] for r in range(ROUNDS)]

# Team locations after each round: team_location[team][round] = (x, y)
team_location = [[[Int(f"loc_{t}_r{r}_x"), Int(f"loc_{t}_r{r}_y")] for r in range(ROUNDS + 1)] for t in range(NUM_TEAMS)]

# Consecutive home/away games: consecutive_home[team][round], consecutive_away[team][round]
consecutive_home = [[Int(f"consec_home_{t}_r{r}") for r in range(ROUNDS)] for t in range(NUM_TEAMS)]
consecutive_away = [[Int(f"consec_away_{t}_r{r}") for r in range(ROUNDS)] for t in range(NUM_TEAMS)]

# Initialize team locations at round 0 (before any games)
for t in range(NUM_TEAMS):
    x, y = team_coords[TEAMS[t]]
    solver.add(team_location[t][0][0] == x)
    solver.add(team_location[t][0][1] == y)

# Initialize consecutive home/away counters
for t in range(NUM_TEAMS):
    for r in range(ROUNDS):
        solver.add(consecutive_home[t][r] == 0)
        solver.add(consecutive_away[t][r] == 0)

# Constraints
# 1. Double Round-Robin: Each ordered pair (t1, t2) plays exactly once
for t1 in range(NUM_TEAMS):
    for t2 in range(NUM_TEAMS):
        if t1 != t2:
            played = Bool(f"played_{t1}_{t2}")
            solver.add(played == And(
                Sum([If(And(matches[r][m][0] == t1, matches[r][m][1] == t2), 1, 0) for r in range(ROUNDS) for m in range(MATCHES_PER_ROUND)]) == 1
            ))

# 2. Round structure: Each round has exactly 3 matches, and each team plays exactly once per round
for r in range(ROUNDS):
    # Exactly 3 matches per round
    for m in range(MATCHES_PER_ROUND):
        solver.add(matches[r][m][0] >= 0, matches[r][m][0] < NUM_TEAMS)
        solver.add(matches[r][m][1] >= 0, matches[r][m][1] < NUM_TEAMS)
        solver.add(matches[r][m][0] != matches[r][m][1])

    # Each team plays exactly once per round
    for t in range(NUM_TEAMS):
        solver.add(Sum([If(matches[r][m][0] == t, 1, 0) + If(matches[r][m][1] == t, 1, 0) for m in range(MATCHES_PER_ROUND)]) == 1)

# 3. Stateful Travel: Update team locations after each round
for r in range(1, ROUNDS + 1):
    for t in range(NUM_TEAMS):
        # Team t's location at round r depends on their game in round r-1
        # If they played at home in round r-1, their location is their home city
        # If they played away in round r-1, their location is the away venue
        home_city_x, home_city_y = team_coords[TEAMS[t]]
        for m in range(MATCHES_PER_ROUND):
            # If team t is home in match m of round r-1
            solver.add(Implies(
                matches[r-1][m][0] == t,
                And(
                    team_location[t][r][0] == home_city_x,
                    team_location[t][r][1] == home_city_y
                )
            ))
            # If team t is away in match m of round r-1
            # Use Or-Loop to avoid symbolic indexing
            away_cond = Or([
                And(
                    matches[r-1][m][1] == t,
                    team_location[t][r][0] == team_coords[TEAMS[h]][0],
                    team_location[t][r][1] == team_coords[TEAMS[h]][1]
                ) for h in range(NUM_TEAMS)
            ])
            solver.add(away_cond)

# 4. Consecutive Game Limit: No team may have more than 3 consecutive home or away games
for t in range(NUM_TEAMS):
    for r in range(ROUNDS):
        # Determine if team t plays home or away in round r
        plays_home = Bool(f"plays_home_{t}_r{r}")
        plays_away = Bool(f"plays_away_{t}_r{r}")
        solver.add(plays_home == Or([matches[r][m][0] == t for m in range(MATCHES_PER_ROUND)]))
        solver.add(plays_away == Or([matches[r][m][1] == t for m in range(MATCHES_PER_ROUND)]))
        
        # Update consecutive home/away counters
        if r == 0:
            solver.add(Implies(plays_home, consecutive_home[t][r] == 1))
            solver.add(Implies(plays_away, consecutive_away[t][r] == 1))
            solver.add(Implies(Not(plays_home), consecutive_home[t][r] == 0))
            solver.add(Implies(Not(plays_away), consecutive_away[t][r] == 0))
        else:
            solver.add(Implies(plays_home, consecutive_home[t][r] == consecutive_home[t][r-1] + 1))
            solver.add(Implies(plays_away, consecutive_away[t][r] == consecutive_away[t][r-1] + 1))
            solver.add(Implies(Not(plays_home), consecutive_home[t][r] == 0))
            solver.add(Implies(Not(plays_away), consecutive_away[t][r] == 0))
        
        # Enforce limit
        solver.add(consecutive_home[t][r] <= 3)
        solver.add(consecutive_away[t][r] <= 3)

# 5. Rivalry Constraint: A vs B and C vs D cannot play in round 1
for m in range(MATCHES_PER_ROUND):
    solver.add(Not(Or(
        And(matches[0][m][0] == 0, matches[0][m][1] == 1),  # A vs B
        And(matches[0][m][0] == 1, matches[0][m][1] == 0),  # B vs A
        And(matches[0][m][0] == 2, matches[0][m][1] == 3),  # C vs D
        And(matches[0][m][0] == 3, matches[0][m][1] == 2)   # D vs C
    )))

# 6. Mandatory Break: Each team must have at least one sequence of two consecutive home games
for t in range(NUM_TEAMS):
    has_break = Bool(f"has_break_{t}")
    solver.add(has_break == Or(
        [And(
            consecutive_home[t][r] >= 2,
            consecutive_home[t][r-1] >= 1
        ) for r in range(1, ROUNDS)]
    ))
    solver.add(has_break)

# 7. Travel Fatigue: If a team travels >140 to an away game, they must play at home in the next round
for r in range(1, ROUNDS):
    for t in range(NUM_TEAMS):
        for m in range(MATCHES_PER_ROUND):
            # If team t plays away in round r-1
            away_prev = Bool(f"away_prev_{t}_r{r-1}_m{m}")
            solver.add(away_prev == (matches[r-1][m][1] == t))
            
            # If team t plays away in round r
            away_curr = Or([matches[r][m2][1] == t for m2 in range(MATCHES_PER_ROUND)])
            
            # Calculate distance from team t's location at end of round r-1 to the new away venue in round r
            # Use Or-Loop to avoid symbolic indexing
            for m2 in range(MATCHES_PER_ROUND):
                if_away = Bool(f"if_away_{t}_r{r}_m2{m2}")
                solver.add(if_away == (matches[r][m2][1] == t))
                
                # Distance calculation using precomputed matrix
                # Use Or-Loop to map home team index to team name
                home_team_name = Or([
                    And(matches[r][m2][0] == h, home_team_name == TEAMS[h])
                    for h in range(NUM_TEAMS)
                ])
                distance = distance_matrix[(TEAMS[t], home_team_name)]
                
                # If team t is away in round r-1 and away in round r, and distance > 140, force home in next round
                solver.add(Implies(
                    And(away_prev, if_away, distance > 140),
                    Or([matches[r][m3][0] == t for m3 in range(MATCHES_PER_ROUND)])  # Must play home in round r
                ))

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract and print the schedule
    schedule = []
    for r in range(ROUNDS):
        round_matches = []
        for m in range(MATCHES_PER_ROUND):
            home = TEAMS[model[matches[r][m][0]].as_long()]
            away = TEAMS[model[matches[r][m][1]].as_long()]
            round_matches.append({"home": home, "away": away})
        schedule.append(round_matches)
    print("schedule =", schedule)
    print("feasible = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")