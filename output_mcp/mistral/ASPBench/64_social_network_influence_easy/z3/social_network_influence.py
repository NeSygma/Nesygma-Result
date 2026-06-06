from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# User data
users = [
    ("user1", 0.8, 100, "influencer"),
    ("user2", 0.3, 50, "regular"),
    ("user3", 0.5, 80, "regular"),
    ("user4", 0.9, 150, "influencer"),
    ("user5", 0.4, 60, "regular"),
    ("user6", 0.6, 90, "regular"),
    ("user7", 0.7, 120, "influencer"),
    ("user8", 0.2, 40, "regular")
]

# Connection data (directed edges with strength)
connections = [
    ("user1", "user2", 0.6),
    ("user1", "user3", 0.7),
    ("user2", "user3", 0.4),
    ("user2", "user5", 0.5),
    ("user3", "user4", 0.3),
    ("user4", "user5", 0.8),
    ("user4", "user6", 0.6),
    ("user5", "user7", 0.5),
    ("user6", "user7", 0.7),
    ("user7", "user8", 0.4)
]

# Budget and max seeds
BUDGET = 300
MAX_SEEDS = 2

# Create solver with optimization
opt = Optimize()

# Declare symbolic variables
seed = [Bool(f"seed_{user[0]}") for user in users]
direct_influence = [Bool(f"direct_{user[0]}") for user in users]
secondary_influence = [Bool(f"secondary_{user[0]}") for user in users]

# Helper: Get user index by name
def get_user_index(name):
    for i, user in enumerate(users):
        if user[0] == name:
            return i
    return -1

# Helper: Get cost of a user
def get_user_cost(name):
    for user in users:
        if user[0] == name:
            return user[2]
    return 0

# Constraint: Budget limit
budget_expr = Sum([If(seed[i], get_user_cost(users[i][0]), 0) for i in range(len(users))])
opt.add(budget_expr <= BUDGET)

# Constraint: Max seeds
opt.add(Sum([If(seed[i], 1, 0) for i in range(len(users))]) <= MAX_SEEDS)

# Constraint: Direct influence
for conn in connections:
    from_user, to_user, strength = conn
    from_idx = get_user_index(from_user)
    to_idx = get_user_index(to_user)
    # If the from_user is a seed and the connection strength >= 0.3, then to_user is directly influenced
    opt.add(Implies(And(seed[from_idx], strength >= 0.3), direct_influence[to_idx]))

# Constraint: Secondary influence
# For each user, if they are directly influenced and have a connection to another user with strength >= 0.2,
# and that other user is not a seed and not directly influenced, then they are secondary influenced.
for conn in connections:
    from_user, to_user, strength = conn
    from_idx = get_user_index(from_user)
    to_idx = get_user_index(to_user)
    # If from_user is directly influenced, strength >= 0.2, and to_user is not a seed and not directly influenced, then to_user is secondary influenced
    opt.add(Implies(
        And(direct_influence[from_idx], strength >= 0.2, Not(seed[to_idx]), Not(direct_influence[to_idx])),
        secondary_influence[to_idx]
    ))

# Ensure no overlap: a user cannot be both directly and secondary influenced
for i in range(len(users)):
    opt.add(Not(And(direct_influence[i], secondary_influence[i])))

# Ensure no overlap: a user cannot be a seed and directly/secondary influenced
for i in range(len(users)):
    opt.add(Not(And(seed[i], direct_influence[i])))
    opt.add(Not(And(seed[i], secondary_influence[i])))

# Objective: Maximize total reach (seeds + directly influenced + secondary influenced)
total_reach = Sum([If(seed[i], 1, 0) for i in range(len(users))]) + \
              Sum([If(direct_influence[i], 1, 0) for i in range(len(users))]) + \
              Sum([If(secondary_influence[i], 1, 0) for i in range(len(users))])

opt.maximize(total_reach)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract selected seeds
    selected_seeds = []
    for i in range(len(users)):
        if is_true(model[seed[i]]):
            selected_seeds.append(users[i][0])
    
    # Extract directly influenced users
    direct_influenced = []
    for i in range(len(users)):
        if is_true(model[direct_influence[i]]):
            direct_influenced.append(users[i][0])
    
    # Extract secondary influenced users
    secondary_influenced = []
    for i in range(len(users)):
        if is_true(model[secondary_influence[i]]):
            secondary_influenced.append(users[i][0])
    
    # Calculate total budget used
    total_budget_used = sum(get_user_cost(user) for user in selected_seeds)
    
    # Calculate total reach
    total_reach_value = len(selected_seeds) + len(direct_influenced) + len(secondary_influenced)
    
    # Calculate coverage ratio
    coverage_ratio = total_reach_value / len(users)
    
    # Calculate efficiency score
    if total_budget_used > 0:
        efficiency_score = total_reach_value / total_budget_used
    else:
        efficiency_score = 0.0
    
    # Cascade depth: maximum depth of influence cascade (1-3)
    # For simplicity, assume depth 2 if secondary influence exists, else 1
    cascade_depth = 2 if len(secondary_influenced) > 0 else 1
    
    # Print results
    print(f"selected_seeds: {selected_seeds}")
    print(f"cascade_analysis:")
    print(f"  total_budget_used: {total_budget_used}")
    print(f"  direct_influence: {direct_influenced}")
    print(f"  secondary_influence: {secondary_influenced}")
    print(f"  total_reach: {total_reach_value}")
    print(f"  influence_probability: 1.0")
    print(f"network_metrics:")
    print(f"  coverage_ratio: {coverage_ratio}")
    print(f"  efficiency_score: {efficiency_score}")
    print(f"  cascade_depth: {cascade_depth}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")