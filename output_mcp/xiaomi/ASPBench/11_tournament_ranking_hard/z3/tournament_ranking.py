from z3 import *
import random

# ============================================================
# 1. Generate match results using the given pattern
# ============================================================
random.seed(42)
teams = [f"T{i+1:02d}" for i in range(30)]

# beats[i][j] = True means team i beats team j
beats = [[False]*30 for _ in range(30)]
weight = [[0]*30 for _ in range(30)]

for i in range(30):
    for j in range(i+1, 30):
        w = random.randint(1, 5)
        weight[i][j] = w
        weight[j][i] = w
        if (i + j) % 2 == 0:
            beats[i][j] = True
        else:
            beats[j][i] = True

# ============================================================
# 2. Z3 Model Setup
# ============================================================
solver = Solver()
solver.set("timeout", 300000)  # 5 minute timeout

N = 30

# rank[i] = position (1..30) of team i
rank = [Int(f'rank_{i}') for i in range(N)]

# All ranks are between 1 and 30, all distinct
for i in range(N):
    solver.add(rank[i] >= 1, rank[i] <= N)
solver.add(Distinct(rank))

# ============================================================
# 3. Must-above constraints (20 pairs)
# ============================================================
# Map team names to indices
team_idx = {f"T{i+1:02d}": i for i in range(30)}

must_above = [
    ("T05", "T18"), ("T10", "T11"), ("T07", "T28"), ("T08", "T19"),
    ("T02", "T27"), ("T04", "T21"), ("T03", "T12"), ("T06", "T17"),
    ("T09", "T25"), ("T01", "T30"), ("T13", "T29"), ("T14", "T20"),
    ("T15", "T16"), ("T22", "T08"), ("T23", "T03"), ("T24", "T07"),
    ("T26", "T05"), ("T25", "T14"), ("T20", "T22"), ("T28", "T15")
]

for above, below in must_above:
    a = team_idx[above]
    b = team_idx[below]
    solver.add(rank[a] < rank[b])

# ============================================================
# 4. Adjacency bans (15 pairs)
# ============================================================
adj_bans = [
    ("T02","T03"), ("T04","T05"), ("T06","T07"), ("T08","T09"),
    ("T10","T11"), ("T12","T13"), ("T14","T15"), ("T16","T17"),
    ("T18","T19"), ("T20","T21"), ("T22","T23"), ("T24","T25"),
    ("T26","T27"), ("T28","T29"), ("T01","T30")
]

for a_name, b_name in adj_bans:
    a = team_idx[a_name]
    b = team_idx[b_name]
    solver.add(Abs(rank[a] - rank[b]) != 1)

# ============================================================
# 5. Forbid-top constraints (8 teams)
# ============================================================
# T27 cannot be in top 3 => rank >= 4
# T14 in top 5 => rank >= 6
# T18 in top 4 => rank >= 5
# T21 in top 2 => rank >= 3
# T22 in top 6 => rank >= 7
# T19 in top 8 => rank >= 9
# T16 in top 7 => rank >= 8
# T29 in top 10 => rank >= 11

forbid_top = [
    ("T27", 3), ("T14", 5), ("T18", 4), ("T21", 2),
    ("T22", 6), ("T19", 8), ("T16", 7), ("T29", 10)
]

for team_name, top_k in forbid_top:
    t = team_idx[team_name]
    solver.add(rank[t] >= top_k + 1)

# ============================================================
# 6. Forbid-block constraints (5 teams)
# ============================================================
# T14 cannot be in positions 11-15
# T20 in positions 5-9
# T23 in positions 13-17
# T02 in positions 21-25
# T09 in positions 26-30

forbid_blocks = [
    ("T14", 11, 15), ("T20", 5, 9), ("T23", 13, 17),
    ("T02", 21, 25), ("T09", 26, 30)
]

for team_name, lo, hi in forbid_blocks:
    t = team_idx[team_name]
    solver.add(Or(rank[t] < lo, rank[t] > hi))

# ============================================================
# 7. Diversity constraint: In any consecutive window of 5,
#    no more than 2 teams from the same group
# ============================================================
groups = {
    'A': [0,1,2,3,4],      # T01-T05
    'B': [5,6,7,8,9],      # T06-T10
    'C': [10,11,12,13,14],  # T11-T15
    'D': [15,16,17,18,19],  # T16-T20
    'E': [20,21,22,23,24],  # T21-T25
    'F': [25,26,27,28,29],  # T26-T30
}

# For each starting position p (1..26) and each group,
# at most 2 teams from that group in positions p..p+4
for p in range(1, 27):  # positions 1 to 26 (window covers p to p+4)
    for gname, gmembers in groups.items():
        # Count how many group members are in this window
        count = Sum([If(And(rank[t] >= p, rank[t] <= p + 4), 1, 0) for t in gmembers])
        solver.add(count <= 2)

# ============================================================
# 8. Seed quota: At least 6 seed teams (T01-T10) in top 10
# ============================================================
seed_teams = list(range(0, 10))  # T01-T10
seed_in_top10 = Sum([If(rank[t] <= 10, 1, 0) for t in seed_teams])
solver.add(seed_in_top10 >= 6)

# ============================================================
# 9. Violation bound: Total weighted violations <= 650
# ============================================================
# A violation: team i beat team j, but rank[i] > rank[j] (i ranked lower)
# Weight of violation = weight[i][j]
violation_terms = []
for i in range(N):
    for j in range(N):
        if i != j and beats[i][j]:
            # i beat j, violation if i is ranked lower (rank[i] > rank[j])
            violation_terms.append(If(rank[i] > rank[j], weight[i][j], 0))

total_violations = Sum(violation_terms)
solver.add(total_violations <= 650)

# ============================================================
# 10. Check and print result
# ============================================================
print("Solving tournament ranking problem...")
print(f"Teams: {N}, Must-above: {len(must_above)}, Adj-bans: {len(adj_bans)}")
print(f"Forbid-top: {len(forbid_top)}, Forbid-block: {len(forbid_blocks)}")

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract ranking
    ranking = []
    for pos in range(1, N+1):
        for t in range(N):
            if m.evaluate(rank[t] == pos, model_completion=True):
                ranking.append(teams[t])
                break
    
    print(f"Ranking: {ranking}")
    
    # Compute violations
    total_v = 0
    for i in range(N):
        for j in range(N):
            if i != j and beats[i][j]:
                ri = m.evaluate(rank[i], model_completion=True).as_long()
                rj = m.evaluate(rank[j], model_completion=True).as_long()
                if ri > rj:
                    total_v += weight[i][j]
    
    print(f"Total weighted violations: {total_v}")
    
    # Verify constraints
    # Must-above
    for above, below in must_above:
        a, b = team_idx[above], team_idx[below]
        ra = m.evaluate(rank[a], model_completion=True).as_long()
        rb = m.evaluate(rank[b], model_completion=True).as_long()
        assert ra < rb, f"Must-above violated: {above}({ra}) should be above {below}({rb})"
    
    # Adjacency bans
    for a_name, b_name in adj_bans:
        a, b = team_idx[a_name], team_idx[b_name]
        ra = m.evaluate(rank[a], model_completion=True).as_long()
        rb = m.evaluate(rank[b], model_completion=True).as_long()
        assert abs(ra - rb) != 1, f"Adjacency ban violated: {a_name}({ra}), {b_name}({rb})"
    
    # Forbid-top
    for team_name, top_k in forbid_top:
        t = team_idx[team_name]
        rt = m.evaluate(rank[t], model_completion=True).as_long()
        assert rt > top_k, f"Forbid-top violated: {team_name}({rt}) in top {top_k}"
    
    # Forbid-block
    for team_name, lo, hi in forbid_blocks:
        t = team_idx[team_name]
        rt = m.evaluate(rank[t], model_completion=True).as_long()
        assert not (lo <= rt <= hi), f"Forbid-block violated: {team_name}({rt}) in [{lo},{hi}]"
    
    # Diversity
    for p in range(1, 27):
        for gname, gmembers in groups.items():
            count = sum(1 for t in gmembers if p <= m.evaluate(rank[t], model_completion=True).as_long() <= p+4)
            assert count <= 2, f"Diversity violated at pos {p}, group {gname}: {count} teams"
    
    # Seed quota
    seed_count = sum(1 for t in seed_teams if m.evaluate(rank[t], model_completion=True).as_long() <= 10)
    assert seed_count >= 6, f"Seed quota violated: only {seed_count} seeds in top 10"
    
    # Violation bound
    assert total_v <= 650, f"Violation bound violated: {total_v} > 650"
    
    print("All constraints verified!")
    print(f"Seed teams in top 10: {seed_count}")
    
    # Total absolute deviation
    total_abs_dev = 0
    for t in range(N):
        rt = m.evaluate(rank[t], model_completion=True).as_long()
        total_abs_dev += abs(rt - (t+1))
    print(f"Total absolute deviation: {total_abs_dev}")
    
    # Print detailed ranking
    print("\nDetailed Ranking:")
    for pos in range(1, N+1):
        for t in range(N):
            if m.evaluate(rank[t] == pos, model_completion=True):
                group = 'A' if t < 5 else 'B' if t < 10 else 'C' if t < 15 else 'D' if t < 20 else 'E' if t < 25 else 'F'
                seed_mark = "*" if t < 10 else " "
                print(f"  Rank {pos:2d}: {teams[t]} (Group {group}) {seed_mark}")
                break

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")