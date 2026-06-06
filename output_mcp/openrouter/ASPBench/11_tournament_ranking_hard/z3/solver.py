from z3 import *
import random, sys

# Setup
teams = [f"T{i:02d}" for i in range(1,31)]
team_index = {name:i for i,name in enumerate(teams)}

# Generate match results with given seed and pattern
random.seed(42)
matches = []  # (winner_idx, loser_idx, weight)
for i in range(30):
    for j in range(i+1,30):
        w = random.randint(1,5)
        if (i + j) % 2 == 0:
            winner, loser = i, j
        else:
            winner, loser = j, i
        matches.append((winner, loser, w))

# Z3 variables: rank of each team (1..30)
rank = [Int(f"r_{i}") for i in range(30)]
solver = Solver()
# domain constraints
for r in rank:
    solver.add(r >= 1, r <= 30)
solver.add(Distinct(rank))

# Helper to get rank variable by team name
def r(name):
    return rank[team_index[name]]

# Must-above constraints (20 pairs)
must_above = [
    ("T05","T18"), ("T10","T11"), ("T07","T28"), ("T08","T19"), ("T02","T27"),
    ("T04","T21"), ("T03","T12"), ("T06","T17"), ("T09","T25"), ("T01","T30"),
    ("T13","T29"), ("T14","T20"), ("T15","T16"), ("T22","T08"), ("T23","T03"),
    ("T24","T07"), ("T26","T05"), ("T25","T14"), ("T20","T22"), ("T28","T15")
]
for a,b in must_above:
    solver.add(r(a) < r(b))

# Adjacency bans (15 pairs)
adj_bans = [("T02","T03"), ("T04","T05"), ("T06","T07"), ("T08","T09"), ("T10","T11"),
            ("T12","T13"), ("T14","T15"), ("T16","T17"), ("T18","T19"), ("T20","T21"),
            ("T22","T23"), ("T24","T25"), ("T26","T27"), ("T28","T29"), ("T01","T30")]
for a,b in adj_bans:
    solver.add(Abs(r(a) - r(b)) != 1)

# Forbid-top constraints (8 teams)
forbid_top = {
    "T27":3, "T14":5, "T18":4, "T21":2, "T22":6, "T19":8, "T16":7, "T29":10
}
for t, bound in forbid_top.items():
    solver.add(r(t) > bound)

# Forbid-block constraints (5 teams)
forbid_block = {
    "T14": (11,15), "T20": (5,9), "T23": (13,17), "T02": (21,25), "T09": (26,30)
}
for t, (lo,hi) in forbid_block.items():
    solver.add(Or(r(t) < lo, r(t) > hi))

# Diversity constraint: in any window of 5 positions, at most 2 from same group
# Groups mapping
group_of = {}
# Group A: T01-T05 indices 0-4
for i in range(0,5): group_of[i] = 'A'
for i in range(5,10): group_of[i] = 'B'
for i in range(10,15): group_of[i] = 'C'
for i in range(15,20): group_of[i] = 'D'
for i in range(20,25): group_of[i] = 'E'
for i in range(25,30): group_of[i] = 'F'

# Precompute team indices per group
group_teams = {g: [i for i,gr in group_of.items() if gr==g] for g in ['A','B','C','D','E','F']}

for start in range(1, 30-5+2):  # start positions 1..26 inclusive
    end = start + 4
    for g, idxs in group_teams.items():
        cnt = Sum([If(And(rank[i] >= start, rank[i] <= end), 1, 0) for i in idxs])
        solver.add(cnt <= 2)

# Seed quota: at least 6 of T01-T10 in top 10
seed_idxs = [team_index[f"T{i:02d}"] for i in range(1,11)]
seed_in_top10 = Sum([If(rank[i] <= 10, 1, 0) for i in seed_idxs])
solver.add(seed_in_top10 >= 6)

# Violation bound: total weighted violations <= 650
violation_sum = Sum([If(rank[winner] > rank[loser], w, 0) for (winner, loser, w) in matches])
solver.add(violation_sum <= 650)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    # Build ranking list ordered by rank
    ranking = [None]*30
    for i in range(30):
        pos = m[rank[i]].as_long()
        ranking[pos-1] = teams[i]
    # Compute total violations using model values
    total_viol = 0
    for winner, loser, w in matches:
        if m[rank[winner]].as_long() > m[rank[loser]].as_long():
            total_viol += w
    print("STATUS: sat")
    print("ranking =", ranking)
    print("violations =", total_viol)
else:
    print("STATUS: unsat")