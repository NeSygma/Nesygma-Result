from z3 import *

# Team locations
teams = ['A', 'B', 'C', 'D']
locations = {
    'A': (0, 0),
    'B': (3, 4),
    'C': (6, 0),
    'D': (2, 8)
}

# Precomputed Euclidean distances as a nested dictionary
raw_dist = {
    'A': {'A': 0, 'B': 5, 'C': 6, 'D': 8.2},
    'B': {'A': 5, 'B': 0, 'C': 5, 'D': 5.7},
    'C': {'A': 6, 'B': 5, 'C': 0, 'D': 10},
    'D': {'A': 8.2, 'B': 5.7, 'C': 10, 'D': 0}
}

# Rounds and matches
num_rounds = 6
matches_per_round = 2

# Helper: team index mapping
team_to_idx = {team: i for i, team in enumerate(teams)}
idx_to_team = {i: team for i, team in enumerate(teams)}

# Decision variables: matches[t][m] = (home, away) as integers 0-3
matches = [[(Int(f"home_{t}_{m}"), Int(f"away_{t}_{m}")) for m in range(matches_per_round)] for t in range(num_rounds)]

# Solver
solver = Optimize()

# Constraint 2: Each team plays exactly once per round
# For each round, home teams are distinct and away teams are distinct
for t in range(num_rounds):
    for m1 in range(matches_per_round):
        for m2 in range(matches_per_round):
            if m1 < m2:
                # In the same round, two matches cannot have the same home team
                solver.add(matches[t][m1][0] != matches[t][m2][0])
                # In the same round, two matches cannot have the same away team
                solver.add(matches[t][m1][1] != matches[t][m2][1])

# Constraint 3: Each unordered pair plays exactly twice (once home, once away)
from itertools import combinations
for a, b in combinations(teams, 2):
    a_idx = team_to_idx[a]
    b_idx = team_to_idx[b]
    # Count occurrences of (a home vs b away) or (b home vs a away)
    count_ab = Sum([
        If(And(matches[t][m][0] == a_idx, matches[t][m][1] == b_idx), 1, 0) 
        for t in range(num_rounds) for m in range(matches_per_round)
    ])
    count_ba = Sum([
        If(And(matches[t][m][0] == b_idx, matches[t][m][1] == a_idx), 1, 0) 
        for t in range(num_rounds) for m in range(matches_per_round)
    ])
    solver.add(count_ab + count_ba == 2)

# Constraint 4: No team plays more than 2 consecutive home games
# Track home streaks per team
for team_idx in range(4):
    home_streak = [Int(f"home_streak_{team_idx}_{t}") for t in range(num_rounds)]
    # Initialize
    home_in_round_0 = Sum([
        If(matches[0][m][0] == team_idx, 1, 0) for m in range(matches_per_round)
    ])
    solver.add(home_streak[0] == If(home_in_round_0 > 0, home_in_round_0, 0))
    # Recurrence
    for t in range(1, num_rounds):
        # Compute home count in round t
        home_in_round = Sum([
            If(matches[t][m][0] == team_idx, 1, 0) for m in range(matches_per_round)
        ])
    # Streak: if home_in_round > 0, streak = previous streak + 1, else 0
        solver.add(home_streak[t] == If(home_in_round > 0, home_streak[t-1] + home_in_round, 0))
        # Limit streak to <= 2
        solver.add(home_streak[t] <= 2)

# Constraint 5: No team plays more than 2 consecutive away games
# Track away streaks per team
for team_idx in range(4):
    away_streak = [Int(f"away_streak_{team_idx}_{t}") for t in range(num_rounds)]
    # Initialize
    away_in_round_0 = Sum([
        If(matches[0][m][1] == team_idx, 1, 0) for m in range(matches_per_round)
    ])
    solver.add(away_streak[0] == If(away_in_round_0 > 0, away_in_round_0, 0))
    # Recurrence
    for t in range(1, num_rounds):
        # Compute away count in round t
        away_in_round = Sum([
            If(matches[t][m][1] == team_idx, 1, 0) for m in range(matches_per_round)
        ])
        # Streak: if away_in_round > 0, streak = previous streak + 1, else 0
        solver.add(away_streak[t] == If(away_in_round > 0, away_streak[t-1] + away_in_round, 0))
        # Limit streak to <= 2
        solver.add(away_streak[t] <= 2)

# Objective: minimize total travel distance
# For each match, the away team travels from its home to the home team's location
# We'll compute the distance using If conditions to avoid direct indexing with Z3 expressions

total_distance = Int('total_distance')
# Compute total distance as sum over all matches
# We'll use a nested If to map (home, away) indices to distance
all_matches = [(t, m) for t in range(num_rounds) for m in range(matches_per_round)]

# Build a Z3 expression for total distance
solver.add(total_distance == Sum(
    If(And(matches[t][m][0] == team_to_idx[h], matches[t][m][1] == team_to_idx[a]),
       raw_dist[h][a],
       0)
    for t, m in all_matches
    for h in teams
    for a in teams
))

solver.minimize(total_distance)

# Set timeout to avoid infinite loops
solver.set("timeout", 30000)

# Check and print result
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    total_dist_val = model.eval(total_distance)
    schedule = []
    for t in range(num_rounds):
        round_matches = []
        for m in range(matches_per_round):
            home_idx = model.eval(matches[t][m][0])
            away_idx = model.eval(matches[t][m][1])
            home_team = idx_to_team[home_idx.as_long()]
            away_team = idx_to_team[away_idx.as_long()]
            round_matches.append({"home": home_team, "away": away_team})
        schedule.append(round_matches)
    
    print("STATUS: sat")
    print("Schedule:")
    for i, round_matches in enumerate(schedule):
        print(f"Round {i+1}: {round_matches}")
    print(f"Total distance: {total_dist_val}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")