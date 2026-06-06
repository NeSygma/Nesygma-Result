from z3 import *

# Data
users = [
    {"id": "u1", "cost": 250, "category": "influencer", "threshold": 10},
    {"id": "u2", "cost": 80, "category": "regular", "threshold": 60},
    {"id": "u3", "cost": 70, "category": "regular", "threshold": 90},
    {"id": "u4", "cost": 150, "category": "expert", "threshold": 100},
    {"id": "u5", "cost": 90, "category": "regular", "threshold": 70},
    {"id": "u6", "cost": 200, "category": "influencer", "threshold": 120},
    {"id": "u7", "cost": 300, "category": "influencer", "threshold": 10},
    {"id": "u8", "cost": 110, "category": "regular", "threshold": 40},
    {"id": "u9", "cost": 60, "category": "regular", "threshold": 80},
    {"id": "u10", "cost": 220, "category": "expert", "threshold": 150},
    {"id": "u11", "cost": 50, "category": "regular", "threshold": 50},
    {"id": "u12", "cost": 130, "category": "regular", "threshold": 90},
    {"id": "u13", "cost": 280, "category": "influencer", "threshold": 10},
    {"id": "u14", "cost": 85, "category": "regular", "threshold": 60},
    {"id": "u15", "cost": 180, "category": "expert", "threshold": 10},
    {"id": "u16", "cost": 95, "category": "regular", "threshold": 50},
    {"id": "u17", "cost": 40, "category": "regular", "threshold": 100},
    {"id": "u18", "cost": 190, "category": "expert", "threshold": 110},
    {"id": "u19", "cost": 210, "category": "influencer", "threshold": 130},
    {"id": "u20", "cost": 75, "category": "regular", "threshold": 70},
    {"id": "u21", "cost": 100, "category": "expert", "threshold": 80},
    {"id": "u22", "cost": 120, "category": "regular", "threshold": 10},
    {"id": "u23", "cost": 140, "category": "regular", "threshold": 120},
    {"id": "u24", "cost": 160, "category": "expert", "threshold": 90},
    {"id": "u25", "cost": 240, "category": "influencer", "threshold": 10},
]

connections = [
    {"from": "u1", "to": "u2", "strength": 70},
    {"from": "u1", "to": "u5", "strength": 50},
    {"from": "u7", "to": "u8", "strength": 50},
    {"from": "u7", "to": "u9", "strength": 30},
    {"from": "u15", "to": "u16", "strength": 60},
    {"from": "u22", "to": "u5", "strength": 30},
    {"from": "u2", "to": "u3", "strength": 40},
    {"from": "u8", "to": "u3", "strength": 50},
    {"from": "u8", "to": "u9", "strength": 60},
]

budget_total = 1000
budget_influencer = 600
max_seeds = 5
required_seed_category = "expert"
key_user_id = "u4"

# Mapping id -> index
id_to_idx = {u["id"]: i for i, u in enumerate(users)}
N = len(users)

# Declare Bool variables for seed selection and activation
seed = [Bool(f"seed_{i}") for i in range(N)]
activated = [Bool(f"act_{i}") for i in range(N)]

# Helper lists
costs = [u["cost"] for u in users]
thresholds = [u["threshold"] for u in users]
categories = [u["category"] for u in users]

# Build incoming influence list per target
incoming = [[] for _ in range(N)]
for conn in connections:
    src = id_to_idx[conn["from"]]
    tgt = id_to_idx[conn["to"]]
    strength = conn["strength"]
    incoming[tgt].append((src, strength))

opt = Optimize()

# Seed implies activation
for i in range(N):
    opt.add(Implies(seed[i], activated[i]))

# Activation condition (equivalence)
for i in range(N):
    # sum of strengths from activated neighbors
    sum_expr = Sum([If(activated[src], strength, 0) for (src, strength) in incoming[i]])
    activation_cond = Or(seed[i], sum_expr >= thresholds[i])
    opt.add(activated[i] == activation_cond)

# Budget constraints
total_cost_expr = Sum([If(seed[i], costs[i], 0) for i in range(N)])
opt.add(total_cost_expr <= budget_total)

# Influencer budget constraint
influencer_cost_expr = Sum([If(And(seed[i], categories[i] == "influencer"), costs[i], 0) for i in range(N)])
opt.add(influencer_cost_expr <= budget_influencer)

# Max seeds
opt.add(Sum([If(seed[i], 1, 0) for i in range(N)]) <= max_seeds)

# Required at least one expert seed
expert_seed_expr = Sum([If(And(seed[i], categories[i] == "expert"), 1, 0) for i in range(N)])
opt.add(expert_seed_expr >= 1)

# Key user activation boolean
key_idx = id_to_idx[key_user_id]
key_user_activated = activated[key_idx]

# Objective components
total_activated = Sum([If(activated[i], 1, 0) for i in range(N)])
final_score = 10 * total_activated + If(key_user_activated, 50, 0)
opt.maximize(final_score)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    selected = [users[i]["id"] for i in range(N) if m.eval(seed[i])]
    act = [users[i]["id"] for i in range(N) if m.eval(activated[i])]
    total_cost = sum(users[i]["cost"] for i in range(N) if m.eval(seed[i]))
    total_activated_cnt = sum(1 for i in range(N) if m.eval(activated[i]))
    key_activated = bool(m.eval(key_user_activated))
    score = 10 * total_activated_cnt + (50 if key_activated else 0)
    print("STATUS: sat")
    print("selected_seeds =", selected)
    print("activated_users =", act)
    print("total_cost =", total_cost)
    print("total_activated_count =", total_activated_cnt)
    print("key_user_activated =", key_activated)
    print("final_score =", score)
else:
    print("STATUS: unsat")