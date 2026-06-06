from z3 import *

# Teams and coordinates
teams = ['A', 'B', 'C', 'D', 'E', 'F']
team_coords = {
    'A': (0, 0),
    'B': (10, 0),
    'C': (5, 8),
    'D': (0, 15),
    'E': (10, 15),
    'F': (15, 8)
}

# Distance matrix (scaled by 10)
distances = {
    ('A', 'B'): 100, ('A', 'C'): 94, ('A', 'D'): 150, ('A', 'E'): 180, ('A', 'F'): 170,
    ('B', 'C'): 94, ('B', 'D'): 180, ('B', 'E'): 150, ('B', 'F'): 94,
    ('C', 'D'): 86, ('C', 'E'): 86, ('C', 'F'): 100,
    ('D', 'E'): 100, ('D', 'F'): 170,
    ('E', 'F'): 94
}

# Add reverse distances
for (t1, t2), d in list(distances.items()):
    distances[(t2, t1)] = d

# Constants
NUM_ROUNDS = 10
NUM_MATCHES_PER_ROUND = 3
NUM_TEAMS = 6

# Create solver
solver = Solver()

# 1. Schedule variables: schedule[round][match] = (home, away)
# We'll use separate variables for home and away teams
home_teams = [[Int(f'home_{r}_{m}') for m in range(NUM_MATCHES_PER_ROUND)] for r in range(NUM_ROUNDS)]
away_teams = [[Int(f'away_{r}_{m}') for m in range(NUM_MATCHES_PER_ROUND)] for r in range(NUM_ROUNDS)]

# Map team names to integers
team_to_int = {team: i for i, team in enumerate(teams)}
int_to_team = {i: team for team, i in team_to_int.items()}

# 2. Location variables: location[team][round] = (x, y)
# We'll track location as coordinates
loc_x = [[Int(f'loc_x_{t}_{r}') for r in range(NUM_ROUNDS + 1)] for t in range(NUM_TEAMS)]
loc_y = [[Int(f'loc_y_{t}_{r}') for r in range(NUM_ROUNDS + 1)] for t in range(NUM_TEAMS)]

# 3. Home/away indicator: is_home[team][round]
is_home = [[Bool(f'is_home_{t}_{r}') for r in range(NUM_ROUNDS)] for t in range(NUM_TEAMS)]

# 4. Consecutive counters
consec_home = [[Int(f'consec_home_{t}_{r}') for r in range(NUM_ROUNDS)] for t in range(NUM_TEAMS)]
consec_away = [[Int(f'consec_away_{t}_{r}') for r in range(NUM_ROUNDS)] for t in range(NUM_TEAMS)]

# 5. Mandatory break: has_home_streak[team] = whether team has 2 consecutive home games
has_home_streak = [Bool(f'has_home_streak_{t}') for t in range(NUM_TEAMS)]

# Initialize locations at round 0 (before any games)
for t in range(NUM_TEAMS):
    team = int_to_team[t]
    x, y = team_coords[team]
    solver.add(loc_x[t][0] == x)
    solver.add(loc_y[t][0] == y)

# Constraint 1: Double round-robin - each ordered pair plays exactly once
# We'll track which pairs have played
played = {}
for t1 in range(NUM_TEAMS):
    for t2 in range(NUM_TEAMS):
        if t1 != t2:
            played[(t1, t2)] = Bool(f'played_{t1}_{t2}')

# Each ordered pair must play exactly once
for t1 in range(NUM_TEAMS):
    for t2 in range(NUM_TEAMS):
        if t1 != t2:
            # Count occurrences of this pair in schedule
            occurrences = []
            for r in range(NUM_ROUNDS):
                for m in range(NUM_MATCHES_PER_ROUND):
                    # Pair (t1, t2) means t1 home vs t2 away
                    occurrences.append(And(home_teams[r][m] == t1, away_teams[r][m] == t2))
            solver.add(Or(occurrences) == played[(t1, t2)])
            solver.add(played[(t1, t2)])  # Must play exactly once

# Constraint 2: Round structure - each team plays exactly once per round
for r in range(NUM_ROUNDS):
    for t in range(NUM_TEAMS):
        # Team t appears exactly once in this round (either home or away)
        appears = []
        for m in range(NUM_MATCHES_PER_ROUND):
            appears.append(home_teams[r][m] == t)
            appears.append(away_teams[r][m] == t)
        solver.add(Sum([If(appears[i], 1, 0) for i in range(len(appears))]) == 1)

# Constraint 3: Stateful travel - location updates
for r in range(NUM_ROUNDS):
    for t in range(NUM_TEAMS):
        # Find which match team t plays in this round
        match_found = False
        for m in range(NUM_MATCHES_PER_ROUND):
            # If team t is home in this match
            solver.add(Implies(
                home_teams[r][m] == t,
                And(
                    loc_x[t][r+1] == loc_x[t][r],  # Stay at home
                    loc_y[t][r+1] == loc_y[t][r],
                    is_home[t][r] == True
                )
            ))
            # If team t is away in this match
            solver.add(Implies(
                away_teams[r][m] == t,
                And(
                    # Location becomes host's location
                    loc_x[t][r+1] == loc_x[home_teams[r][m]][r],
                    loc_y[t][r+1] == loc_y[home_teams[r][m]][r],
                    is_home[t][r] == False
                )
            ))

# Constraint 4: Consecutive game limit (≤3 consecutive home/away)
for t in range(NUM_TEAMS):
    # Initialize counters
    solver.add(consec_home[t][0] == If(is_home[t][0], 1, 0))
    solver.add(consec_away[t][0] == If(Not(is_home[t][0]), 1, 0))
    
    for r in range(1, NUM_ROUNDS):
        # Update consecutive home counter
        solver.add(consec_home[t][r] == If(
            is_home[t][r],
            consec_home[t][r-1] + 1,
            0
        ))
        # Update consecutive away counter
        solver.add(consec_away[t][r] == If(
            Not(is_home[t][r]),
            consec_away[t][r-1] + 1,
            0
        ))
        # Limit to 3
        solver.add(consec_home[t][r] <= 3)
        solver.add(consec_away[t][r] <= 3)

# Constraint 5: Rivalry constraint
# A-B cannot play in round 1
a_int = team_to_int['A']
b_int = team_to_int['B']
c_int = team_to_int['C']
d_int = team_to_int['D']

for m in range(NUM_MATCHES_PER_ROUND):
    # A vs B cannot happen in round 0
    solver.add(Not(And(
        Or(home_teams[0][m] == a_int, away_teams[0][m] == a_int),
        Or(home_teams[0][m] == b_int, away_teams[0][m] == b_int)
    )))
    # C vs D cannot happen in round 0
    solver.add(Not(And(
        Or(home_teams[0][m] == c_int, away_teams[0][m] == c_int),
        Or(home_teams[0][m] == d_int, away_teams[0][m] == d_int)
    )))

# Constraint 6: Mandatory break - each team must have at least one sequence of 2 consecutive home games
for t in range(NUM_TEAMS):
    has_streak = []
    for r in range(NUM_ROUNDS - 1):
        has_streak.append(And(is_home[t][r], is_home[t][r+1]))
    solver.add(Or(has_streak) == has_home_streak[t])
    solver.add(has_home_streak[t])

# Constraint 7: Travel fatigue
for t in range(NUM_TEAMS):
    for r in range(NUM_ROUNDS - 1):
        # Calculate travel distance from location at end of round r to away venue in round r+1
        # If team plays away in round r+1, distance is from loc at end of round r to host's location
        for m in range(NUM_MATCHES_PER_ROUND):
            # If team t is away in round r+1, host is home_teams[r+1][m]
            host = home_teams[r+1][m]
            # Calculate Euclidean distance (scaled by 10)
            dx = loc_x[t][r] - loc_x[host][r]  # Host's location at end of round r
            dy = loc_y[t][r] - loc_y[host][r]
            distance_squared = dx*dx + dy*dy
            # We need actual distance > 140, but we have squared distance
            # 140^2 = 19600
            # We'll use a constraint: if distance > 140, then next round must be home
            # But we need to be careful with integer arithmetic
            
            # For now, let's use a simpler approach: if team plays away in round r+1,
            # check if distance from current location to host > 140
            # If so, force team to play home in round r+2 (if exists)
            
            # Actually, let's compute distance more carefully
            # We'll use the distance matrix for known pairs
            # For unknown pairs, we'll compute from coordinates
            
            # For simplicity, let's precompute all distances between teams
            # and use those when possible

# Let me rewrite constraint 7 more carefully
# First, let's compute distances between teams based on their home cities
team_home_dist = {}
for t1 in teams:
    for t2 in teams:
        if t1 != t2:
            x1, y1 = team_coords[t1]
            x2, y2 = team_coords[t2]
            d = int(((x1-x2)**2 + (y1-y2)**2)**0.5 * 10)  # Scale by 10
            team_home_dist[(t1, t2)] = d

# Now, for travel fatigue:
# If team plays away in round r+1, and the distance from their location at end of round r
# to the host's home city > 140, then they must play home in round r+2 (if exists)
for t in range(NUM_TEAMS):
    for r in range(NUM_ROUNDS - 1):  # r is current round, r+1 is next round
        for m in range(NUM_MATCHES_PER_ROUND):
            # If team t is away in round r+1
            solver.add(Implies(
                away_teams[r+1][m] == t,
                # Calculate distance from team t's location at end of round r
                # to host's home location
                # We need to get host's home coordinates
                # This is tricky because we need to know which team is host
                # Let's use a different approach: precompute all possible distances
                # and use constraints
                True  # Placeholder
            ))

# Let me simplify: Instead of computing distances dynamically,
# let's precompute all possible travel scenarios
# For each team, for each round, for each possible away game,
# we can compute the distance based on where they were before

# Actually, let's use a different approach for constraint 7:
# For each team, for each round r (except last), if they play away in round r+1,
# and the distance from their location at end of round r to the host's home > 140,
# then they must play home in round r+2 (if exists)

# To compute distance, we need to know:
# 1. Team t's location at end of round r
# 2. Host's home location (which is fixed)

# Let's create a helper function to compute distance between two locations
def compute_distance(x1, y1, x2, y2):
    return Sqrt((x1 - x2)**2 + (y1 - y2)**2)

# But Z3 doesn't have Sqrt for integers easily
# Let's use squared distance and compare with 140^2 = 19600

for t in range(NUM_TEAMS):
    for r in range(NUM_ROUNDS - 1):
        for m in range(NUM_MATCHES_PER_ROUND):
            # If team t is away in round r+1
            host = home_teams[r+1][m]
            # Get host's home coordinates
            host_team = host  # This is an integer, need to map to team name
            # We need to create constraints for each possible host
            
            # Let's create a constraint for each possible host team
            for host_int in range(NUM_TEAMS):
                if host_int != t:
                    host_team_name = int_to_team[host_int]
                    hx, hy = team_coords[host_team_name]
                    
                    # Distance squared from team t's location at end of round r to host's home
                    dx = loc_x[t][r] - hx
                    dy = loc_y[t][r] - hy
                    dist_sq = dx*dx + dy*dy
                    
                    # If distance > 140 (i.e., dist_sq > 19600), then team must play home in round r+2
                    if r + 2 < NUM_ROUNDS:
                        solver.add(Implies(
                            And(
                                away_teams[r+1][m] == t,
                                host == host_int,
                                dist_sq > 19600
                            ),
                            # Team must play home in round r+2
                            Or([home_teams[r+2][mm] == t for mm in range(NUM_MATCHES_PER_ROUND)])
                        ))

# Let's also add constraints to ensure each match has distinct teams
for r in range(NUM_ROUNDS):
    for m in range(NUM_MATCHES_PER_ROUND):
        solver.add(home_teams[r][m] != away_teams[r][m])
        # Ensure no team appears twice in the same round
        for m2 in range(m + 1, NUM_MATCHES_PER_ROUND):
            solver.add(home_teams[r][m] != home_teams[r][m2])
            solver.add(home_teams[r][m] != away_teams[r][m2])
            solver.add(away_teams[r][m] != home_teams[r][m2])
            solver.add(away_teams[r][m] != away_teams[r][m2])

# Add some bounds to help solver
for r in range(NUM_ROUNDS):
    for m in range(NUM_MATCHES_PER_ROUND):
        solver.add(home_teams[r][m] >= 0)
        solver.add(home_teams[r][m] < NUM_TEAMS)
        solver.add(away_teams[r][m] >= 0)
        solver.add(away_teams[r][m] < NUM_TEAMS)

# Check satisfiability
print("Checking satisfiability...")
result = solver.check()

if result == sat:
    print("STATUS: sat")
    print("Feasible schedule found!")
    model = solver.model()
    
    # Print schedule
    print("\nSchedule:")
    for r in range(NUM_ROUNDS):
        print(f"Round {r+1}:")
        for m in range(NUM_MATCHES_PER_ROUND):
            home = model[home_teams[r][m]]
            away = model[away_teams[r][m]]
            home_team = int_to_team[home.as_long()]
            away_team = int_to_team[away.as_long()]
            print(f"  Match {m+1}: {home_team} vs {away_team}")
    
    # Print locations
    print("\nTeam locations after each round:")
    for t in range(NUM_TEAMS):
        team = int_to_team[t]
        print(f"{team}: ", end="")
        for r in range(NUM_ROUNDS + 1):
            x = model[loc_x[t][r]].as_long()
            y = model[loc_y[t][r]].as_long()
            print(f"R{r}({x},{y}) ", end="")
        print()
    
    # Print home/away pattern
    print("\nHome/Away patterns:")
    for t in range(NUM_TEAMS):
        team = int_to_team[t]
        pattern = ""
        for r in range(NUM_ROUNDS):
            is_h = model[is_home[t][r]]
            pattern += "H" if is_h else "A"
        print(f"{team}: {pattern}")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found with current constraints")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")