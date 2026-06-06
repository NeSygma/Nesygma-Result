from z3 import *

# Users data
users = [
    {"id": 1, "weight": 0.8, "cost": 100, "category": "influencer"},
    {"id": 2, "weight": 0.3, "cost": 50, "category": "regular"},
    {"id": 3, "weight": 0.5, "cost": 80, "category": "regular"},
    {"id": 4, "weight": 0.9, "cost": 150, "category": "influencer"},
    {"id": 5, "weight": 0.4, "cost": 60, "category": "regular"},
    {"id": 6, "weight": 0.6, "cost": 90, "category": "regular"},
    {"id": 7, "weight": 0.7, "cost": 120, "category": "influencer"},
    {"id": 8, "weight": 0.2, "cost": 40, "category": "regular"},
]

N = len(users)  # 8

# Connections: (from, to, strength)
edges = [
    (1, 2, 0.6),
    (1, 3, 0.7),
    (2, 3, 0.4),
    (2, 5, 0.5),
    (3, 4, 0.3),
    (4, 5, 0.8),
    (4, 6, 0.6),
    (5, 7, 0.5),
    (6, 7, 0.7),
    (7, 8, 0.4),
]

# Decision variables: seed[i] = 1 if user i is selected as seed
seed = [Int(f"seed_{i}") for i in range(1, N+1)]

# Directly influenced: direct[i] = 1 if user i is directly influenced by a seed
direct = [Int(f"direct_{i}") for i in range(1, N+1)]

# Secondary influenced: secondary[i] = 1 if user i is secondary influenced
secondary = [Int(f"secondary_{i}") for i in range(1, N+1)]

opt = Optimize()

# Domain: all variables are 0 or 1
for i in range(N):
    opt.add(Or(seed[i] == 0, seed[i] == 1))
    opt.add(Or(direct[i] == 0, direct[i] == 1))
    opt.add(Or(secondary[i] == 0, secondary[i] == 1))

# Constraint 1: Budget limit - total cost of selected seeds <= 300
total_cost = Sum([seed[i] * users[i]["cost"] for i in range(N)])
opt.add(total_cost <= 300)

# Constraint 2: At most 2 seeds
opt.add(Sum(seed) <= 2)

# Constraint 3: Direct influence - a user is directly influenced if connected from a seed with strength >= 0.3
for j in range(1, N+1):
    incoming = []
    for (f, t, s) in edges:
        if t == j and s >= 0.3:
            incoming.append(f)
    if incoming:
        opt.add(direct[j-1] == If(Or([seed[f-1] == 1 for f in incoming]), 1, 0))
    else:
        opt.add(direct[j-1] == 0)

# Constraint 4: Secondary influence - a user is secondary influenced if connected from a directly influenced user with strength >= 0.2
for j in range(1, N+1):
    incoming_secondary = []
    for (f, t, s) in edges:
        if t == j and s >= 0.2:
            incoming_secondary.append(f)
    if incoming_secondary:
        opt.add(secondary[j-1] == If(And(Or([direct[f-1] == 1 for f in incoming_secondary]),
                                            seed[j-1] == 0,
                                            direct[j-1] == 0), 1, 0))
    else:
        opt.add(secondary[j-1] == 0)

# Constraint: A seed cannot also be directly influenced or secondary influenced
for i in range(N):
    opt.add(Implies(seed[i] == 1, And(direct[i] == 0, secondary[i] == 0)))
    opt.add(Implies(direct[i] == 1, secondary[i] == 0))

# Objective: Maximize total reach = seeds + direct + secondary
total_reach = Sum([seed[i] + direct[i] + secondary[i] for i in range(N)])
opt.maximize(total_reach)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    selected_seeds = []
    total_budget_used = 0
    for i in range(N):
        if m.eval(seed[i]) == 1:
            selected_seeds.append(users[i]["id"])
            total_budget_used += users[i]["cost"]
    
    direct_influenced = []
    for i in range(N):
        if m.eval(direct[i]) == 1:
            direct_influenced.append(users[i]["id"])
    
    secondary_influenced = []
    for i in range(N):
        if m.eval(secondary[i]) == 1:
            secondary_influenced.append(users[i]["id"])
    
    total_reach_val = len(selected_seeds) + len(direct_influenced) + len(secondary_influenced)
    
    print(f"selected_seeds = {selected_seeds}")
    print(f"total_budget_used = {total_budget_used}")
    print(f"direct_influence = {direct_influenced}")
    print(f"secondary_influence = {secondary_influenced}")
    print(f"total_reach = {total_reach_val}")
    
    coverage_ratio = total_reach_val / N
    efficiency_score = total_reach_val / total_budget_used if total_budget_used > 0 else 0
    
    # Determine cascade depth
    if len(secondary_influenced) > 0:
        cascade_depth = 3
    elif len(direct_influenced) > 0:
        cascade_depth = 2
    else:
        cascade_depth = 1
    
    print(f"coverage_ratio = {coverage_ratio}")
    print(f"efficiency_score = {efficiency_score}")
    print(f"cascade_depth = {cascade_depth}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")