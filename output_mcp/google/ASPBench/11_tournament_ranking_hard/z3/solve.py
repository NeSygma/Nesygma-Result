from z3 import *
import random

# 1. Setup Data
random.seed(42)
num_teams = 30
teams = list(range(num_teams))
seeds = list(range(10)) # T01-T10
groups = {
    'A': list(range(0, 5)),
    'B': list(range(5, 10)),
    'C': list(range(10, 15)),
    'D': list(range(15, 20)),
    'E': list(range(20, 25)),
    'F': list(range(25, 30))
}

def get_group(team_idx):
    for g, members in groups.items():
        if team_idx in members:
            return g
    return None

# Match results
matches = []
for i in range(num_teams):
    for j in range(i + 1, num_teams):
        weight = random.randint(1, 5)
        if (i + j) % 2 == 0:
            matches.append((i, j, weight)) # i beats j
        else:
            matches.append((j, i, weight)) # j beats i

# 2. Model
solver = Solver()
rank = [Int(f'rank_{i}') for i in range(num_teams)]
team_at = [Int(f'team_at_{p}') for p in range(num_teams)]

# Basic constraints
solver.add(Distinct(rank))
for i in range(num_teams):
    solver.add(rank[i] >= 1, rank[i] <= num_teams)
    # Link rank and team_at
    for p in range(num_teams):
        solver.add(Implies(rank[i] == p + 1, team_at[p] == i))

# 1. Must-above
must_above = [
    (4, 17), (9, 10), (6, 27), (7, 18), (1, 26), (3, 20), (2, 11), (5, 16), (8, 24), (0, 29),
    (12, 28), (13, 19), (14, 15), (21, 7), (22, 2), (23, 6), (25, 4), (24, 13), (19, 21), (27, 14)
]
for a, b in must_above:
    solver.add(rank[a] < rank[b])

# 2. Adjacency bans
adj_bans = [
    (1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 18), (19, 20),
    (21, 22), (23, 24), (25, 26), (27, 28), (0, 29)
]
for a, b in adj_bans:
    solver.add(Not(Or(rank[a] == rank[b] + 1, rank[b] == rank[a] + 1)))

# 3. Forbid-top
# T27 top 3, T14 top 5, T18 top 4, T21 top 2, T22 top 6, T19 top 8, T16 top 7, T29 top 10
forbid_top = [(26, 3), (13, 5), (17, 4), (20, 2), (21, 6), (18, 8), (15, 7), (28, 10)]
for t, limit in forbid_top:
    solver.add(rank[t] > limit)

# 4. Forbid-block
# T14 11-15, T20 5-9, T23 13-17, T02 21-25, T09 26-30
forbid_block = [(13, 11, 15), (19, 5, 9), (22, 13, 17), (1, 21, 25), (8, 26, 30)]
for t, start, end in forbid_block:
    solver.add(Not(And(rank[t] >= start, rank[t] <= end)))

# 5. Diversity
for p in range(num_teams - 4):
    for g in groups.keys():
        solver.add(Sum([If(Or([And(team_at[p+k] == m, get_group(m) == g) for m in groups[g]]), 1, 0) for k in range(5)]) <= 2)

# 6. Seed quota
solver.add(Sum([If(rank[i] <= 10, 1, 0) for i in seeds]) >= 6)

# 7. Violation bound
violations = Sum([If(rank[w] > rank[l], weight, 0) for w, l, weight in matches])
solver.add(violations <= 650)

# 3. Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    final_ranking = [0] * num_teams
    for i in range(num_teams):
        final_ranking[m[rank[i]].as_long() - 1] = i
    print("Ranking (1-30):", [f"T{t+1:02d}" for t in final_ranking])
    print("Violations:", m.evaluate(violations))
else:
    print("STATUS: unsat")