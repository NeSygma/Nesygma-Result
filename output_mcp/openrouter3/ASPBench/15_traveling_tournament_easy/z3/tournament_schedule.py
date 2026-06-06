from z3 import *

# Teams and distances
teams = ['A', 'B', 'C', 'D']
team_index = {t: i for i, t in enumerate(teams)}

# Distance matrix (as given)
distances = {
    ('A', 'B'): 5, ('A', 'C'): 6, ('A', 'D'): 8.2,
    ('B', 'A'): 5, ('B', 'C'): 5, ('B', 'D'): 5.7,
    ('C', 'A'): 6, ('C', 'B'): 5, ('C', 'D'): 10,
    ('D', 'A'): 8.2, ('D', 'B'): 5.7, ('D', 'C'): 10
}

# Number of rounds and matches per round
NUM_ROUNDS = 6
MATCHES_PER_ROUND = 2

# Create solver with optimization
opt = Optimize()

# Decision variables: match[round][home][away] = 1 if home hosts away in that round
# We'll use a 3D array of Booleans
match = {}
for r in range(NUM_ROUNDS):
    for h in teams:
        for a in teams:
            if h != a:
                match[(r, h, a)] = Bool(f'match_{r}_{h}_{a}')

# Constraint 1: Each pair plays exactly twice (once home, once away)
for h in teams:
    for a in teams:
        if h != a:
            # Count how many times h hosts a
            host_count = Sum([If(match[(r, h, a)], 1, 0) for r in range(NUM_ROUNDS)])
            # Count how many times a hosts h
            away_count = Sum([If(match[(r, a, h)], 1, 0) for r in range(NUM_ROUNDS)])
            # Total should be 2 (one home, one away for each pair)
            opt.add(host_count + away_count == 2)
            # Specifically, each team hosts each other exactly once
            opt.add(host_count == 1)

# Constraint 2: Each round has exactly 2 matches
for r in range(NUM_ROUNDS):
    round_matches = Sum([If(match[(r, h, a)], 1, 0) for h in teams for a in teams if h != a])
    opt.add(round_matches == MATCHES_PER_ROUND)

# Constraint 3: Each team plays exactly once per round
for r in range(NUM_ROUNDS):
    for t in teams:
        # Team plays if they are home or away in any match in this round
        plays = Or([match[(r, t, a)] for a in teams if a != t] + 
                   [match[(r, h, t)] for h in teams if h != t])
        opt.add(plays == True)  # Must play exactly once

# Constraint 4 & 5: Consecutive limits (≤2 consecutive home/away games)
# We need to track consecutive home/away games for each team
for t in teams:
    for r in range(NUM_ROUNDS - 2):  # Check windows of 3 consecutive rounds
        # Check if team plays 3 consecutive home games
        home_3 = And(
            match[(r, t, teams[0])] if teams[0] != t else False,
            match[(r+1, t, teams[0])] if teams[0] != t else False,
            match[(r+2, t, teams[0])] if teams[0] != t else False
        )
        # Actually, we need to check all possible opponents
        home_3_any = Or([
            And(
                match[(r, t, a1)],
                match[(r+1, t, a2)],
                match[(r+2, t, a3)]
            )
            for a1 in teams if a1 != t
            for a2 in teams if a2 != t
            for a3 in teams if a3 != t
        ])
        opt.add(Not(home_3_any))
        
        # Similarly for away games
        away_3_any = Or([
            And(
                match[(r, h1, t)],
                match[(r+1, h2, t)],
                match[(r+2, h3, t)]
            )
            for h1 in teams if h1 != t
            for h2 in teams if h2 != t
            for h3 in teams if h3 != t
        ])
        opt.add(Not(away_3_any))

# Objective: Minimize total travel distance
# For each match, the away team travels to the home team's location
total_distance = Real('total_distance')
distance_expr = Sum([
    If(match[(r, h, a)], distances[(h, a)], 0)
    for r in range(NUM_ROUNDS)
    for h in teams
    for a in teams
    if h != a
])
opt.add(total_distance == distance_expr)
opt.minimize(total_distance)

# Check and print results
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for r in range(NUM_ROUNDS):
        round_matches = []
        for h in teams:
            for a in teams:
                if h != a:
                    if is_true(m[match[(r, h, a)]]):
                        round_matches.append({"home": h, "away": a})
        schedule.append(round_matches)
    
    # Print schedule
    print("Schedule:")
    for r, matches in enumerate(schedule):
        print(f"Round {r+1}: {matches}")
    
    # Calculate total distance
    total_dist = 0
    for r in range(NUM_ROUNDS):
        for h in teams:
            for a in teams:
                if h != a and is_true(m[match[(r, h, a)]]):
                    total_dist += distances[(h, a)]
    
    print(f"Total distance: {total_dist}")
    print(f"Expected optimal: 75")
    
    # Verify constraints
    print("\nConstraint verification:")
    
    # 1. Double round-robin
    print("1. Double round-robin:")
    for h in teams:
        for a in teams:
            if h != a:
                host_count = sum(1 for r in range(NUM_ROUNDS) if is_true(m[match[(r, h, a)]]))
                away_count = sum(1 for r in range(NUM_ROUNDS) if is_true(m[match[(r, a, h)]]))
                print(f"  {h} vs {a}: {host_count} home, {away_count} away")
    
    # 2. Round structure
    print("2. Round structure:")
    for r in range(NUM_ROUNDS):
        count = sum(1 for h in teams for a in teams if h != a and is_true(m[match[(r, h, a)]]))
        print(f"  Round {r+1}: {count} matches")
    
    # 3. Team availability
    print("3. Team availability per round:")
    for r in range(NUM_ROUNDS):
        for t in teams:
            plays = any(is_true(m[match[(r, t, a)]]) for a in teams if a != t) or \
                    any(is_true(m[match[(r, h, t)]]) for h in teams if h != t)
            print(f"  Round {r+1}, {t}: {'plays' if plays else 'does not play'}")
    
    # 4 & 5. Consecutive limits
    print("4 & 5. Consecutive limits:")
    for t in teams:
        home_streak = 0
        away_streak = 0
        max_home_streak = 0
        max_away_streak = 0
        for r in range(NUM_ROUNDS):
            is_home = any(is_true(m[match[(r, t, a)]]) for a in teams if a != t)
            is_away = any(is_true(m[match[(r, h, t)]]) for h in teams if h != t)
            
            if is_home:
                home_streak += 1
                away_streak = 0
                max_home_streak = max(max_home_streak, home_streak)
            elif is_away:
                away_streak += 1
                home_streak = 0
                max_away_streak = max(max_away_streak, away_streak)
            else:
                home_streak = 0
                away_streak = 0
        
        print(f"  {t}: max home streak = {max_home_streak}, max away streak = {max_away_streak}")
    
    # Check if total distance matches expected
    if abs(total_dist - 75) < 0.1:
        print(f"\nSUCCESS: Total distance {total_dist} matches expected optimal 75")
    else:
        print(f"\nNOTE: Total distance {total_dist} differs from expected 75")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found")
else:
    print("STATUS: unknown")