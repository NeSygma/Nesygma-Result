from z3 import *

# Teams: 0=A, 1=B, 2=C, 3=D, 4=E, 5=F
N_TEAMS = 6
N_ROUNDS = 10
N_MATCHES_PER_ROUND = 3

# Distance matrix (scaled by 10)
dist = {}
teams = [0, 1, 2, 3, 4, 5]
team_names = ['A', 'B', 'C', 'D', 'E', 'F']

# Symmetric distances
d = {(0,1): 100, (0,2): 94, (0,3): 150, (0,4): 180, (0,5): 170,
     (1,2): 94, (1,3): 180, (1,4): 150, (1,5): 94,
     (2,3): 86, (2,4): 86, (2,5): 100,
     (3,4): 100, (3,5): 170,
     (4,5): 94}
for (i,j), v in d.items():
    dist[(i,j)] = v
    dist[(j,i)] = v

solver = Solver()

# Decision variables: for each round r and match slot m, home[r][m] and away[r][m] are team indices
home = [[Int(f'home_{r}_{m}') for m in range(N_MATCHES_PER_ROUND)] for r in range(N_ROUNDS)]
away = [[Int(f'away_{r}_{m}') for m in range(N_MATCHES_PER_ROUND)] for r in range(N_ROUNDS)]

# For each team, track if they play home in round r
play_home = [[Bool(f'ph_{t}_{r}') for r in range(N_ROUNDS)] for t in range(N_TEAMS)]
play_away = [[Bool(f'pa_{t}_{r}') for r in range(N_ROUNDS)] for t in range(N_TEAMS)]

# For each team, who is their opponent in round r
opponent = [[Int(f'opp_{t}_{r}') for r in range(N_ROUNDS)] for t in range(N_TEAMS)]

# Location tracking: loc[t][r] = team index of the city where team t is located at end of round r
loc = [[Int(f'loc_{t}_{r}') for r in range(N_ROUNDS)] for t in range(N_TEAMS)]

# --- Basic domain constraints ---
for r in range(N_ROUNDS):
    for m in range(N_MATCHES_PER_ROUND):
        solver.add(home[r][m] >= 0, home[r][m] < N_TEAMS)
        solver.add(away[r][m] >= 0, away[r][m] < N_TEAMS)
        solver.add(home[r][m] != away[r][m])

# --- Constraint 2: Each team plays exactly once per round ---
for r in range(N_ROUNDS):
    for t in range(N_TEAMS):
        is_home = Or([home[r][m] == t for m in range(N_MATCHES_PER_ROUND)])
        is_away = Or([away[r][m] == t for m in range(N_MATCHES_PER_ROUND)])
        solver.add(Or(is_home, is_away))
        solver.add(Not(And(is_home, is_away)))

# --- Constraint 1: Double round-robin ---
# Each ordered pair (t1, t2) with t1 != t2 plays exactly once
for t1 in range(N_TEAMS):
    for t2 in range(N_TEAMS):
        if t1 != t2:
            matches = []
            for r in range(N_ROUNDS):
                for m in range(N_MATCHES_PER_ROUND):
                    matches.append(And(home[r][m] == t1, away[r][m] == t2))
            # Exactly one: at least one, and at most one (pairwise exclusion)
            solver.add(Or(matches))
            for i in range(len(matches)):
                for j in range(i+1, len(matches)):
                    solver.add(Not(And(matches[i], matches[j])))

# --- Link play_home, play_away, opponent to match assignments ---
for t in range(N_TEAMS):
    for r in range(N_ROUNDS):
        solver.add(play_home[t][r] == Or([home[r][m] == t for m in range(N_MATCHES_PER_ROUND)]))
        solver.add(play_away[t][r] == Or([away[r][m] == t for m in range(N_MATCHES_PER_ROUND)]))
        
        opp_constraints = []
        for m in range(N_MATCHES_PER_ROUND):
            opp_constraints.append(And(home[r][m] == t, opponent[t][r] == away[r][m]))
            opp_constraints.append(And(away[r][m] == t, opponent[t][r] == home[r][m]))
        solver.add(Or(opp_constraints))

# --- Constraint 3: Stateful Travel - Location tracking ---
for t in range(N_TEAMS):
    for r in range(N_ROUNDS):
        solver.add(If(play_home[t][r], loc[t][r] == t, loc[t][r] == opponent[t][r]))

# --- Constraint 4: Consecutive game limit (max 3 consecutive home or away) ---
for t in range(N_TEAMS):
    for r in range(N_ROUNDS - 3):
        solver.add(Not(And(play_home[t][r], play_home[t][r+1], play_home[t][r+2], play_home[t][r+3])))
        solver.add(Not(And(play_away[t][r], play_away[t][r+1], play_away[t][r+2], play_away[t][r+3])))

# --- Constraint 5: Rivalry constraints ---
# A(0) and B(1) cannot play each other in round 0
for m in range(N_MATCHES_PER_ROUND):
    solver.add(Not(And(home[0][m] == 0, away[0][m] == 1)))
    solver.add(Not(And(home[0][m] == 1, away[0][m] == 0)))

# C(2) and D(3) cannot play each other in round 0
for m in range(N_MATCHES_PER_ROUND):
    solver.add(Not(And(home[0][m] == 2, away[0][m] == 3)))
    solver.add(Not(And(home[0][m] == 3, away[0][m] == 2)))

# --- Constraint 6: Mandatory Break - at least one sequence of 2 consecutive home games ---
for t in range(N_TEAMS):
    consecutive_home = []
    for r in range(N_ROUNDS - 1):
        consecutive_home.append(And(play_home[t][r], play_home[t][r+1]))
    solver.add(Or(consecutive_home))

# --- Constraint 7: Travel Fatigue ---
for t in range(N_TEAMS):
    for r in range(N_ROUNDS):
        if r + 1 < N_ROUNDS:
            loc_before = loc[t][r-1] if r > 0 else t
            
            for loc_val in range(N_TEAMS):
                for opp_val in range(N_TEAMS):
                    if loc_val != opp_val:
                        d_val = dist.get((loc_val, opp_val), 0)
                        if d_val > 140:
                            solver.add(
                                Implies(
                                    And(play_away[t][r], loc_before == loc_val, opponent[t][r] == opp_val),
                                    play_home[t][r+1]
                                )
                            )

# --- Symmetry breaking: order matches within a round by home team ---
for r in range(N_ROUNDS):
    for m in range(N_MATCHES_PER_ROUND - 1):
        solver.add(home[r][m] < home[r][m+1])

# --- Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("FEASIBLE: true")
    print()
    
    schedule = []
    for r in range(N_ROUNDS):
        round_matches = []
        for m in range(N_MATCHES_PER_ROUND):
            h = model.evaluate(home[r][m]).as_long()
            a = model.evaluate(away[r][m]).as_long()
            round_matches.append({"home": team_names[h], "away": team_names[a]})
        schedule.append(round_matches)
    
    print("SCHEDULE:")
    for r in range(N_ROUNDS):
        print(f"  Round {r+1}:")
        for match in schedule[r]:
            print(f"    {match['home']} vs {match['away']}")
    
    # Print location tracking
    print()
    print("LOCATION TRACKING:")
    for t in range(N_TEAMS):
        locs = []
        for r in range(N_ROUNDS):
            l = model.evaluate(loc[t][r]).as_long()
            locs.append(team_names[l])
        ph = ["H" if model.evaluate(play_home[t][r]) else "A" for r in range(N_ROUNDS)]
        print(f"  Team {team_names[t]}: games={ph}, locations={locs}")
    
    # Verify constraints
    print()
    print("VERIFICATION:")
    
    for r in range(N_ROUNDS):
        teams_in_round = []
        for m in range(N_MATCHES_PER_ROUND):
            h = model.evaluate(home[r][m]).as_long()
            a = model.evaluate(away[r][m]).as_long()
            teams_in_round.extend([h, a])
        assert len(set(teams_in_round)) == 6, f"Round {r+1} has duplicate teams"
    print("  Each team plays once per round: OK")
    
    pair_count = {}
    for r in range(N_ROUNDS):
        for m in range(N_MATCHES_PER_ROUND):
            h = model.evaluate(home[r][m]).as_long()
            a = model.evaluate(away[r][m]).as_long()
            pair_count[(h, a)] = pair_count.get((h, a), 0) + 1
    for t1 in range(N_TEAMS):
        for t2 in range(N_TEAMS):
            if t1 != t2:
                assert pair_count.get((t1,t2), 0) == 1, f"Pair ({t1},{t2}) count={pair_count.get((t1,t2),0)}"
    print("  Double round-robin: OK")
    
    for t in range(N_TEAMS):
        consec_home = 0
        consec_away = 0
        for r in range(N_ROUNDS):
            if model.evaluate(play_home[t][r]):
                consec_home += 1
                consec_away = 0
            elif model.evaluate(play_away[t][r]):
                consec_away += 1
                consec_home = 0
            assert consec_home <= 3, f"Team {t} has {consec_home} consecutive home at round {r}"
            assert consec_away <= 3, f"Team {t} has {consec_away} consecutive away at round {r}"
    print("  Consecutive game limit: OK")
    
    for m in range(N_MATCHES_PER_ROUND):
        h = model.evaluate(home[0][m]).as_long()
        a = model.evaluate(away[0][m]).as_long()
        assert not (h == 0 and a == 1) and not (h == 1 and a == 0), "A vs B in round 1"
        assert not (h == 2 and a == 3) and not (h == 3 and a == 2), "C vs D in round 1"
    print("  Rivalry constraints: OK")
    
    for t in range(N_TEAMS):
        found = False
        for r in range(N_ROUNDS - 1):
            if model.evaluate(play_home[t][r]) and model.evaluate(play_home[t][r+1]):
                found = True
                break
        assert found, f"Team {t} has no consecutive home games"
    print("  Mandatory break: OK")
    
    for t in range(N_TEAMS):
        for r in range(N_ROUNDS):
            if r + 1 < N_ROUNDS:
                if model.evaluate(play_away[t][r]):
                    loc_before = model.evaluate(loc[t][r-1]).as_long() if r > 0 else t
                    opp = model.evaluate(opponent[t][r]).as_long()
                    travel_dist = dist.get((loc_before, opp), 0)
                    if travel_dist > 140:
                        assert model.evaluate(play_home[t][r+1]), \
                            f"Team {t} travels {travel_dist} in round {r+1} but doesn't play home in round {r+2}"
    print("  Travel fatigue: OK")
    
    print()
    print("All constraints verified!")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")