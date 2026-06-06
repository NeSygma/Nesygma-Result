from z3 import *

# Problem setup
teams = [f"T{i:02d}" for i in range(1, 31)]
seeds = teams[:10]  # T01-T10

# Groups
groups = {
    'A': teams[0:5],   # T01-T05
    'B': teams[5:10],  # T06-T10
    'C': teams[10:15], # T11-T15
    'D': teams[15:20], # T16-T20
    'E': teams[20:25], # T21-T25
    'F': teams[25:30]  # T26-T30
}

# Create solver
solver = Solver()

# Variables: position of each team (1-30)
positions = {team: Int(f"pos_{team}") for team in teams}

# All positions must be distinct and in range 1-30
for team in teams:
    solver.add(positions[team] >= 1)
    solver.add(positions[team] <= 30)
solver.add(Distinct([positions[team] for team in teams]))

# Generate match results based on the given pattern
import random
random.seed(42)
match_results = {}  # (winner, loser) -> weight
for i in range(30):
    for j in range(i+1, 30):
        weight = random.randint(1, 5)
        if (i + j) % 2 == 0:
            winner, loser = teams[i], teams[j]
        else:
            winner, loser = teams[j], teams[i]
        match_results[(winner, loser)] = weight

# Function to calculate total weighted violations
def calculate_violations():
    violations = []
    for (winner, loser), weight in match_results.items():
        # Violation if loser is ranked higher (lower position number) than winner
        violation = If(positions[loser] < positions[winner], weight, 0)
        violations.append(violation)
    return Sum(violations)

total_violations = calculate_violations()
solver.add(total_violations <= 650)

# 1. Must-above constraints
must_above_pairs = [
    ("T05", "T18"), ("T10", "T11"), ("T07", "T28"), ("T08", "T19"),
    ("T02", "T27"), ("T04", "T21"), ("T03", "T12"), ("T06", "T17"),
    ("T09", "T25"), ("T01", "T30"), ("T13", "T29"), ("T14", "T20"),
    ("T15", "T16"), ("T22", "T08"), ("T23", "T03"), ("T24", "T07"),
    ("T26", "T05"), ("T25", "T14"), ("T20", "T22"), ("T28", "T15")
]
for team_a, team_b in must_above_pairs:
    solver.add(positions[team_a] < positions[team_b])

# 2. Adjacency bans
adjacency_bans = [
    ("T02", "T03"), ("T04", "T05"), ("T06", "T07"), ("T08", "T09"),
    ("T10", "T11"), ("T12", "T13"), ("T14", "T15"), ("T16", "T17"),
    ("T18", "T19"), ("T20", "T21"), ("T22", "T23"), ("T24", "T25"),
    ("T26", "T27"), ("T28", "T29"), ("T01", "T30")
]
for team_a, team_b in adjacency_bans:
    # Not adjacent means |pos_a - pos_b| != 1
    solver.add(Abs(positions[team_a] - positions[team_b]) != 1)

# 3. Forbid-top constraints
forbid_top = {
    "T27": 3,   # cannot be in top 3 (positions 1-3)
    "T14": 5,   # cannot be in top 5 (positions 1-5)
    "T18": 4,   # cannot be in top 4 (positions 1-4)
    "T21": 2,   # cannot be in top 2 (positions 1-2)
    "T22": 6,   # cannot be in top 6 (positions 1-6)
    "T19": 8,   # cannot be in top 8 (positions 1-8)
    "T16": 7,   # cannot be in top 7 (positions 1-7)
    "T29": 10   # cannot be in top 10 (positions 1-10)
}
for team, max_pos in forbid_top.items():
    solver.add(positions[team] > max_pos)

# 4. Forbid-block constraints
forbid_block = {
    "T14": (11, 15),  # cannot be in positions 11-15
    "T20": (5, 9),    # cannot be in positions 5-9
    "T23": (13, 17),  # cannot be in positions 13-17
    "T02": (21, 25),  # cannot be in positions 21-25
    "T09": (26, 30)   # cannot be in positions 26-30
}
for team, (low, high) in forbid_block.items():
    solver.add(Or(positions[team] < low, positions[team] > high))

# 5. Diversity constraint: no more than 2 teams from same group in any 5-consecutive window
# We need to check windows of positions 1-5, 2-6, ..., 26-30
# For each window, we need to ensure that for each group, at most 2 teams are in that window
for start in range(1, 27):  # 26 windows of 5 consecutive positions
    for group_name, group_teams in groups.items():
        # For each team in the group, check if it's in the window
        # We need to count how many are in the window
        # Use a more efficient approach: for each team, create a boolean indicating if it's in window
        in_window = []
        for team in group_teams:
            # Check if position is in [start, start+4]
            in_window.append(And(positions[team] >= start, positions[team] <= start + 4))
        # Count how many are true
        count = Sum([If(expr, 1, 0) for expr in in_window])
        solver.add(count <= 2)

# 6. Seed quota: at least 6 seed teams in top 10 positions
seeds_in_top_10 = Sum([If(positions[seed] <= 10, 1, 0) for seed in seeds])
solver.add(seeds_in_top_10 >= 6)

# Check for solution
print("Solving...")
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract ranking
    ranking = sorted([(team, model[positions[team]].as_long()) for team in teams], 
                     key=lambda x: x[1])
    
    print("\nRanking (position: team):")
    for team, pos in ranking:
        print(f"  {pos:2d}: {team}")
    
    # Calculate violations using model.eval
    total_viol = model.eval(total_violations).as_long()
    print(f"\nTotal weighted violations: {total_viol}")
    
    # Verify constraints
    print("\nConstraint verification:")
    
    # Must-above
    print("  Must-above constraints: ", end="")
    all_ok = True
    for team_a, team_b in must_above_pairs:
        if model[positions[team_a]].as_long() >= model[positions[team_b]].as_long():
            print(f"FAIL ({team_a} not above {team_b})")
            all_ok = False
            break
    if all_ok:
        print("OK")
    
    # Adjacency bans
    print("  Adjacency bans: ", end="")
    all_ok = True
    for team_a, team_b in adjacency_bans:
        if abs(model[positions[team_a]].as_long() - model[positions[team_b]].as_long()) == 1:
            print(f"FAIL ({team_a} and {team_b} adjacent)")
            all_ok = False
            break
    if all_ok:
        print("OK")
    
    # Forbid-top
    print("  Forbid-top constraints: ", end="")
    all_ok = True
    for team, max_pos in forbid_top.items():
        if model[positions[team]].as_long() <= max_pos:
            print(f"FAIL ({team} in top {max_pos})")
            all_ok = False
            break
    if all_ok:
        print("OK")
    
    # Forbid-block
    print("  Forbid-block constraints: ", end="")
    all_ok = True
    for team, (low, high) in forbid_block.items():
        pos = model[positions[team]].as_long()
        if low <= pos <= high:
            print(f"FAIL ({team} in block {low}-{high})")
            all_ok = False
            break
    if all_ok:
        print("OK")
    
    # Diversity
    print("  Diversity constraint: ", end="")
    all_ok = True
    for start in range(1, 27):
        window_positions = list(range(start, start + 5))
        for group_name, group_teams in groups.items():
            count = sum(1 for team in group_teams 
                       if model[positions[team]].as_long() in window_positions)
            if count > 2:
                print(f"FAIL (window {start}-{start+4}, group {group_name}: {count} teams)")
                all_ok = False
                break
        if not all_ok:
            break
    if all_ok:
        print("OK")
    
    # Seed quota
    print("  Seed quota: ", end="")
    seeds_in_top = sum(1 for seed in seeds if model[positions[seed]].as_long() <= 10)
    if seeds_in_top >= 6:
        print(f"OK ({seeds_in_top} seeds in top 10)")
    else:
        print(f"FAIL ({seeds_in_top} seeds in top 10, need ≥6)")
    
    # Violation bound
    print("  Violation bound: ", end="")
    if total_viol <= 650:
        print(f"OK ({total_viol} ≤ 650)")
    else:
        print(f"FAIL ({total_viol} > 650)")
    
    # Calculate total absolute deviation
    total_deviation = 0
    for i, team in enumerate(teams, 1):
        expected_pos = i
        actual_pos = model[positions[team]].as_long()
        total_deviation += abs(actual_pos - expected_pos)
    print(f"\nTotal absolute deviation: {total_deviation}")
    
    print("\nanswer: Found valid ranking")

elif result == unsat:
    print("STATUS: unsat")
    print("No valid ranking found with current constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")