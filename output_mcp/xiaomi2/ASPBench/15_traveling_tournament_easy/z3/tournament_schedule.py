from z3 import *
import math

BENCHMARK_MODE = True

# Team data
teams = ['A', 'B', 'C', 'D']
coords = [(0,0), (3,4), (6,0), (2,8)]
n_teams = 4
n_rounds = 6
n_matches_per_round = 2

# Compute exact Euclidean distances
dist = {}
for i in range(n_teams):
    for j in range(n_teams):
        if i != j:
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist[(i,j)] = math.sqrt(dx*dx + dy*dy)

print("Exact Euclidean distances:")
for i in range(n_teams):
    for j in range(i+1, n_teams):
        print(f"  {teams[i]}-{teams[j]}: {dist[(i,j)]:.4f}")

# Expected fixed total = 2 * sum of all pairwise distances
pair_sum = sum(dist[(i,j)] for i in range(n_teams) for j in range(i+1, n_teams))
print(f"Sum of pairwise distances: {pair_sum:.4f}")
print(f"Expected total (2x): {2*pair_sum:.4f} ≈ {round(2*pair_sum)}")
print()

# Decision variables: home[r][m] and away[r][m] are team indices (0-3)
home = [[Int(f'home_{r}_{m}') for m in range(n_matches_per_round)] for r in range(n_rounds)]
away = [[Int(f'away_{r}_{m}') for m in range(n_matches_per_round)] for r in range(n_rounds)]

opt = Optimize()

# --- Constraints ---

# 1. Domain: team indices in [0, 3], home != away
for r in range(n_rounds):
    for m in range(n_matches_per_round):
        opt.add(home[r][m] >= 0, home[r][m] < n_teams)
        opt.add(away[r][m] >= 0, away[r][m] < n_teams)
        opt.add(home[r][m] != away[r][m])

# 2. Each round: all 4 teams play exactly once (all 4 values distinct)
for r in range(n_rounds):
    opt.add(Distinct([home[r][0], away[r][0], home[r][1], away[r][1]]))

# 3. Double round-robin: each ordered pair (home=i, away=j) appears exactly once
for i in range(n_teams):
    for j in range(n_teams):
        if i != j:
            appearances = Sum([If(And(home[r][m] == i, away[r][m] == j), 1, 0) 
                              for r in range(n_rounds) for m in range(n_matches_per_round)])
            opt.add(appearances == 1)

# 4. No team plays more than 2 consecutive home or away games
for t in range(n_teams):
    for r in range(n_rounds - 2):
        # No 3 consecutive home games
        opt.add(Not(And(
            Or(home[r][0] == t, home[r][1] == t),
            Or(home[r+1][0] == t, home[r+1][1] == t),
            Or(home[r+2][0] == t, home[r+2][1] == t)
        )))
        # No 3 consecutive away games
        opt.add(Not(And(
            Or(away[r][0] == t, away[r][1] == t),
            Or(away[r+1][0] == t, away[r+1][1] == t),
            Or(away[r+2][0] == t, away[r+2][1] == t)
        )))

# --- Objective: minimize total travel distance ---
# Use scaled integer distances (×10000) for clean integer optimization
SCALE = 10000
total_dist = Sum([If(And(away[r][m] == i, home[r][m] == j), 
                     round(dist[(i,j)] * SCALE), 0) 
                 for r in range(n_rounds) 
                 for m in range(n_matches_per_round)
                 for i in range(n_teams)
                 for j in range(n_teams)
                 if i != j])

opt.minimize(total_dist)

# --- Solve ---
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    total_exact = 0.0
    schedule = []
    for r in range(n_rounds):
        round_matches = []
        for m in range(n_matches_per_round):
            h = model.evaluate(home[r][m]).as_long()
            a = model.evaluate(away[r][m]).as_long()
            round_matches.append({"home": teams[h], "away": teams[a]})
            total_exact += dist[(a, h)]
        schedule.append(round_matches)
    
    total_int = round(total_exact)
    
    print(f"total_distance = {total_int}")
    print(f"exact_total_distance = {total_exact:.4f}")
    print(f"feasible = True")
    print()
    
    for r, matches in enumerate(schedule):
        match_strs = [f"{m['home']}(H) vs {m['away']}(A)" for m in matches]
        print(f"  Round {r+1}: {', '.join(match_strs)}")
    
    # --- Verification ---
    print("\n--- Constraint Verification ---")
    
    # Verify double round-robin
    pair_count = {}
    for r in range(n_rounds):
        for m in range(n_matches_per_round):
            h = model.evaluate(home[r][m]).as_long()
            a = model.evaluate(away[r][m]).as_long()
            pair_count[(h, a)] = pair_count.get((h, a), 0) + 1
    
    drr_ok = True
    for i in range(n_teams):
        for j in range(n_teams):
            if i != j:
                c = pair_count.get((i, j), 0)
                if c != 1:
                    drr_ok = False
                    print(f"  FAIL: ({teams[i]} home, {teams[j]} away) appears {c} times")
    print(f"  Double round-robin: {'PASS' if drr_ok else 'FAIL'}")
    
    # Verify consecutive constraints
    consec_ok = True
    for t in range(n_teams):
        home_streak = 0
        away_streak = 0
        role_history = []
        for r in range(n_rounds):
            is_h = any(model.evaluate(home[r][m]).as_long() == t for m in range(n_matches_per_round))
            is_a = any(model.evaluate(away[r][m]).as_long() == t for m in range(n_matches_per_round))
            if is_h:
                home_streak += 1
                away_streak = 0
                role_history.append('H')
            elif is_a:
                away_streak += 1
                home_streak = 0
                role_history.append('A')
            if home_streak > 2 or away_streak > 2:
                consec_ok = False
                print(f"  FAIL: Team {teams[t]} streak violation at round {r+1} (H={home_streak}, A={away_streak})")
        print(f"  Team {teams[t]} role sequence: {''.join(role_history)}")
    print(f"  Consecutive constraints: {'PASS' if consec_ok else 'FAIL'}")
    
    # Verify each team plays once per round
    round_ok = True
    for r in range(n_rounds):
        players = set()
        for m in range(n_matches_per_round):
            players.add(model.evaluate(home[r][m]).as_long())
            players.add(model.evaluate(away[r][m]).as_long())
        if len(players) != 4:
            round_ok = False
            print(f"  FAIL: Round {r+1} has {len(players)} teams instead of 4")
    print(f"  Round structure (4 teams/round): {'PASS' if round_ok else 'FAIL'}")
    
    all_ok = drr_ok and consec_ok and round_ok
    print(f"\n  ALL CONSTRAINTS SATISFIED: {all_ok}")
    
    # Print distance breakdown
    print("\n--- Distance Breakdown ---")
    for r, matches in enumerate(schedule):
        for m_info in matches:
            h_name, a_name = m_info['home'], m_info['away']
            h_idx, a_idx = teams.index(h_name), teams.index(a_name)
            d = dist[(a_idx, h_idx)]
            print(f"  Round {r+1}: {a_name} travels to {h_name}: {d:.4f}")
    print(f"  TOTAL: {total_exact:.4f} → rounded to {total_int}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")