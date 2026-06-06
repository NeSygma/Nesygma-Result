from z3 import *
import math

# Teams and their indices
teams = ["A", "B", "C", "D"]
T = 4  # number of teams
R = 6  # number of rounds

# Distance matrix (rounded to 1 decimal for Z3 Real)
# Using exact values: AB=5, AC=6, AD=8.2, BC=5, BD=5.7, CD=10
dist = {
    ("A","B"): 5, ("A","C"): 6, ("A","D"): 8.2,
    ("B","A"): 5, ("B","C"): 5, ("B","D"): 5.7,
    ("C","A"): 6, ("C","B"): 5, ("C","D"): 10,
    ("D","A"): 8.2, ("D","B"): 5.7, ("D","C"): 10
}

# Decision variables:
# For each round r (0..5) and each team t (0..3), we need to know:
# - opponent[r][t] = which team team t plays in round r (0..3, -1 = no match)
# - venue[r][t] = 1 if team t is home in round r, 0 if away

# We'll use integer variables for opponent and boolean for venue
opponent = [[Int(f"opp_r{r}_t{t}") for t in range(T)] for r in range(R)]
venue = [[Bool(f"venue_r{r}_t{t}") for t in range(T)] for r in range(R)]

opt = Optimize()

# Domain constraints
for r in range(R):
    for t in range(T):
        opt.add(opponent[r][t] >= 0, opponent[r][t] < T)
        opt.add(opponent[r][t] != t)  # can't play yourself

# Constraint 1: Each pair plays exactly twice (once home, once away)
# For each ordered pair (h, a) with h != a, count how many rounds h hosts a
for h in range(T):
    for a in range(T):
        if h == a:
            continue
        # Count rounds where team h hosts team a
        count_home = Sum([If(And(venue[r][h], opponent[r][h] == a), 1, 0) for r in range(R)])
        opt.add(count_home == 1)

# Constraint 2 & 3: Each round has exactly 2 matches, each team plays exactly once per round
for r in range(R):
    # Each team plays exactly once per round (opponent is valid)
    for t in range(T):
        opt.add(opponent[r][t] >= 0)  # already constrained above
    
    # Symmetry: if team t1 plays team t2 in round r, then t2 plays t1
    for t1 in range(T):
        for t2 in range(T):
            if t1 < t2:
                # t1 plays t2 iff t2 plays t1
                opt.add(opponent[r][t1] == t2)
                opt.add(opponent[r][t2] == t1)
    
    # Exactly 2 matches per round: for each round, exactly 2 teams are home
    # (since each match has one home team, 2 matches = 2 home teams)
    opt.add(Sum([If(venue[r][t], 1, 0) for t in range(T)]) == 2)
    
    # Venue consistency: if team t1 hosts t2, then t1 is home and t2 is away
    for t1 in range(T):
        for t2 in range(T):
            if t1 != t2:
                # If t1 plays t2 in round r, then venue[r][t1] = True and venue[r][t2] = False
                opt.add(Implies(opponent[r][t1] == t2, And(venue[r][t1], Not(venue[r][t2]))))

# Constraint 4 & 5: No team plays more than 2 consecutive home/away games
for t in range(T):
    for r in range(R - 2):
        # Not all three consecutive rounds are home
        opt.add(Not(And(venue[r][t], venue[r+1][t], venue[r+2][t])))
        # Not all three consecutive rounds are away
        opt.add(Not(And(Not(venue[r][t]), Not(venue[r+1][t]), Not(venue[r+2][t]))))

# Objective: Minimize total travel distance
# For each round r and each team t, if team t is away (venue[r][t] == False),
# they travel from home to opponent's city. Distance = dist[teams[t]][teams[opponent[r][t]]]
# Since they return home after each round, each away game costs one trip.

total_distance = Real('total_distance')
distance_terms = []
for r in range(R):
    for t in range(T):
        # If team t is away in round r, add distance to opponent's city
        # opponent[r][t] is the opponent index
        # We need to map opponent index to team name for distance lookup
        # Use If-Then-Else chain
        d = Real(f"d_r{r}_t{t}")
        # Distance depends on opponent
        dist_expr = 0
        for opp_idx in range(T):
            if opp_idx != t:
                d_val = dist[(teams[t], teams[opp_idx])]
                dist_expr = If(opponent[r][t] == opp_idx, RealVal(d_val), dist_expr)
        
        # If away, add this distance; if home, add 0
        term = If(Not(venue[r][t]), dist_expr, RealVal(0))
        distance_terms.append(term)

opt.add(total_distance == Sum(distance_terms))
opt.minimize(total_distance)

# Try to find optimal solution
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Total distance = {m.eval(total_distance)}")
    
    # Print schedule
    print("\nSchedule:")
    for r in range(R):
        matches = []
        for t in range(T):
            if m.eval(venue[r][t]):
                opp_idx = m.eval(opponent[r][t]).as_long()
                matches.append(f"{teams[t]} vs {teams[opp_idx]} (home: {teams[t]})")
        print(f"Round {r+1}: {matches[0]}, {matches[1]}")
    
    # Verify constraints
    print("\nVerification:")
    # Check each pair plays twice
    for h in range(T):
        for a in range(T):
            if h == a: continue
            cnt = 0
            for r in range(R):
                if m.eval(venue[r][h]) and m.eval(opponent[r][h]).as_long() == a:
                    cnt += 1
            print(f"  {teams[h]} hosts {teams[a]}: {cnt} time(s)")
    
    # Check consecutive home/away
    for t in range(T):
        venues_str = ""
        for r in range(R):
            venues_str += "H" if m.eval(venue[r][t]) else "A"
        print(f"  Team {teams[t]} venues: {venues_str}")
    
    # Calculate total distance manually
    total_dist_manual = 0
    for r in range(R):
        for t in range(T):
            if not m.eval(venue[r][t]):
                opp_idx = m.eval(opponent[r][t]).as_long()
                total_dist_manual += dist[(teams[t], teams[opp_idx])]
    print(f"  Manual total distance: {total_dist_manual}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found")
else:
    print("STATUS: unknown")