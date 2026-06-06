from z3 import *

# Problem parameters
users = [
    {"id": "user1", "influence_weight": 0.8, "cost": 100, "category": "influencer"},
    {"id": "user2", "influence_weight": 0.3, "cost": 50, "category": "regular"},
    {"id": "user3", "influence_weight": 0.5, "cost": 80, "category": "regular"},
    {"id": "user4", "influence_weight": 0.9, "cost": 150, "category": "influencer"},
    {"id": "user5", "influence_weight": 0.4, "cost": 60, "category": "regular"},
    {"id": "user6", "influence_weight": 0.6, "cost": 90, "category": "regular"},
    {"id": "user7", "influence_weight": 0.7, "cost": 120, "category": "influencer"},
    {"id": "user8", "influence_weight": 0.2, "cost": 40, "category": "regular"},
]

# Edges: (from_user_id, to_user_id, strength)
edges = [
    ("user1", "user2", 0.6),
    ("user1", "user3", 0.7),
    ("user2", "user3", 0.4),
    ("user2", "user5", 0.5),
    ("user3", "user4", 0.3),
    ("user4", "user5", 0.8),
    ("user4", "user6", 0.6),
    ("user5", "user7", 0.5),
    ("user6", "user7", 0.7),
    ("user7", "user8", 0.4),
]

# Budget and max seeds
BUDGET = 300
MAX_SEEDS = 2

# Initialize solver
solver = Optimize()

# Declare symbolic variables for each user
is_seed = [Bool(f"is_seed_{user['id']}") for user in users]
is_direct = [Bool(f"is_direct_{user['id']}") for user in users]
is_secondary = [Bool(f"is_secondary_{user['id']}") for user in users]

# Cost of each user
costs = [user["cost"] for user in users]

# Add constraints for max seeds and budget
solver.add(Sum([If(is_seed[i], 1, 0) for i in range(len(users))]) <= MAX_SEEDS)
solver.add(Sum([If(is_seed[i], costs[i], 0) for i in range(len(users))]) <= BUDGET)

# Direct influence: if a seed has an edge to a user with strength >= 0.3, mark as directly influenced
for i, user in enumerate(users):
    for edge in edges:
        from_user, to_user, strength = edge
        if to_user == user["id"]:
            # Find index of from_user
            from_idx = next((idx for idx, u in enumerate(users) if u["id"] == from_user), None)
            if from_idx is not None:
                solver.add(Implies(And(is_seed[from_idx], strength >= 0.3), is_direct[i]))

# Secondary influence: if a directly influenced user has an edge to another user with strength >= 0.2, and the target is not a seed or directly influenced, mark as secondary influenced
for i, user in enumerate(users):
    for edge in edges:
        from_user, to_user, strength = edge
        if to_user == user["id"]:
            from_idx = next((idx for idx, u in enumerate(users) if u["id"] == from_user), None)
            if from_idx is not None:
                # Target user must not be a seed or directly influenced
                not_already_influenced = And(Not(is_seed[i]), Not(is_direct[i]))
                solver.add(Implies(
                    And(is_direct[from_idx], strength >= 0.2, not_already_influenced),
                    is_secondary[i]
                ))

# Ensure a user is not marked as secondary if already a seed or directly influenced
for i in range(len(users)):
    solver.add(Implies(is_seed[i], Not(is_secondary[i])))
    solver.add(Implies(is_direct[i], Not(is_secondary[i])))

# Total reach: sum of seeds, direct, and secondary influenced users
total_reach = Sum([
    If(is_seed[i], 1, 0) + 
    If(is_direct[i], 1, 0) + 
    If(is_secondary[i], 1, 0) 
    for i in range(len(users))
])

# Maximize total reach
solver.maximize(total_reach)

# Check for satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract selected seeds
    selected_seeds = []
    for i, user in enumerate(users):
        if is_true(model[is_seed[i]]):
            selected_seeds.append({
                "user_id": user["id"],
                "cost": user["cost"],
                "expected_reach": user["influence_weight"]
            })
    
    # Extract direct and secondary influence
    direct_influence = []
    secondary_influence = []
    for i, user in enumerate(users):
        if is_true(model[is_direct[i]]):
            direct_influence.append(user["id"])
        if is_true(model[is_secondary[i]]):
            secondary_influence.append(user["id"])
    
    # Total budget used
    total_budget_used = sum(user["cost"] for user in selected_seeds)
    
    # Total reach
    total_reach_val = model.eval(total_reach).as_long()
    
    # Coverage ratio
    coverage_ratio = total_reach_val / len(users)
    
    # Efficiency score
    efficiency_score = total_reach_val / total_budget_used if total_budget_used > 0 else 0
    
    # Cascade depth
    cascade_depth = 1  # At least 1 (seeds)
    if any(is_true(model[is_direct[i]]) for i in range(len(users))):
        cascade_depth = 2
    if any(is_true(model[is_secondary[i]]) for i in range(len(users))):
        cascade_depth = 3
    
    # Print results
    print("STATUS: sat")
    print("selected_seeds:", selected_seeds)
    print("cascade_analysis:")
    print(f"  total_budget_used: {total_budget_used}")
    print(f"  direct_influence: {direct_influence}")
    print(f"  secondary_influence: {secondary_influence}")
    print(f"  total_reach: {total_reach_val}")
    print(f"  influence_probability: 1.0")
    print("network_metrics:")
    print(f"  coverage_ratio: {coverage_ratio}")
    print(f"  efficiency_score: {efficiency_score}")
    print(f"  cascade_depth: {cascade_depth}")
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE is ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")