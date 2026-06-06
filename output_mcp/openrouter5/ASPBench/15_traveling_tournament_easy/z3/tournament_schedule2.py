from z3 import *
import math

# Teams and their indices
teams = ["A", "B", "C", "D"]
T = 4  # number of teams
R = 6  # number of rounds

# Distance matrix
dist = {
    ("A","B"): 5, ("A","C"): 6, ("A","D"): 8.2,
    ("B","A"): 5, ("B","C"): 5, ("B","D"): 5.7,
    ("C","A"): 6, ("C","B"): 5, ("C","D"): 10,
    ("D","A"): 8.2, ("D","B"): 5.7, ("D","C"): 10
}

# Alternative encoding: For each round r and each unordered pair (t1,t2),
# we decide if they play, and who is home.
# match_exists[r][t1][t2] = True if t1 and t2 play in round r (t1 < t2)
# home_team[r][t1][t2] = True if t1 is home, False if t2 is home (only valid when match_exists)

match_exists = [[[Bool(f"match_r{r}_{t1}_{t2}") for t2 in range(T)] for t1 in range(T)] for r in range(R)]
home_team = [[[Bool(f"home_r{r}_{t1}_{t2}") for t2 in range(T)] for t1 in range(T)] for r in range(R)]

opt = Optimize()

# Symmetry: only define for t1 < t2
for r in range(R):
    for t1 in range(T):
        for t2 in range(T):
            if t1 >= t2:
                continue
            # If match exists, exactly one of home_team[t1][t2] or not(home_team[t1][t2])
            # home_team[t1][t2] = True means t1 is home, False means t2 is home
            pass

# Constraint 2 & 3: Each round has exactly 2 matches, each team plays exactly once
for r in range(R):
    # Exactly 2 matches per round
    opt.add(Sum([If(match_exists[r][t1][t2], 1, 0) for t1 in range(T) for t2 in range(T) if t1 < t2]) == 2)
    
    # Each team plays exactly once per round
    for t in range(T):
        matches_with_t = []
        for t2 in range(T):
            if t < t2:
                matches_with_t.append(match_exists[r][t][t2])
            elif t2 < t:
                matches_with_t.append(match_exists[r][t2][t])
        opt.add(Sum([If(m, 1, 0) for m in matches_with_t]) == 1)

# Constraint 1: Each ordered pair plays exactly once (home team hosts away team once)
for h in range(T):
    for a in range(T):
        if h == a:
            continue
        t1, t2 = (h, a) if h < a else (a, h)
        # Count rounds where h and a play AND h is home
        count = Sum([If(And(match_exists[r][t1][t2], 
                           If(h < a, home_team[r][t1][t2], Not(home_team[r][t1][t2]))), 1, 0) 
                     for r in range(R)])
        opt.add(count == 1)

# Constraint 4 & 5: No team plays more than 2 consecutive home/away games
# For each team t, we need to know if they're home in each round
is_home = [[Bool(f"is_home_r{r}_t{t}") for t in range(T)] for r in range(R)]

for r in range(R):
    for t in range(T):
        # Team t is home in round r iff there exists a match where t is home
        conditions = []
        for t2 in range(T):
            if t < t2:
                conditions.append(And(match_exists[r][t][t2], home_team[r][t][t2]))
            elif t2 < t:
                conditions.append(And(match_exists[r][t2][t], Not(home_team[r][t2][t])))
        opt.add(is_home[r][t] == Or(conditions))

# Consecutive limit
for t in range(T):
    for r in range(R - 2):
        opt.add(Not(And(is_home[r][t], is_home[r+1][t], is_home[r+2][t])))
        opt.add(Not(And(Not(is_home[r][t]), Not(is_home[r+1][t]), Not(is_home[r+2][t]))))

# Objective: Minimize total travel distance
distance_terms = []
for r in range(R):
    for t in range(T):
        # If team t is away in round r, they travel to opponent's city
        # Opponent is the other team in the match involving t
        for t2 in range(T):
            if t == t2:
                continue
            t1, t2_sorted = (t, t2) if t < t2 else (t2, t)
            # Team t is away vs t2 if they play and t2 is home
            is_away_vs_t2 = And(match_exists[r][t1][t2_sorted], 
                               If(t < t2_sorted, Not(home_team[r][t1][t2_sorted]), home_team[r][t1][t2_sorted]))
            d_val = dist[(teams[t], teams[t2])]
            distance_terms.append(If(is_away_vs_t2, RealVal(d_val), RealVal(0)))

total_distance = Real('total_distance')
opt.add(total_distance == Sum(distance_terms))
opt.minimize(total_distance)

result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Total distance = {m.eval(total_distance)}")
    
    print("\nSchedule:")
    for r in range(R):
        matches = []
        for t1 in range(T):
            for t2 in range(T):
                if t1 < t2:
                    if m.eval(match_exists[r][t1][t2]):
                        if m.eval(home_team[r][t1][t2]):
                            matches.append(f"{teams[t1]} hosts {teams[t2]}")
                        else:
                            matches.append(f"{teams[t2]} hosts {teams[t1]}")
        print(f"Round {r+1}: {matches[0]}, {matches[1]}")
    
    # Verify
    print("\nVerification:")
    for h in range(T):
        for a in range(T):
            if h == a: continue
            cnt = 0
            for r in range(R):
                t1, t2 = (h, a) if h < a else (a, h)
                if m.eval(match_exists[r][t1][t2]):
                    if h < a:
                        if m.eval(home_team[r][t1][t2]):
                            cnt += 1
                    else:
                        if not m.eval(home_team[r][t1][t2]):
                            cnt += 1
            print(f"  {teams[h]} hosts {teams[a]}: {cnt} time(s)")
    
    for t in range(T):
        venues_str = ""
        for r in range(R):
            venues_str += "H" if m.eval(is_home[r][t]) else "A"
        print(f"  Team {teams[t]} venues: {venues_str}")
    
    total_dist_manual = 0
    for r in range(R):
        for t in range(T):
            for t2 in range(T):
                if t == t2: continue
                t1, t2_s = (t, t2) if t < t2 else (t2, t)
                if m.eval(match_exists[r][t1][t2_s]):
                    is_away = False
                    if t < t2_s:
                        is_away = not m.eval(home_team[r][t1][t2_s])
                    else:
                        is_away = m.eval(home_team[r][t1][t2_s])
                    if is_away:
                        total_dist_manual += dist[(teams[t], teams[t2])]
    print(f"  Manual total distance: {total_dist_manual}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found")
else:
    print("STATUS: unknown")