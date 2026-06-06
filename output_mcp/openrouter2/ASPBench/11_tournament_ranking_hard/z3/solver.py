from z3 import *

# Problem data
teams = [f"T{str(i+1).zfill(2)}" for i in range(30)]
team_index = {t:i for i,t in enumerate(teams)}

# Groups mapping
# Group A: T01-T05
# Group B: T06-T10
# Group C: T11-T15
# Group D: T16-T20
# Group E: T21-T25
# Group F: T26-T30
group_of = [0]*30
for i in range(5): group_of[i]=0
for i in range(5,10): group_of[i]=1
for i in range(10,15): group_of[i]=2
for i in range(15,20): group_of[i]=3
for i in range(20,25): group_of[i]=4
for i in range(25,30): group_of[i]=5

# Generate match results
import random
random.seed(42)
match_pairs = []  # list of (i,j,weight,beats_i)
for i in range(30):
    for j in range(i+1,30):
        w = random.randint(1,5)
        beats_i = ((i+j)%2==0)  # True if i beats j
        match_pairs.append((i,j,w,beats_i))

# Solver
solver = Solver()
# Position variables: pos[team] in 1..30
pos = [Int(f"pos_{i}") for i in range(30)]
for p in pos:
    solver.add(p >= 1, p <= 30)
solver.add(Distinct(pos))

# Must-above constraints
must_above_pairs = [
    (4,17), (9,10), (6,27), (7,18), (1,26), (3,20), (2,11), (5,16), (8,24), (0,29),
    (12,28), (13,19), (14,15), (21,7), (22,2), (23,6), (25,4), (24,13), (19,21), (27,14)
]
for a,b in must_above_pairs:
    solver.add(pos[a] < pos[b])

# Adjacency bans
adj_bans = [
    (1,2), (3,4), (5,6), (7,8), (9,10), (11,12), (13,14), (15,16), (17,18), (19,20),
    (21,22), (23,24), (25,26), (27,28), (0,29)
]
for a,b in adj_bans:
    solver.add(Abs(pos[a]-pos[b]) != 1)

# Forbid-top constraints
forbid_top = {
    26:3, 13:5, 17:4, 20:2, 21:6, 18:8, 15:7, 28:10
}
for t,top in forbid_top.items():
    solver.add(pos[t] > top)

# Forbid-block constraints
forbid_block = {
    13:(11,15), 19:(5,9), 22:(13,17), 1:(21,25), 8:(26,30)
}
for t,(l,r) in forbid_block.items():
    solver.add(Or(pos[t] < l, pos[t] > r))

# Diversity constraint: any window of 5 teams, no more than 2 from same group
for start in range(1, 30-5+2):  # start positions 1..26
    for g in range(6):
        count = Sum([If(And(pos[i] >= start, pos[i] <= start+4, group_of[i]==g), 1, 0) for i in range(30)])
        solver.add(count <= 2)

# Seed quota: at least 6 seed teams (indices 0-9) in top 10
seed_indices = list(range(10))
seed_in_top10 = Sum([If(pos[i] <= 10, 1, 0) for i in seed_indices])
solver.add(seed_in_top10 >= 6)

# Violation bound
violations = Sum([If(If(beats_i, pos[i] > pos[j], pos[j] > pos[i]), w, 0) for (i,j,w,beats_i) in match_pairs])
solver.add(violations <= 650)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    # Build ranking list
    ranking = sorted(teams, key=lambda t: m[pos[team_index[t]]].as_long())
    # Compute violations value
    viol_val = sum([w if ((m[pos[i]].as_long() > m[pos[j]].as_long()) if beats_i else (m[pos[j]].as_long() > m[pos[i]].as_long())) else 0 for (i,j,w,beats_i) in match_pairs])
    # Compute total_abs_deviation
    total_abs_dev = sum([abs(m[pos[i]].as_long() - (i+1)) for i in range(30)])
    print("STATUS: sat")
    print("ranking:", ranking)
    print("violations:", viol_val)
    print("valid:", True)
    print("total_abs_deviation:", total_abs_dev)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")
    else:
        print("RAW_RESULT:", result)