from z3 import *

# Problem data
users_data = [
    {"id": "u1", "cost": 250, "category": "influencer", "activation_threshold": 10},
    {"id": "u2", "cost": 80, "category": "regular", "activation_threshold": 60},
    {"id": "u3", "cost": 70, "category": "regular", "activation_threshold": 90},
    {"id": "u4", "cost": 150, "category": "expert", "activation_threshold": 100},
    {"id": "u5", "cost": 90, "category": "regular", "activation_threshold": 70},
    {"id": "u6", "cost": 200, "category": "influencer", "activation_threshold": 120},
    {"id": "u7", "cost": 300, "category": "influencer", "activation_threshold": 10},
    {"id": "u8", "cost": 110, "category": "regular", "activation_threshold": 40},
    {"id": "u9", "cost": 60, "category": "regular", "activation_threshold": 80},
    {"id": "u10", "cost": 220, "category": "expert", "activation_threshold": 150},
    {"id": "u11", "cost": 50, "category": "regular", "activation_threshold": 50},
    {"id": "u12", "cost": 130, "category": "regular", "activation_threshold": 90},
    {"id": "u13", "cost": 280, "category": "influencer", "activation_threshold": 10},
    {"id": "u14", "cost": 85, "category": "regular", "activation_threshold": 60},
    {"id": "u15", "cost": 180, "category": "expert", "activation_threshold": 10},
    {"id": "u16", "cost": 95, "category": "regular", "activation_threshold": 50},
    {"id": "u17", "cost": 40, "category": "regular", "activation_threshold": 100},
    {"id": "u18", "cost": 190, "category": "expert", "activation_threshold": 110},
    {"id": "u19", "cost": 210, "category": "influencer", "activation_threshold": 130},
    {"id": "u20", "cost": 75, "category": "regular", "activation_threshold": 70},
    {"id": "u21", "cost": 100, "category": "expert", "activation_threshold": 80},
    {"id": "u22", "cost": 120, "category": "regular", "activation_threshold": 10},
    {"id": "u23", "cost": 140, "category": "regular", "activation_threshold": 120},
    {"id": "u24", "cost": 160, "category": "expert", "activation_threshold": 90},
    {"id": "u25", "cost": 240, "category": "influencer", "activation_threshold": 10}
]

connections_data = [
    {"from": "u1", "to": "u2", "strength": 70},
    {"from": "u1", "to": "u5", "strength": 50},
    {"from": "u7", "to": "u8", "strength": 50},
    {"from": "u7", "to": "u9", "strength": 30},
    {"from": "u15", "to": "u16", "strength": 60},
    {"from": "u22", "to": "u5", "strength": 30},
    {"from": "u2", "to": "u3", "strength": 40},
    {"from": "u8", "to": "u3", "strength": 50},
    {"from": "u8", "to": "u9", "strength": 60}
]

budget_data = {"total": 1000, "influencer": 600}
max_seeds = 5
required_seed_category = "expert"
key_user_id = "u4"

# Create solver
solver = Solver()

# Map user IDs to indices
user_ids = [u["id"] for u in users_data]
user_index = {uid: i for i, uid in enumerate(user_ids)}
n_users = len(user_ids)

# Create symbolic variables for seeds
seed = [Bool(f"seed_{i}") for i in range(n_users)]

# Create symbolic variables for activation status at each time step
# We'll use 5 time steps for the cascade to propagate
T = 5
activated = [[Bool(f"activated_{i}_{t}") for t in range(T+1)] for i in range(n_users)]

# Build incoming connections for each user
incoming = [[] for _ in range(n_users)]
for conn in connections_data:
    from_idx = user_index[conn["from"]]
    to_idx = user_index[conn["to"]]
    incoming[to_idx].append((from_idx, conn["strength"]))

# Add constraints

# 1. Seed selection constraints
# At most 5 seeds
solver.add(Sum(seed) <= max_seeds)

# Total cost constraint
total_cost = Sum([If(seed[i], users_data[i]["cost"], 0) for i in range(n_users)])
solver.add(total_cost <= budget_data["total"])

# Influencer cost constraint - use Z3 And instead of Python and
influencer_cost = Sum([If(And(seed[i], users_data[i]["category"] == "influencer"), 
                         users_data[i]["cost"], 0) for i in range(n_users)])
solver.add(influencer_cost <= budget_data["influencer"])

# At least one expert seed
expert_seeds = Sum([If(And(seed[i], users_data[i]["category"] == "expert"), 1, 0) for i in range(n_users)])
solver.add(expert_seeds >= 1)

# 2. Cascade activation constraints
# Initial state: seeds are activated at time 0
for i in range(n_users):
    solver.add(activated[i][0] == seed[i])

# Propagation rules for each time step
for t in range(T):
    for i in range(n_users):
        # Calculate incoming influence from neighbors at time t
        incoming_influence = Sum([If(activated[neighbor_idx][t], strength, 0) 
                                 for neighbor_idx, strength in incoming[i]])
        
        # Activation condition: either already activated or meets threshold
        activation_condition = Or(
            activated[i][t],  # Already activated
            incoming_influence >= users_data[i]["activation_threshold"]
        )
        
        # Next state: if activation condition is met, user is activated
        solver.add(activated[i][t+1] == activation_condition)

# 3. Final activation status (after T steps)
final_activated = [activated[i][T] for i in range(n_users)]

# 4. Objective: maximize composite score
# 10 points per activated user
total_activated = Sum([If(final_activated[i], 1, 0) for i in range(n_users)])
# 50 points if key user (u4) is activated
key_user_idx = user_index[key_user_id]
key_user_activated = final_activated[key_user_idx]
score = 10 * total_activated + If(key_user_activated, 50, 0)

# Use Optimize to maximize score
opt = Optimize()
opt.add(solver.assertions())
opt.maximize(score)

# Check and extract solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract selected seeds
    selected_seeds = [user_ids[i] for i in range(n_users) if is_true(model.eval(seed[i]))]
    
    # Extract activated users
    activated_users = [user_ids[i] for i in range(n_users) if is_true(model.eval(final_activated[i]))]
    
    # Calculate total cost
    total_cost_val = sum(users_data[i]["cost"] for i in range(n_users) if is_true(model.eval(seed[i])))
    
    # Calculate total activated count
    total_activated_count = len(activated_users)
    
    # Check if key user is activated
    key_user_activated_val = is_true(model.eval(key_user_activated))
    
    # Calculate final score
    final_score_val = 10 * total_activated_count + (50 if key_user_activated_val else 0)
    
    print("STATUS: sat")
    print(f"selected_seeds: {selected_seeds}")
    print(f"activated_users: {activated_users}")
    print(f"total_cost: {total_cost_val}")
    print(f"total_activated_count: {total_activated_count}")
    print(f"key_user_activated: {key_user_activated_val}")
    print(f"final_score: {final_score_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")