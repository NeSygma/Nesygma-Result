from z3 import *

# Teams mapping
teams = ['A', 'B', 'C', 'D']
num_teams = len(teams)
num_rounds = 6
# Distance matrix as Real values
# rows: home, cols: away? We'll store dist[away][home] for travel distance of away team to home.
# Given matrix distances between cities (symmetric). Use Euclidean distances provided.
# We'll create a dict dist[away][home]
raw_dist = {
    ('A','A'):0, ('A','B'):5, ('A','C'):6, ('A','D'):8.2,
    ('B','A'):5, ('B','B'):0, ('B','C'):5, ('B','D'):5.7,
    ('C','A'):6, ('C','B'):5, ('C','C'):0, ('C','D'):10,
    ('D','A'):8.2, ('D','B'):5.7, ('D','C'):10, ('D','D'):0,
}
# Convert to RealVal matrix indexed by indices
dist = [[RealVal(raw_dist[(teams[i], teams[j])]) for j in range(num_teams)] for i in range(num_teams)]

# Decision variables: play[i][j][r] = Bool, i hosts j in round r
play = [[[Bool(f"play_{i}_{j}_{r}") for r in range(num_rounds)] for j in range(num_teams)] for i in range(num_teams)]

s = Optimize()

# Constraint: no self matches
for i in range(num_teams):
    for r in range(num_rounds):
        s.add(Not(play[i][i][r]))

# Double round-robin: each ordered pair (i,j) with i!=j appears exactly once as i hosts j
for i in range(num_teams):
    for j in range(num_teams):
        if i == j: continue
        s.add(Sum([If(play[i][j][r], 1, 0) for r in range(num_rounds)]) == 1)

# Each round has exactly 2 matches
for r in range(num_rounds):
    s.add(Sum([If(play[i][j][r], 1, 0) for i in range(num_teams) for j in range(num_teams) if i!=j]) == 2)

# Each team plays exactly once per round (either home or away)
for r in range(num_rounds):
    for i in range(num_teams):
        home_occ = Sum([If(play[i][j][r], 1, 0) for j in range(num_teams) if i!=j])
        away_occ = Sum([If(play[j][i][r], 1, 0) for j in range(num_teams) if i!=j])
        s.add(home_occ + away_occ == 1)

# Consecutive home/away limits (no more than 2 consecutive homes or aways)
for i in range(num_teams):
    for start in range(num_rounds-2):
        # homes in three consecutive rounds
        home_sum = Sum([If(play[i][j][r], 1, 0) for r in range(start, start+3) for j in range(num_teams) if i!=j])
        s.add(home_sum <= 2)
        # aways in three consecutive rounds
        away_sum = Sum([If(play[j][i][r], 1, 0) for r in range(start, start+3) for j in range(num_teams) if i!=j])
        s.add(away_sum <= 2)

# Objective: minimize total travel distance (away team travels to home)
total_distance = Sum([If(play[i][j][r], dist[j][i], RealVal(0)) for i in range(num_teams) for j in range(num_teams) if i!=j for r in range(num_rounds)])
s.minimize(total_distance)

# Solve
if s.check() == sat:
    m = s.model()
    # Compute total distance value
    td_val = m.eval(total_distance, model_completion=True)
    # Extract schedule
    schedule = []
    for r in range(num_rounds):
        round_matches = []
        for i in range(num_teams):
            for j in range(num_teams):
                if i==j: continue
                if is_true(m.eval(play[i][j][r])):
                    round_matches.append({"home": teams[i], "away": teams[j]})
        schedule.append(round_matches)
    print("STATUS: sat")
    print("total_distance =", td_val)
    for idx, rm in enumerate(schedule):
        print(f"Round {idx+1}:")
        for match in rm:
            print(f"  {match['home']} vs {match['away']}")
else:
    print("STATUS: unsat")