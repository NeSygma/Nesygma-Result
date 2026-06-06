from z3 import *
import random

# Precompute match results deterministically
random.seed(42)
matches = []  # (winner, loser, weight)
for i in range(30):
    for j in range(i+1, 30):
        weight = random.randint(1, 5)
        if (i+j) % 2 == 0:
            matches.append((i, j, weight))  # i beats j
        else:
            matches.append((j, i, weight))  # j beats i

print(f"Total matches: {len(matches)}")
print(f"Total possible weight sum: {sum(w for _,_,w in matches)}")

# Create solver
solver = Solver()

# Variables: rank[t] = position of team t (1 to 30, 1 is best)
rank = [Int(f"rank_T{t+1:02d}") for t in range(30)]

# Domain constraints (positions 1 to 30)
for t in range(30):
    solver.add(rank[t] >= 1, rank[t] <= 30)

# All ranks are distinct (a permutation)
solver.add(Distinct(rank))

# --- Constraint 1: Must-above (team_a must rank above team_b, i.e., lower rank number) ---
must_above = [
    (4, 17),  # T05 above T18
    (9, 10),  # T10 above T11
    (6, 27),  # T07 above T28
    (7, 18),  # T08 above T19
    (1, 26),  # T02 above T27
    (3, 20),  # T04 above T21
    (2, 11),  # T03 above T12
    (5, 16),  # T06 above T17
    (8, 24),  # T09 above T25
    (0, 29),  # T01 above T30
    (12, 28), # T13 above T29
    (13, 19), # T14 above T20
    (14, 15), # T15 above T16
    (21, 7),  # T22 above T08
    (22, 2),  # T23 above T03
    (23, 6),  # T24 above T07
    (25, 4),  # T26 above T05
    (24, 13), # T25 above T14
    (19, 21), # T20 above T22
    (27, 14), # T28 above T15
]
for a, b in must_above:
    solver.add(rank[a] < rank[b])

# --- Constraint 2: Adjacency bans (|rank[a] - rank[b]| != 1) ---
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
for a, b in adj_bans:
    solver.add(rank[a] - rank[b] != 1)
    solver.add(rank[b] - rank[a] != 1)

# --- Constraint 3: Forbid-top ---
# T27 (idx 26) not in top 3: rank[26] > 3
# T14 (idx 13) not in top 5: rank[13] > 5
# T18 (idx 17) not in top 4: rank[17] > 4
# T21 (idx 20) not in top 2: rank[20] > 2
# T22 (idx 21) not in top 6: rank[21] > 6
# T19 (idx 18) not in top 8: rank[18] > 8
# T16 (idx 15) not in top 7: rank[15] > 7
# T29 (idx 28) not in top 10: rank[28] > 10
forbid_top = {
    26: 3,   # T27 not in top 3
    13: 5,   # T14 not in top 5
    17: 4,   # T18 not in top 4
    20: 2,   # T21 not in top 2
    21: 6,   # T22 not in top 6
    18: 8,   # T19 not in top 8
    15: 7,   # T16 not in top 7
    28: 10,  # T29 not in top 10
}
for t, top in forbid_top.items():
    solver.add(rank[t] > top)

# --- Constraint 4: Forbid-block ---
# T14 (idx 13) not in positions 11-15
solver.add(Or(rank[13] < 11, rank[13] > 15))
# T20 (idx 19) not in positions 5-9
solver.add(Or(rank[19] < 5, rank[19] > 9))
# T23 (idx 22) not in positions 13-17
solver.add(Or(rank[22] < 13, rank[22] > 17))
# T02 (idx 1) not in positions 21-25
solver.add(Or(rank[1] < 21, rank[1] > 25))
# T09 (idx 8) not in positions 26-30
solver.add(rank[8] < 26)

# --- Constraint 5: Diversity constraint ---
# Groups (team indices, 0-based)
groups = {
    'A': list(range(0, 5)),    # T01-T05
    'B': list(range(5, 10)),   # T06-T10
    'C': list(range(10, 15)),  # T11-T15
    'D': list(range(15, 20)),  # T16-T20
    'E': list(range(20, 25)),  # T21-T25
    'F': list(range(25, 30)),  # T26-T30
}

for start in range(1, 27):  # windows starting at positions 1 to 26
    for g_name, g_teams in groups.items():
        # Count teams from this group in positions [start, start+4]
        solver.add(
            Sum([If(And(rank[t] >= start, rank[t] <= start + 4), 1, 0) for t in g_teams]) <= 2
        )

# --- Constraint 6: Seed quota ---
# At least 6 seed teams (T01-T10, indices 0-9) in top 10 positions (1-10)
solver.add(
    Sum([If(rank[t] <= 10, 1, 0) for t in range(10)]) >= 6
)

# --- Constraint 7: Violation bound ≤ 650 ---
total_violations = Sum([
    If(rank[winner] > rank[loser], weight, 0) 
    for (winner, loser, weight) in matches
])
solver.add(total_violations <= 650)

print("Starting solver (this may take a while for 30 teams)...")
print()

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print()
    
    # Build ranking list: position 1 (best) to position 30 (worst)
    ranking = [0] * 30
    for t in range(30):
        pos = m[rank[t]].as_long()
        ranking[pos - 1] = t + 1  # store T01-T30 team number
    
    print("Ranking (position 1 = best, 30 = worst):")
    for i, team_id in enumerate(ranking):
        print(f"  {i+1:2d}: T{team_id:02d}")
    
    # Calculate total weighted violations
    total_v = 0
    for winner, loser, weight in matches:
        w_pos = m[rank[winner]].as_long()
        l_pos = m[rank[loser]].as_long()
        if w_pos > l_pos:
            total_v += weight
    print()
    print(f"Total weighted violations: {total_v}")
    print(f"Violation bound (≤650): {total_v <= 650}")
    
    # Verify seed quota
    seeds_in_top10 = sum(1 for t in range(10) if m[rank[t]].as_long() <= 10)
    print(f"Seeds in top 10: {seeds_in_top10} (need ≥ 6)")
    
    # Verify must-above constraints
    print("\nMust-above checks:")
    all_above_ok = True
    for a, b in must_above:
        ra = m[rank[a]].as_long()
        rb = m[rank[b]].as_long()
        ok = ra < rb
        if not ok:
            print(f"  FAIL: T{a+1:02d} (rank {ra}) must be above T{b+1:02d} (rank {rb})")
            all_above_ok = False
    if all_above_ok:
        print("  All must-above constraints satisfied!")
    
    # Calculate total absolute deviation
    total_abs_dev = sum(abs(m[rank[t]].as_long() - (t + 1)) for t in range(30))
    print(f"\nTotal absolute deviation: {total_abs_dev}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")