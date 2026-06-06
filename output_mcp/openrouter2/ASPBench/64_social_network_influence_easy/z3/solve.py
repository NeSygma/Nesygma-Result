from z3 import *

# Define users
user_names = ['user1','user2','user3','user4','user5','user6','user7','user8']
costs = [100,50,80,150,60,90,120,40]
# edges: (src, dst, strength)
edges = [
    (0,1,0.6),
    (0,2,0.7),
    (1,2,0.4),
    (1,4,0.5),
    (2,3,0.3),
    (3,4,0.8),
    (3,5,0.6),
    (4,6,0.5),
    (5,6,0.7),
    (6,7,0.4)
]

n = len(user_names)
# Bool vars for seed, direct, secondary
is_seed = [Bool(f'seed_{i}') for i in range(n)]
is_direct = [Bool(f'direct_{i}') for i in range(n)]
is_secondary = [Bool(f'sec_{i}') for i in range(n)]

opt = Optimize()

# Max 2 seeds
opt.add(Sum([If(is_seed[i],1,0) for i in range(n)]) <= 2)
# Budget <= 300
opt.add(Sum([If(is_seed[i],costs[i],0) for i in range(n)]) <= 300)

# Precompute adjacency lists for direct and secondary thresholds
# Direct threshold >=0.3
direct_sources = [[] for _ in range(n)]
# Secondary threshold >=0.2
sec_sources = [[] for _ in range(n)]
for (src,dst,strength) in edges:
    if strength >= 0.3:
        direct_sources[dst].append(src)
    if strength >= 0.2:
        sec_sources[dst].append(src)

# Define direct influence constraints
for j in range(n):
    if direct_sources[j]:
        opt.add(is_direct[j] == Or([is_seed[i] for i in direct_sources[j]]))
    else:
        opt.add(is_direct[j] == False)

# Define secondary influence constraints
for j in range(n):
    if sec_sources[j]:
        sec_candidate = Or([is_direct[v] for v in sec_sources[j]])
        opt.add(is_secondary[j] == And(sec_candidate, Not(is_seed[j]), Not(is_direct[j])))
    else:
        opt.add(is_secondary[j] == False)

# Ensure seeds are not direct or secondary
for i in range(n):
    opt.add(Implies(is_seed[i], Not(is_direct[i])))
    opt.add(Implies(is_seed[i], Not(is_secondary[i])))
    opt.add(Implies(is_direct[i], Not(is_secondary[i])))

# Total reach
reach_expr = Sum([If(is_seed[i],1,0) + If(is_direct[i],1,0) + If(is_secondary[i],1,0) for i in range(n)])
opt.maximize(reach_expr)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract lists
    selected_seeds = []
    for i in range(n):
        if is_true(m.eval(is_seed[i])):
            selected_seeds.append(i)
    direct_influenced = [i for i in range(n) if is_true(m.eval(is_direct[i]))]
    secondary_influenced = [i for i in range(n) if is_true(m.eval(is_secondary[i]))]
    total_budget_used = sum(costs[i] for i in selected_seeds)
    total_reach = sum(1 for i in range(n) if is_true(m.eval(is_seed[i])) or is_true(m.eval(is_direct[i])) or is_true(m.eval(is_secondary[i])))
    coverage_ratio = total_reach / n
    efficiency_score = total_reach / total_budget_used if total_budget_used>0 else 0
    cascade_depth = 2 if secondary_influenced else (1 if direct_influenced else 0)
    # Print results
    print("STATUS: sat")
    print("selected_seeds:")
    for i in selected_seeds:
        print(f"- user_id: {user_names[i]}, cost: {costs[i]}, expected_reach: 0")
    print("cascade_analysis:")
    print(f"total_budget_used: {total_budget_used}")
    print("direct_influence: ", ", ".join(user_names[i] for i in direct_influenced))
    print("secondary_influence: ", ", ".join(user_names[i] for i in secondary_influenced))
    print(f"total_reach: {total_reach}")
    print("influence_probability: 1.0")
    print("network_metrics:")
    print(f"coverage_ratio: {coverage_ratio}")
    print(f"efficiency_score: {efficiency_score}")
    print(f"cascade_depth: {cascade_depth}")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")