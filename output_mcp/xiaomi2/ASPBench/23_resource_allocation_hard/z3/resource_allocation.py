from z3 import *

# Create optimizer
opt = Optimize()

# Task data: (ID, Category, Value, Compute, Bandwidth, Storage, Specialists)
tasks = [
    (0,  "Research",     40, 20, 10, 30,  5),
    (1,  "Research",     60, 30, 25, 20, 10),
    (2,  "Research",     70, 25, 20, 15,  5),
    (3,  "Research",     55, 20, 15, 25, 10),
    (4,  "Development",  80, 40, 30, 20, 20),
    (5,  "Development",  90, 35, 25, 30, 15),
    (6,  "Development",  75, 30, 40, 25, 18),
    (7,  "Development",  85, 45, 35, 15, 22),
    (8,  "Deployment",   65, 15, 20, 40,  8),
    (9,  "Deployment",   80, 20, 30, 35, 12),
    (10, "Deployment",   70, 25, 25, 30, 10),
    (11, "Deployment",   95, 30, 35, 45, 15),
]

# Resource capacities
CAP_COMPUTE = 150
CAP_BANDWIDTH = 120
CAP_STORAGE = 140
CAP_SPECIALISTS = 60

# Category indices
research_ids = [0, 1, 2, 3]
dev_ids = [4, 5, 6, 7]
deploy_ids = [8, 9, 10, 11]

# Decision variables: 0-1 selection for each task
sel = [Bool(f'sel_{i}') for i in range(12)]

# --- Constraints ---

# 1. Prerequisite: Task 4 requires Task 0
opt.add(Implies(sel[4], sel[0]))

# 2. Mutual Exclusion: Task 1 and Task 7 cannot both be selected
opt.add(Not(And(sel[1], sel[7])))

# 3. Resource limits (base costs)
# Compute
opt.add(Sum([If(sel[i], tasks[i][3], 0) for i in range(12)]) <= CAP_COMPUTE)
# Bandwidth
opt.add(Sum([If(sel[i], tasks[i][4], 0) for i in range(12)]) <= CAP_BANDWIDTH)
# Storage
opt.add(Sum([If(sel[i], tasks[i][5], 0) for i in range(12)]) <= CAP_STORAGE)

# 4. Conditional Specialist Cost:
# If at least one Development task is selected, each selected Deployment task
# incurs an additional 5 Specialist units.
has_dev = Or([sel[i] for i in dev_ids])

# For each deployment task, the extra specialist cost is 5 if (has_dev AND task selected)
# Total specialist cost = base + conditional
base_specialists = Sum([If(sel[i], tasks[i][6], 0) for i in range(12)])
extra_specialists = Sum([If(And(has_dev, sel[i]), 5, 0) for i in deploy_ids])
total_specialists = base_specialists + extra_specialists

opt.add(total_specialists <= CAP_SPECIALISTS)

# 5. Diversity Bonus
has_research = Or([sel[i] for i in research_ids])
has_deployment = Or([sel[i] for i in deploy_ids])
bonus_achieved = And(has_research, has_dev, has_deployment)

# Objective: maximize total value
base_value = Sum([If(sel[i], tasks[i][2], 0) for i in range(12)])
total_value = If(bonus_achieved, base_value + 100, base_value)

opt.maximize(total_value)

# Solve
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    
    selected = [i for i in range(12) if is_true(m.eval(sel[i]))]
    selected.sort()
    
    bv = sum(tasks[i][2] for i in selected)
    bonus = (len(set(selected) & set(research_ids)) > 0 and
             len(set(selected) & set(dev_ids)) > 0 and
             len(set(selected) & set(deploy_ids)) > 0)
    tv = bv + (100 if bonus else 0)
    
    comp_used = sum(tasks[i][3] for i in selected)
    bw_used = sum(tasks[i][4] for i in selected)
    stor_used = sum(tasks[i][5] for i in selected)
    
    base_spec = sum(tasks[i][6] for i in selected)
    has_dev_sel = any(i in dev_ids for i in selected)
    extra_spec = sum(5 for i in selected if i in deploy_ids) if has_dev_sel else 0
    spec_used = base_spec + extra_spec
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected}")
    print(f"total_value: {tv}")
    print(f"bonus_achieved: {bonus}")
    print(f"resource_usage:")
    print(f"  compute: {comp_used}")
    print(f"  bandwidth: {bw_used}")
    print(f"  storage: {stor_used}")
    print(f"  specialists: {spec_used}")
    
    # Verify
    assert comp_used <= CAP_COMPUTE, f"Compute exceeded: {comp_used}"
    assert bw_used <= CAP_BANDWIDTH, f"Bandwidth exceeded: {bw_used}"
    assert stor_used <= CAP_STORAGE, f"Storage exceeded: {stor_used}"
    assert spec_used <= CAP_SPECIALISTS, f"Specialists exceeded: {spec_used}"
    assert 4 not in selected or 0 in selected, "Prerequisite violated"
    assert not (1 in selected and 7 in selected), "Mutual exclusion violated"
    print("All constraints verified.")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")