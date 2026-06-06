from z3 import *

# Users data
users = ['user1','user2','user3','user4','user5','user6','user7','user8']
costs = [100,50,80,150,60,90,120,40]
# Influence weights not needed for reach count

# Edges: (src, dst, strength)
edges = [
    (0,1,0.6), # user1->user2
    (0,2,0.7), # user1->user3
    (1,2,0.4), # user2->user3
    (1,4,0.5), # user2->user5
    (2,3,0.3), # user3->user4
    (3,4,0.8), # user4->user5
    (3,5,0.6), # user4->user6
    (4,6,0.5), # user5->user7
    (5,6,0.7), # user6->user7
    (6,7,0.4), # user7->user8
]

n = len(users)
seed = [Bool(f'seed_{i}') for i in range(n)]
# Directly influenced
direct = [Bool(f'direct_{i}') for i in range(n)]
# Secondary influenced
secondary = [Bool(f'secondary_{i}') for i in range(n)]

opt = Optimize()

# Budget constraint
budget = Sum([If(seed[i], costs[i], 0) for i in range(n)])
opt.add(budget <= 300)
# Max seeds constraint
opt.add(Sum([If(seed[i], 1, 0) for i in range(n)]) <= 2)

# Direct influence definition
for i in range(n):
    # collect seeds that have edge to i with strength >=0.3
    relevant = []
    for (src,dst,strg) in edges:
        if dst == i and strg >= 0.3:
            relevant.append(seed[src])
    if relevant:
        opt.add(direct[i] == Or(relevant))
    else:
        opt.add(direct[i] == False)

# Secondary influence definition
for i in range(n):
    # collect directly influenced nodes that have edge to i with strength >=0.2
    relevant = []
    for (src,dst,strg) in edges:
        if dst == i and strg >= 0.2:
            relevant.append(direct[src])
    if relevant:
        opt.add(secondary[i] == And(Not(seed[i]), Not(direct[i]), Or(relevant)))
    else:
        opt.add(secondary[i] == False)

# Total reach (distinct users)
reach_expr = Sum([If(Or(seed[i], direct[i], secondary[i]), 1, 0) for i in range(n)])
opt.maximize(reach_expr)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Extract selections
    selected = [i for i in range(n) if m.eval(seed[i])]
    direct_inf = [i for i in range(n) if m.eval(direct[i])]
    secondary_inf = [i for i in range(n) if m.eval(secondary[i])]
    total_reach = sum(1 for i in range(n) if m.eval(Or(seed[i], direct[i], secondary[i])))
    total_budget_used = sum(costs[i] for i in selected)
    coverage_ratio = total_reach / n
    efficiency_score = total_reach / total_budget_used if total_budget_used != 0 else 0
    # cascade depth: 0 if only seeds, 1 if any direct, 2 if any secondary
    cascade_depth = 0
    if secondary_inf:
        cascade_depth = 2
    elif direct_inf:
        cascade_depth = 1
    else:
        cascade_depth = 0
    # Print results
    print("STATUS: sat")
    print("selected_seeds:")
    for i in selected:
        print(f"  - user_id: {users[i]}, cost: {costs[i]}, expected_reach: TBD")
    print("cascade_analysis:")
    print(f"  total_budget_used: {total_budget_used}")
    print("  direct_influence: ", [users[i] for i in direct_inf])
    print("  secondary_influence: ", [users[i] for i in secondary_inf])
    print(f"  total_reach: {total_reach}")
    print(f"  influence_probability: 1.0")
    print("network_metrics:")
    print(f"  coverage_ratio: {coverage_ratio}")
    print(f"  efficiency_score: {efficiency_score}")
    print(f"  cascade_depth: {cascade_depth}")
else:
    print("STATUS: unsat")