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

# Map team names to integers
team_to_int = {team: i for i, team in enumerate(teams)}
int_to_team = {i: team for team, i in team_to_int.items()}

# 1. Schedule variables: schedule[round][match] = (home, away)
home_teams = [[Int(f'home_{r}_{m}') for m in range(NUM_MATCHES_PER_ROUND)] for r in range(NUM_ROUNDS)]
away_teams = [[Int(f'away_{r}_{m}') for m in range(NUM_MATCHES_PER_ROUND)] for r in range(NUM_ROUNDS)]

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
# We need to avoid indexing Python lists with Z3 variables
# Instead, we'll use constraints that relate location updates to match assignments
for r in range(NUM_ROUNDS):
    for t in range(NUM_TEAMS):
        # For each possible match in this round
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
            # We need to get the host's location
            # We'll use a different approach: for each possible host
            for host in range(NUM_TEAMS):
                if host != t:
                    solver.add(Implies(
                        And(
                            away_teams[r][m] == t,
                            home_teams[r][m] == host
                        ),
                        And(
                            # Location becomes host's location at end of previous round
                            loc_x[t][r+1] == loc_x[host][r],
                            loc_y[t][r+1] == loc_y[host][r],
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
# If a team travels > 140 to an away game, they must play home in the next round
for t in range(NUM_TEAMS):
    for r in range(NUM_ROUNDS - 1):  # r is current round, r+1 is next round
        for m in range(NUM_MATCHES_PER_ROUND):
            # If team t is away in round r+1
            for host in range(NUM_TEAMS):
                if host != t:
                    # Calculate distance from team t's location at end of round r
                    # to host's home location
                    dx = loc_x[t][r] - team_coords[int_to_team[host]][0]
                    dy = loc_y[t][r] - team_coords[int_to_team[host]][1]
                    dist_sq = dx*dx + dy*dy
                    
                    # If distance > 140 (i.e., dist_sq > 19600), then team must play home in round r+2
                    if r + 2 < NUM_ROUNDS:
                        solver.add(Implies(
                            And(
                                away_teams[r+1][m] == t,
                                home_teams[r+1][m] == host,
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