from z3 import *
import random

# Generate match results
random.seed(42)
teams = list(range(30))  # 0-29
matches = []  # (winner, loser, weight)
for i in range(30):
    for j in range(i+1, 30):
        weight = random.randint(1, 5)
        if (i + j) % 2 == 0:
            winner, loser = i, j
        else:
            winner, loser = j, i
        matches.append((winner, loser, weight))

print(f"Generated {len(matches)} matches")

# Define groups
groups = {}
for t in range(30):
    if t <= 4:
        groups[t] = 0  # Group A
    elif t <= 9:
        groups[t] = 1  # Group B
    elif t <= 14:
        groups[t] = 2  # Group C
    elif t <= 19:
        groups[t] = 3  # Group D
    elif t <= 24:
        groups[t] = 4  # Group E
    else:
        groups[t] = 5  # Group F

# Seeds: 0-9
seeds = set(range(10))

# Must-above constraints: (team_a, team_b) where a must be above b
must_above = [
    (4, 17),   # T05 above T18 (T05=4, T18=17)
    (9, 10),   # T10 above T11 (T10=9, T11=10)
    (6, 27),   # T07 above T28 (T07=6, T28=27)
    (7, 18),   # T08 above T19 (T08=7, T19=18)
    (1, 26),   # T02 above T27 (T02=1, T27=26)
    (3, 20),   # T04 above T21 (T04=3, T21=20)
    (2, 11),   # T03 above T12 (T03=2, T12=11)
    (5, 16),   # T06 above T17 (T06=5, T17=16)
    (8, 24),   # T09 above T25 (T09=8, T25=24)
    (0, 29),   # T01 above T30 (T01=0, T30=29)
    (12, 28),  # T13 above T29 (T13=12, T29=28)
    (13, 19),  # T14 above T20 (T14=13, T20=19)
    (14, 15),  # T15 above T16 (T15=14, T16=15)
    (21, 7),   # T22 above T08 (T22=21, T08=7)
    (22, 2),   # T23 above T03 (T23=22, T03=2)
    (23, 6),   # T24 above T07 (T24=23, T07=6)
    (25, 4),   # T26 above T05 (T26=25, T05=4)
    (24, 13),  # T25 above T14 (T25=24, T14=13)
    (19, 21),  # T20 above T22 (T20=19, T22=21)
    (27, 14),  # T28 above T15 (T28=27, T15=14)
]

# Adjacency bans: pairs that cannot be adjacent
adj_bans = [
    (1, 2),   # T02,T03
    (3, 4),   # T04,T05
    (5, 6),   # T06,T07
    (7, 8),   # T08,T09
    (9, 10),  # T10,T11
    (11, 12), # T12,T13
    (13, 14), # T14,T15
    (15, 16), # T16,T17
    (17, 18), # T18,T19
    (19, 20), # T20,T21
    (21, 22), # T22,T23
    (23, 24), # T24,T25
    (25, 26), # T26,T27
    (27, 28), # T28,T29
    (0, 29),  # T01,T30
]

# Forbid-top: team cannot be in top N positions (rank <= N)
forbid_top = [
    (26, 3),   # T27 cannot be in top 3
    (13, 5),   # T14 cannot be in top 5
    (17, 4),   # T18 cannot be in top 4
    (20, 2),   # T21 cannot be in top 2
    (21, 6),   # T22 cannot be in top 6
    (18, 8),   # T19 cannot be in top 8
    (15, 7),   # T16 cannot be in top 7
    (28, 10),  # T29 cannot be in top 10
]

# Forbid-block: team cannot be in positions [start, end]
forbid_block = [
    (13, 11, 15),  # T14 cannot be in 11-15
    (19, 5, 9),    # T20 cannot be in 5-9
    (22, 13, 17),  # T23 cannot be in 13-17
    (1, 21, 25),   # T02 cannot be in 21-25
    (8, 26, 30),   # T09 cannot be in 26-30
]

# Z3 solver
solver = Solver()

# Position variables: position[rank] = team_id, rank 1..30
position = [Int(f'pos_{r}') for r in range(1, 31)]

# All positions are distinct teams 0..29
for p in position:
    solver.add(p >= 0, p <= 29)
solver.add(Distinct(position))

# Must-above constraints
for a, b in must_above:
    # rank[a] < rank[b] means a appears earlier (lower rank number)
    # We need to find rank of a and b
    # Use Or-loop to express rank[a] < rank[b]
    # Since position[rank] = team, we need to find rank where position[rank] == a
    # Let's define rank variables for each team instead? Might be easier.
    # Let's switch approach: define rank[team] = position (1-30)
    # That's more straightforward for must-above, adjacency, etc.
    # Let's restart with rank variables.

print("Switching to rank variables...")
# Redefine with rank variables
solver = Solver()
rank = [Int(f'rank_{t}') for t in range(30)]
for r in rank:
    solver.add(r >= 1, r <= 30)
solver.add(Distinct(rank))

# Must-above: rank[a] < rank[b]
for a, b in must_above:
    solver.add(rank[a] < rank[b])

# Adjacency bans: |rank[a] - rank[b]| != 1
for a, b in adj_bans:
    solver.add(Or(rank[a] - rank[b] != 1, rank[b] - rank[a] != 1))
    # Equivalent: Not(Or(rank[a] - rank[b] == 1, rank[b] - rank[a] == 1))
    # But Z3 doesn't have absolute value directly, so we do:
    solver.add(Not(Or(rank[a] - rank[b] == 1, rank[b] - rank[a] == 1)))

# Forbid-top: rank[t] > top_position
for t, top in forbid_top:
    solver.add(rank[t] > top)

# Forbid-block: rank[t] not in [start, end]
for t, start, end in forbid_block:
    solver.add(Or(rank[t] < start, rank[t] > end))

# Diversity: For each window of 5 consecutive ranks (positions 1-5, 2-6, ..., 26-30)
# For each window, count teams from each group, ensure <=2 per group
for window_start in range(1, 27):  # 1 to 26 inclusive
    window_ranks = list(range(window_start, window_start + 5))
    # For each group, count teams in this window
    for g in range(6):
        # Count teams from group g in window
        count = Sum([If(rank[t] == r, 1, 0) for t in range(30) if groups[t] == g for r in window_ranks])
        # Actually, we need to count for each rank in window, which team is there.
        # Better: For each rank r in window, team = t where rank[t] == r.
        # We can use an array of team at each rank, but we have rank variables.
        # Let's create a helper: team_at_rank[r] = t such that rank[t] == r.
        # We can use an array of Int variables for team_at_rank, but that's extra.
        # Instead, we can use a constraint: For each rank r in window, the team t at that rank must satisfy group count.
        # We'll use a different approach: For each window, for each group, the number of teams from that group in the window <= 2.
        # We can express this as: Sum over teams t in group g of [rank[t] in window] <= 2.
        # rank[t] in window means rank[t] >= window_start and rank[t] <= window_start+4.
        # So we can write:
        solver.add(Sum([If(And(rank[t] >= window_start, rank[t] <= window_start+4), 1, 0) for t in range(30) if groups[t] == g]) <= 2)

# Seed quota: at least 6 seeds in top 10 positions (rank <= 10)
seed_top_count = Sum([If(rank[t] <= 10, 1, 0) for t in range(30) if t in seeds])
solver.add(seed_top_count >= 6)

# Violation bound: total weighted violations <= 650
# For each match (winner, loser, weight), if rank[winner] > rank[loser] then violation weight added
violation_weights = []
for winner, loser, weight in matches:
    # If winner's rank > loser's rank (winner lower rank number is better)
    # Actually rank 1 is best, so if winner's rank > loser's rank, winner is worse (lower rank number is better)
    # Wait: rank 1 is highest (best). So if winner's rank > loser's rank, winner is worse (higher number), meaning loser beat winner? No.
    # The match result: winner beats loser. If winner's rank > loser's rank, that means winner is ranked lower (worse) than loser, which is a violation.
    # So violation condition: rank[winner] > rank[loser]
    # We'll create a boolean variable for each match indicating violation.
    # But we need to sum weights. We can use If(condition, weight, 0).
    violation_weights.append(If(rank[winner] > rank[loser], weight, 0))
total_violations = Sum(violation_weights)
solver.add(total_violations <= 650)

print("Constraints added. Solving...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Extract ranking: sort teams by rank
    team_rank = [(t, m.evaluate(rank[t])) for t in range(30)]
    team_rank.sort(key=lambda x: x[1])  # sort by rank (ascending)
    ranking = [f"T{t+1:02d}" for t, r in team_rank]
    print("Ranking:", ranking)
    # Compute violations
    total_viol = 0
    for winner, loser, weight in matches:
        w_rank = m.evaluate(rank[winner])
        l_rank = m.evaluate(rank[loser])
        if w_rank > l_rank:
            total_viol += weight
    print("Total violations:", total_viol)
    # Check constraints
    valid = True
    # Must-above
    for a, b in must_above:
        if m.evaluate(rank[a]) >= m.evaluate(rank[b]):
            print(f"Must-above violated: T{a+1} vs T{b+1}")
            valid = False
    # Adjacency
    for a, b in adj_bans:
        if abs(m.evaluate(rank[a]) - m.evaluate(rank[b])) == 1:
            print(f"Adjacency violated: T{a+1} vs T{b+1}")
            valid = False
    # Forbid-top
    for t, top in forbid_top:
        if m.evaluate(rank[t]) <= top:
            print(f"Forbid-top violated: T{t+1} in top {top}")
            valid = False
    # Forbid-block
    for t, start, end in forbid_block:
        if start <= m.evaluate(rank[t]) <= end:
            print(f"Forbid-block violated: T{t+1} in {start}-{end}")
            valid = False
    # Diversity
    for window_start in range(1, 27):
        window_ranks = list(range(window_start, window_start+5))
        for g in range(6):
            count = 0
            for t in range(30):
                if groups[t] == g and window_start <= m.evaluate(rank[t]) <= window_start+4:
                    count += 1
            if count > 2:
                print(f"Diversity violated: window {window_start}-{window_start+4}, group {g}, count {count}")
                valid = False
    # Seed quota
    seed_count = sum(1 for t in seeds if m.evaluate(rank[t]) <= 10)
    if seed_count < 6:
        print(f"Seed quota violated: {seed_count} seeds in top 10")
        valid = False
    print("Valid:", valid)
    # Compute total absolute deviation (optional)
    total_abs_dev = sum(abs(m.evaluate(rank[t]) - (t+1)) for t in range(30))
    print("Total absolute deviation:", total_abs_dev)
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found")
else:
    print("STATUS: unknown")