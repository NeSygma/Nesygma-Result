from z3 import *

# Problem data
users = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8']
n = len(users)

# Influence weights and costs
influence_weight = {
    'user1': 0.8, 'user2': 0.3, 'user3': 0.5, 'user4': 0.9,
    'user5': 0.4, 'user6': 0.6, 'user7': 0.7, 'user8': 0.2
}
cost = {
    'user1': 100, 'user2': 50, 'user3': 80, 'user4': 150,
    'user5': 60, 'user6': 90, 'user7': 120, 'user8': 40
}

# Directed edges with strength
edges = [
    ('user1', 'user2', 0.6),
    ('user1', 'user3', 0.7),
    ('user2', 'user3', 0.4),
    ('user2', 'user5', 0.5),
    ('user3', 'user4', 0.3),
    ('user4', 'user5', 0.8),
    ('user4', 'user6', 0.6),
    ('user5', 'user7', 0.5),
    ('user6', 'user7', 0.7),
    ('user7', 'user8', 0.4)
]

# Create adjacency lookup: for each target, list of (source, strength)
incoming = {u: [] for u in users}
for src, tgt, strength in edges:
    incoming[tgt].append((src, strength))

# Z3 solver with optimization
opt = Optimize()

# Decision variables: is user selected as seed?
seed = {u: Bool(f'seed_{u}') for u in users}

# Influence status variables
direct_influenced = {u: Bool(f'direct_{u}') for u in users}
secondary_influenced = {u: Bool(f'secondary_{u}') for u in users}

# Constraint 1: Budget limit
opt.add(Sum([If(seed[u], cost[u], 0) for u in users]) <= 300)

# Constraint 2: Max 2 seeds
opt.add(Sum([If(seed[u], 1, 0) for u in users]) <= 2)

# Constraint 3: Direct influence - user is directly influenced if connected FROM a seed with strength >= 0.3
for u in users:
    # A user is directly influenced if ANY incoming edge from a seed has strength >= 0.3
    direct_conditions = []
    for src, strength in incoming[u]:
        if strength >= 0.3:
            direct_conditions.append(seed[src])
    
    if direct_conditions:
        # User is directly influenced if at least one condition holds AND user is not a seed
        opt.add(Implies(And(Or(direct_conditions), Not(seed[u])), direct_influenced[u]))
        opt.add(Implies(Not(Or(direct_conditions)), Not(direct_influenced[u])))
        opt.add(Implies(seed[u], Not(direct_influenced[u])))
    else:
        opt.add(Not(direct_influenced[u]))

# Constraint 4: Secondary influence - user is secondary influenced if connected FROM a directly influenced user with strength >= 0.2
# But not already a seed or directly influenced
for u in users:
    secondary_conditions = []
    for src, strength in incoming[u]:
        if strength >= 0.2:
            secondary_conditions.append(direct_influenced[src])
    
    if secondary_conditions:
        # User is secondary influenced if at least one condition holds AND user is not seed or directly influenced
        opt.add(Implies(And(Or(secondary_conditions), Not(seed[u]), Not(direct_influenced[u])), secondary_influenced[u]))
        opt.add(Implies(Not(Or(secondary_conditions)), Not(secondary_influenced[u])))
        opt.add(Implies(Or(seed[u], direct_influenced[u]), Not(secondary_influenced[u])))
    else:
        opt.add(Not(secondary_influenced[u]))

# Objective: Maximize total reach (seeds + direct + secondary)
total_reach = Sum([If(Or(seed[u], direct_influenced[u], secondary_influenced[u]), 1, 0) for u in users])
opt.maximize(total_reach)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    selected_seeds = []
    for u in users:
        if m.evaluate(seed[u], model_completion=True):
            selected_seeds.append(u)
    
    direct_list = []
    for u in users:
        if m.evaluate(direct_influenced[u], model_completion=True):
            direct_list.append(u)
    
    secondary_list = []
    for u in users:
        if m.evaluate(secondary_influenced[u], model_completion=True):
            secondary_list.append(u)
    
    total_budget_used = sum(cost[u] for u in selected_seeds)
    total_reach_val = len(selected_seeds) + len(direct_list) + len(secondary_list)
    coverage_ratio = total_reach_val / n
    efficiency_score = total_reach_val / total_budget_used if total_budget_used > 0 else 0
    
    # Calculate cascade depth
    # Seeds are depth 0, direct influenced are depth 1, secondary influenced are depth 2
    # But we need to check if there's any path that goes deeper
    # For this problem, max depth is 2 (seeds -> direct -> secondary)
    cascade_depth = 0
    if selected_seeds:
        cascade_depth = 1
        if direct_list:
            cascade_depth = 2
            if secondary_list:
                cascade_depth = 3
    
    print("\n=== Selected Seeds ===")
    for u in selected_seeds:
        # Calculate expected reach from this seed
        # This is complex - for now, just report the seed
        print(f"  {u}: cost={cost[u]}, influence_weight={influence_weight[u]}")
    
    print(f"\n=== Cascade Analysis ===")
    print(f"total_budget_used: {total_budget_used}")
    print(f"direct_influence: {direct_list}")
    print(f"secondary_influence: {secondary_list}")
    print(f"total_reach: {total_reach_val}")
    print(f"influence_probability: 1.0 (deterministic model)")
    
    print(f"\n=== Network Metrics ===")
    print(f"coverage_ratio: {coverage_ratio:.3f}")
    print(f"efficiency_score: {efficiency_score:.6f}")
    print(f"cascade_depth: {cascade_depth}")
    
    print(f"\n=== Solution Summary ===")
    print(f"Selected seeds: {selected_seeds}")
    print(f"Total reach: {total_reach_val} out of {n} users")
    print(f"Budget used: {total_budget_used} out of 300")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")