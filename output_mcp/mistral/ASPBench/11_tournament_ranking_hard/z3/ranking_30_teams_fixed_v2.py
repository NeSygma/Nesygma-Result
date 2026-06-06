from z3 import *

# ============================================================================
# Problem: Find a valid ranking for 30 teams with complex constraints
# ============================================================================

# ----------------------------------------------------------------------------
# 1. Declare teams, groups, seeds
# ----------------------------------------------------------------------------
teams = [f"T{i+1:02d}" for i in range(30)]  # T01 to T30
seeds = [f"T{i+1:02d}" for i in range(10)]   # T01 to T10

groups = {
    'A': [f"T{i+1:02d}" for i in range(5)],   # T01-T05
    'B': [f"T{i+1:02d}" for i in range(5, 10)], # T06-T10
    'C': [f"T{i+1:02d}" for i in range(10, 15)], # T11-T15
    'D': [f"T{i+1:02d}" for i in range(15, 20)], # T16-T20
    'E': [f"T{i+1:02d}" for i in range(20, 25)], # T21-T25
    'F': [f"T{i+1:02d}" for i in range(25, 30)]  # T26-T30
}

# ----------------------------------------------------------------------------
# 2. Generate match results (beats[winner][loser] = weight)
# ----------------------------------------------------------------------------
import random
random.seed(42)

# Initialize beats dictionary
beats = {t1: {t2: 0 for t2 in teams} for t1 in teams}

# Generate results
for i in range(30):
    for j in range(i+1, 30):
        weight = random.randint(1, 5)
        if (i + j) % 2 == 0:
            winner, loser = teams[i], teams[j]
        else:
            winner, loser = teams[j], teams[i]
        beats[winner][loser] = weight

# ----------------------------------------------------------------------------
# 3. Declare Z3 variables
# ----------------------------------------------------------------------------
solver = Solver()

# rank[t] = rank of team t (1..30)
rank = {t: Int(f"rank_{t}") for t in teams}

# pos[i] = team at position i (0-indexed, 0..29)
# Use a Python list of Z3 variables for the permutation
pos = [Int(f"pos_{i}") for i in range(30)]

# Total weighted violations
violations = Int("violations")

# ----------------------------------------------------------------------------
# 4. Add permutation constraints
# ----------------------------------------------------------------------------
# Each position has a team in [0,29] (0-indexed team indices)
for i in range(30):
    solver.add(pos[i] >= 0, pos[i] < 30)

# Each team appears exactly once in the permutation
solver.add(Distinct(pos))

# Link rank and pos: rank[t] = i+1  <=>  pos[i] = team_to_idx(t)
team_to_idx = {t: i for i, t in enumerate(teams)}
idx_to_team = teams

for t in teams:
    idx = team_to_idx[t]
    # If pos[i] = idx, then rank[t] = i+1
    solver.add(Or([And(pos[i] == idx, rank[t] == i+1) for i in range(30)]))

# Also, for each position i, the team at that position is teams[pos[i]], and its rank is i+1
for i in range(30):
    idx = pos[i]
    t = idx_to_team[idx]
    solver.add(rank[t] == i+1)

# ----------------------------------------------------------------------------
# 5. Add must-above constraints (20 pairs)
# ----------------------------------------------------------------------------
must_above_pairs = [
    ("T05", "T18"), ("T10", "T11"), ("T07", "T28"), ("T08", "T19"), ("T02", "T27"),
    ("T04", "T21"), ("T03", "T12"), ("T06", "T17"), ("T09", "T25"), ("T01", "T30"),
    ("T13", "T29"), ("T14", "T20"), ("T15", "T16"), ("T22", "T08"), ("T23", "T03"),
    ("T24", "T07"), ("T26", "T05"), ("T25", "T14"), ("T20", "T22"), ("T28", "T15")
]

for higher, lower in must_above_pairs:
    solver.add(rank[higher] < rank[lower])

# ----------------------------------------------------------------------------
# 6. Add adjacency bans (15 pairs)
# ----------------------------------------------------------------------------
adjacency_ban_pairs = [
    ("T02", "T03"), ("T04", "T05"), ("T06", "T07"), ("T08", "T09"), ("T10", "T11"),
    ("T12", "T13"), ("T14", "T15"), ("T16", "T17"), ("T18", "T19"), ("T20", "T21"),
    ("T22", "T23"), ("T24", "T25"), ("T26", "T27"), ("T28", "T29"), ("T01", "T30")
]

for a, b in adjacency_ban_pairs:
    solver.add(Abs(rank[a] - rank[b]) > 1)

# ----------------------------------------------------------------------------
# 7. Add forbid-top constraints (8 teams)
# ----------------------------------------------------------------------------
forbid_top = {
    "T27": [1, 2, 3],
    "T14": [1, 2, 3, 4, 5],
    "T18": [1, 2, 3, 4],
    "T21": [1, 2],
    "T22": [1, 2, 3, 4, 5, 6],
    "T19": [1, 2, 3, 4, 5, 6, 7, 8],
    "T16": [1, 2, 3, 4, 5, 6, 7],
    "T29": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

for team, forbidden_positions in forbid_top.items():
    for pos in forbidden_positions:
        solver.add(rank[team] != pos)

# ----------------------------------------------------------------------------
# 8. Add forbid-block constraints (5 teams)
# ----------------------------------------------------------------------------
forbid_block = {
    "T14": (11, 15),
    "T20": (5, 9),
    "T23": (13, 17),
    "T02": (21, 25),
    "T09": (26, 30)
}

for team, (start, end) in forbid_block.items():
    solver.add(rank[team] < start, rank[team] > end)

# ----------------------------------------------------------------------------
# 9. Add diversity constraint: in any consecutive window of 5 teams, no more than 2 teams from the same group
# ----------------------------------------------------------------------------
# For each window of 5 consecutive positions
for i in range(26):  # positions 0-25 (1-26 in 1-indexed)
    # Get the teams in this window
    window_teams = [pos[j] for j in range(i, i+5)]
    for group_name, group_teams in groups.items():
        # Count how many teams in this window belong to this group
        count = Sum([If(Or([window_teams[k] == team_to_idx[t] for t in group_teams]), 1, 0) for k in range(5)])
        solver.add(count <= 2)

# ----------------------------------------------------------------------------
# 10. Add seed quota: at least 6 seed teams (T01-T10) in top 10 positions
# ----------------------------------------------------------------------------
seed_count = Sum([If(rank[t] <= 10, 1, 0) for t in seeds])
solver.add(seed_count >= 6)

# ----------------------------------------------------------------------------
# 11. Calculate total weighted violations
# ----------------------------------------------------------------------------
# A violation occurs when a lower-ranked team beat a higher-ranked team
# For each pair (a,b) where a beats b, if rank[a] > rank[b], add beats[a][b] to violations
violation_terms = []
for a in teams:
    for b in teams:
        if a != b:
            w = beats[a][b]
            if w > 0:  # a beats b with weight w
                violation_terms.append(If(rank[a] > rank[b], w, 0))

solver.add(violations == Sum(violation_terms))
solver.add(violations <= 650)

# ----------------------------------------------------------------------------
# 12. Check satisfiability
# ----------------------------------------------------------------------------
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract ranking
    ranking = []
    for i in range(30):
        team_idx = model.eval(pos[i], model_completion=True).as_long()
        ranking.append(teams[team_idx])
    
    # Extract violations
    total_violations = model.eval(violations, model_completion=True).as_long()
    
    # Print ranking
    print("ranking:")
    for i, team in enumerate(ranking):
        print(f"  {i+1}: {team}")
    
    # Print violations
    print(f"violations = {total_violations}")
    
    # Verify all constraints are satisfied
    print("\nVerifying constraints...")
    
    # Check must-above
    print("Must-above constraints satisfied:")
    for higher, lower in must_above_pairs:
        if model.eval(rank[higher], model_completion=True).as_long() < model.eval(rank[lower], model_completion=True).as_long():
            print(f"  ✓ {higher} < {lower}")
        else:
            print(f"  ✗ {higher} >= {lower} (VIOLATION)")
    
    # Check adjacency bans
    print("\nAdjacency bans satisfied:")
    for a, b in adjacency_ban_pairs:
        if abs(model.eval(rank[a], model_completion=True).as_long() - model.eval(rank[b], model_completion=True).as_long()) > 1:
            print(f"  ✓ {a} and {b} not adjacent")
        else:
            print(f"  ✗ {a} and {b} are adjacent (VIOLATION)")
    
    # Check forbid-top
    print("\nForbid-top constraints satisfied:")
    for team, forbidden_positions in forbid_top.items():
        r = model.eval(rank[team], model_completion=True).as_long()
        if r not in forbidden_positions:
            print(f"  ✓ {team} not in top forbidden positions")
        else:
            print(f"  ✗ {team} in forbidden position {r} (VIOLATION)")
    
    # Check forbid-block
    print("\nForbid-block constraints satisfied:")
    for team, (start, end) in forbid_block.items():
        r = model.eval(rank[team], model_completion=True).as_long()
        if r < start or r > end:
            print(f"  ✓ {team} not in forbidden block [{start},{end}]")
        else:
            print(f"  ✗ {team} in forbidden block [{start},{end}] (VIOLATION)")
    
    # Check diversity
    print("\nDiversity constraints satisfied:")
    valid_diversity = True
    for i in range(26):
        window_teams = [model.eval(pos[j], model_completion=True).as_long() for j in range(i, i+5)]
        for group_name, group_teams in groups.items():
            count = sum(1 for idx in window_teams if teams[idx] in group_teams)
            if count > 2:
                print(f"  ✗ Window {i+1}-{i+5} has {count} teams from group {group_name} (VIOLATION)")
                valid_diversity = False
    if valid_diversity:
        print("  ✓ All windows have ≤ 2 teams from the same group")
    
    # Check seed quota
    seed_count = sum(1 for t in seeds if model.eval(rank[t], model_completion=True).as_long() <= 10)
    print(f"\nSeed quota: {seed_count} seed teams in top 10 (required ≥ 6)")
    if seed_count >= 6:
        print("  ✓ Seed quota satisfied")
    else:
        print("  ✗ Seed quota not satisfied (VIOLATION)")
    
    # Check violation bound
    print(f"\nTotal weighted violations: {total_violations} (required ≤ 650)")
    if total_violations <= 650:
        print("  ✓ Violation bound satisfied")
    else:
        print("  ✗ Violation bound exceeded (VIOLATION)")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")