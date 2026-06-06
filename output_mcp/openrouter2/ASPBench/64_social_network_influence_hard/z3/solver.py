from z3 import *

# Data
ids = ['u1','u2','u3','u4','u5','u6','u7','u8','u9','u10','u11','u12','u13','u14','u15','u16','u17','u18','u19','u20','u21','u22','u23','u24','u25']
# Map category to int: influencer=0, regular=1, expert=2
cat_map = {'influencer':0,'regular':1,'expert':2}
categories = [cat_map['influencer'],cat_map['regular'],cat_map['regular'],cat_map['expert'],cat_map['regular'],cat_map['influencer'],cat_map['influencer'],cat_map['regular'],cat_map['regular'],cat_map['expert'],cat_map['regular'],cat_map['regular'],cat_map['influencer'],cat_map['regular'],cat_map['expert'],cat_map['regular'],cat_map['regular'],cat_map['expert'],cat_map['influencer'],cat_map['regular'],cat_map['expert'],cat_map['regular'],cat_map['regular'],cat_map['expert'],cat_map['influencer']]
costs = [250,80,70,150,90,200,300,110,60,220,50,130,280,85,180,95,40,190,210,75,100,120,140,160,240]
thresholds = [10,60,90,100,70,120,10,40,80,150,50,90,10,60,10,50,100,110,130,70,80,10,120,90,10]

# Build incoming edges list
incoming = [[] for _ in ids]
# connections list
connections = [
    ('u1','u2',70),('u1','u5',50),('u7','u8',50),('u7','u9',30),('u15','u16',60),('u22','u5',30),('u2','u3',40),('u8','u3',50),('u8','u9',60)
]
# map id to index
id_to_idx = {uid:i for i,uid in enumerate(ids)}
for fr,to,st in connections:
    incoming[id_to_idx[to]].append((id_to_idx[fr], st))

# Solver
opt = Optimize()

n = len(ids)
seed = [Bool(f'seed_{i}') for i in range(n)]
activated = [Bool(f'activated_{i}') for i in range(n)]

# Seed implies activated
for i in range(n):
    opt.add(Implies(seed[i], activated[i]))

# Activated implies seed or threshold satisfied
for i in range(n):
    # sum of strengths from activated neighbors
    sum_strength = Sum([If(activated[v], IntVal(st), IntVal(0)) for v,st in incoming[i]])
    opt.add(Implies(activated[i], Or(seed[i], sum_strength >= IntVal(thresholds[i]))))

# Budget constraints
total_cost = Sum([If(seed[i], IntVal(costs[i]), IntVal(0)) for i in range(n)])
opt.add(total_cost <= IntVal(1000))
# Influencer budget
influencer_cost = Sum([If(And(seed[i], categories[i]==0), IntVal(costs[i]), IntVal(0)) for i in range(n)])
opt.add(influencer_cost <= IntVal(600))
# Max seeds
num_seeds = Sum([If(seed[i], IntVal(1), IntVal(0)) for i in range(n)])
opt.add(num_seeds <= IntVal(5))
# Required expert seed
expert_seed = Sum([If(And(seed[i], categories[i]==2), IntVal(1), IntVal(0)) for i in range(n)])
opt.add(expert_seed >= IntVal(1))

# Objective: maximize score
key_index = id_to_idx['u4']
activated_count = Sum([If(activated[i], IntVal(1), IntVal(0)) for i in range(n)])
score_expr = 10 * activated_count + 50 * If(activated[key_index], IntVal(1), IntVal(0))
opt.maximize(score_expr)

# Check
res = opt.check()
if res == sat:
    m = opt.model()
    selected_seeds = [ids[i] for i in range(n) if is_true(m.evaluate(seed[i], model_completion=True))]
    activated_users = [ids[i] for i in range(n) if is_true(m.evaluate(activated[i], model_completion=True))]
    total_cost_val = sum(costs[i] for i in range(n) if is_true(m.evaluate(seed[i], model_completion=True)))
    total_activated_count_val = sum(1 for i in range(n) if is_true(m.evaluate(activated[i], model_completion=True)))
    key_user_activated_val = is_true(m.evaluate(activated[key_index], model_completion=True))
    final_score_val = 10 * total_activated_count_val + (50 if key_user_activated_val else 0)
    print("STATUS: sat")
    print("selected_seeds =", selected_seeds)
    print("activated_users =", activated_users)
    print("total_cost =", total_cost_val)
    print("total_activated_count =", total_activated_count_val)
    print("key_user_activated =", key_user_activated_val)
    print("final_score =", final_score_val)
else:
    print("STATUS: unsat")
    if res == unknown:
        print("STATUS: unknown")