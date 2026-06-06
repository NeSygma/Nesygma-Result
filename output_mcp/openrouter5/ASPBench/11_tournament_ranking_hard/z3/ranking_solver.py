from z3 import *

# ============================================================
# Problem: Find a valid ranking for 30 teams with constraints
# ============================================================

N = 30
TEAMS = list(range(N))  # 0..29 representing T01..T30

# Match results: generate using the same pattern as problem statement
import random
random.seed(42)

# winner[i][j] = True if team i beats team j (i < j)
winner = [[False]*N for _ in range(N)]
weight = [[0]*N for _ in range(N)]

for i in range(N):
    for j in range(i+1, N):
        w = random.randint(1, 5)
        weight[i][j] = w
        weight[j][i] = w
        if (i + j) % 2 == 0:
            winner[i][j] = True  # i beats j
            winner[j][i] = False
        else:
            winner[i][j] = False
            winner[j][i] = True  # j beats i

# ============================================================
# Decision Variables
# ============================================================
# rank[t] = position of team t (1-indexed, 1..30)
rank = [Int(f'rank_{t}') for t in range(N)]

# position[p] = team at position p (1-indexed, 1..30)
pos = [Int(f'pos_{p}') for p in range(N)]

solver = Solver()

# ============================================================
# Domain constraints
# ============================================================
for t in range(N):
    solver.add(rank[t] >= 1, rank[t] <= N)

for p in range(N):
    solver.add(pos[p] >= 0, pos[p] <= N-1)  # 0-indexed team IDs

# Bijection: rank and pos are inverses
for t in range(N):
    solver.add(pos[rank[t] - 1] == t)

for p in range(N):
    solver.add(rank[pos[p]] == p + 1)

# All ranks distinct
solver.add(Distinct(rank))

# ============================================================
# Constraint 1: Must-above (20 pairs)
# Format: T05 must rank above T18 => rank[4] < rank[17]
# ============================================================
must_above = [
    (4, 17),   # T05 above T18
    (9, 10),   # T10 above T11
    (6, 27),   # T07 above T28
    (7, 18),   # T08 above T19
    (1, 26),   # T02 above T27
    (3, 20),   # T04 above T21
    (2, 11),   # T03 above T12
    (5, 16),   # T06 above T17
    (8, 24),   # T09 above T25
    (0, 29),   # T01 above T30
    (12, 28),  # T13 above T29
    (13, 19),  # T14 above T20
    (14, 15),  # T15 above T16
    (21, 7),   # T22 above T08
    (22, 2),   # T23 above T03
    (23, 6),   # T24 above T07
    (25, 4),   # T26 above T05
    (24, 13),  # T25 above T14
    (19, 21),  # T20 above T22
    (27, 14),  # T28 above T15
]

for a, b in must_above:
    solver.add(rank[a] < rank[b])

# ============================================================
# Constraint 2: Adjacency bans (15 pairs)
# Teams cannot be adjacent in ranking: |rank[a] - rank[b]| != 1
# ============================================================
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

# ============================================================
# Constraint 3: Forbid-top constraints
# ============================================================
# T27 cannot be in top 3 => rank[26] > 3
solver.add(rank[26] > 3)
# T14 cannot be in top 5 => rank[13] > 5
solver.add(rank[13] > 5)
# T18 cannot be in top 4 => rank[17] > 4
solver.add(rank[17] > 4)
# T21 cannot be in top 2 => rank[20] > 2
solver.add(rank[20] > 2)
# T22 cannot be in top 6 => rank[21] > 6
solver.add(rank[21] > 6)
# T19 cannot be in top 8 => rank[18] > 8
solver.add(rank[18] > 8)
# T16 cannot be in top 7 => rank[15] > 7
solver.add(rank[15] > 7)
# T29 cannot be in top 10 => rank[28] > 10
solver.add(rank[28] > 10)

# ============================================================
# Constraint 4: Forbid-block constraints
# ============================================================
# T14 cannot be in positions 11-15 => rank[13] < 11 or rank[13] > 15
solver.add(Or(rank[13] < 11, rank[13] > 15))
# T20 cannot be in positions 5-9 => rank[19] < 5 or rank[19] > 9
solver.add(Or(rank[19] < 5, rank[19] > 9))
# T23 cannot be in positions 13-17 => rank[22] < 13 or rank[22] > 17
solver.add(Or(rank[22] < 13, rank[22] > 17))
# T02 cannot be in positions 21-25 => rank[1] < 21 or rank[1] > 25
solver.add(Or(rank[1] < 21, rank[1] > 25))
# T09 cannot be in positions 26-30 => rank[8] < 26 or rank[8] > 30 (i.e., rank[8] < 26)
solver.add(rank[8] < 26)

# ============================================================
# Constraint 5: Diversity constraint
# In any consecutive window of 5 teams, no more than 2 teams from the same group
# ============================================================
# Groups: A:0-4, B:5-9, C:10-14, D:15-19, E:20-24, F:25-29
groups = [0]*5 + [1]*5 + [2]*5 + [3]*5 + [4]*5 + [5]*5  # group id for each team

# For each window starting at position p (1-indexed, p from 1 to 26)
# Window covers positions p, p+1, p+2, p+3, p+4
# For each group g, count teams from group g in the window <= 2
for p in range(1, N - 4 + 1):  # p = 1..26
    for g in range(6):
        # Count teams in window [p, p+4] that belong to group g
        count_expr = Sum([If(And(rank[t] >= p, rank[t] <= p+4, groups[t] == g), 1, 0) for t in range(N)])
        solver.add(count_expr <= 2)

# ============================================================
# Constraint 6: Seed quota
# At least 6 seed teams (T01-T10, indices 0-9) in top 10 positions
# ============================================================
seed_count = Sum([If(rank[t] <= 10, 1, 0) for t in range(10)])
solver.add(seed_count >= 6)

# ============================================================
# Constraint 7: Violation bound
# Total weighted violations <= 650
# A violation occurs when a lower-ranked team beat a higher-ranked team
# ============================================================
# For each pair (i,j) with i < j:
# If winner[i][j] is True (i beats j), then violation if rank[i] > rank[j] (i is lower ranked)
# If winner[i][j] is False (j beats i), then violation if rank[j] > rank[i] (j is lower ranked)
violation_terms = []
for i in range(N):
    for j in range(i+1, N):
        w = weight[i][j]
        if winner[i][j]:
            # i beats j, violation if rank[i] > rank[j]
            violation_terms.append(If(rank[i] > rank[j], w, 0))
        else:
            # j beats i, violation if rank[j] > rank[i]
            violation_terms.append(If(rank[j] > rank[i], w, 0))

total_violations = Sum(violation_terms)
solver.add(total_violations <= 650)

# ============================================================
# Solve
# ============================================================
print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    ranking = [m.eval(pos[p]).as_long() for p in range(N)]
    # Convert to 1-indexed team IDs
    ranking_teams = [f"T{t+1:02d}" for t in ranking]
    
    # Compute violations for verification
    total_v = 0
    for i in range(N):
        for j in range(i+1, N):
            w = weight[i][j]
            ri = ranking.index(i) + 1  # rank of i
            rj = ranking.index(j) + 1  # rank of j
            if winner[i][j] and ri > rj:
                total_v += w
            elif not winner[i][j] and rj > ri:
                total_v += w
    
    print("STATUS: sat")
    print(f"Ranking: {ranking_teams}")
    print(f"Total weighted violations: {total_v}")
    
    # Verify all constraints
    print("\n=== Constraint Verification ===")
    
    # Must-above
    ok = True
    for a, b in must_above:
        ra = ranking.index(a) + 1
        rb = ranking.index(b) + 1
        if ra >= rb:
            print(f"FAIL must-above: T{a+1:02d} (rank {ra}) not above T{b+1:02d} (rank {rb})")
            ok = False
    if ok:
        print("Must-above: OK")
    
    # Adjacency bans
    ok = True
    for a, b in adj_bans:
        ra = ranking.index(a) + 1
        rb = ranking.index(b) + 1
        if abs(ra - rb) == 1:
            print(f"FAIL adjacency ban: T{a+1:02d} (rank {ra}) and T{b+1:02d} (rank {rb}) are adjacent")
            ok = False
    if ok:
        print("Adjacency bans: OK")
    
    # Forbid-top
    checks = [(26, 3, "T27 top 3"), (13, 5, "T14 top 5"), (17, 4, "T18 top 4"),
              (20, 2, "T21 top 2"), (21, 6, "T22 top 6"), (18, 8, "T19 top 8"),
              (15, 7, "T16 top 7"), (28, 10, "T29 top 10")]
    ok = True
    for t, limit, desc in checks:
        r = ranking.index(t) + 1
        if r <= limit:
            print(f"FAIL forbid-top: {desc} (rank {r})")
            ok = False
    if ok:
        print("Forbid-top: OK")
    
    # Forbid-block
    checks = [(13, 11, 15, "T14 in 11-15"), (19, 5, 9, "T20 in 5-9"),
              (22, 13, 17, "T23 in 13-17"), (1, 21, 25, "T02 in 21-25"),
              (8, 26, 30, "T09 in 26-30")]
    ok = True
    for t, lo, hi, desc in checks:
        r = ranking.index(t) + 1
        if lo <= r <= hi:
            print(f"FAIL forbid-block: {desc} (rank {r})")
            ok = False
    if ok:
        print("Forbid-block: OK")
    
    # Diversity
    ok = True
    for p in range(1, N - 4 + 1):
        for g in range(6):
            count = sum(1 for t in range(N) if groups[t] == g and p <= ranking.index(t) + 1 <= p+4)
            if count > 2:
                print(f"FAIL diversity: window [{p},{p+4}] group {g} has {count} teams")
                ok = False
    if ok:
        print("Diversity: OK")
    
    # Seed quota
    seed_top10 = sum(1 for t in range(10) if ranking.index(t) + 1 <= 10)
    print(f"Seed quota: {seed_top10} seeds in top 10 (need >= 6)")
    if seed_top10 >= 6:
        print("Seed quota: OK")
    else:
        print("Seed quota: FAIL")
    
    # Violation bound
    print(f"Violation bound: {total_v} <= 650: {'OK' if total_v <= 650 else 'FAIL'}")
    
    # Total absolute deviation
    total_abs_dev = sum(abs(ranking.index(t) + 1 - (t + 1)) for t in range(N))
    print(f"Total absolute deviation: {total_abs_dev}")
    
else:
    print("STATUS: unsat")
    print("No solution found. Need to refine constraints.")