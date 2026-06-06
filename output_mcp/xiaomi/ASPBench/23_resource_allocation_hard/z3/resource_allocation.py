from z3 import *

# Create optimizer
opt = Optimize()

# Task data
num_tasks = 12
categories = [0,0,0,0, 1,1,1,1, 2,2,2,2]  # 0=Research, 1=Development, 2=Deployment
values = [40, 60, 70, 55, 80, 90, 75, 85, 65, 80, 70, 95]
compute = [20, 30, 25, 20, 40, 35, 30, 45, 15, 20, 25, 30]
bandwidth = [10, 25, 20, 15, 30, 25, 40, 35, 20, 30, 25, 35]
storage = [30, 20, 15, 25, 20, 30, 25, 15, 40, 35, 30, 45]
specialists = [5, 10, 5, 10, 20, 15, 18, 22, 8, 12, 10, 15]

# Resource capacities
cap_compute = 150
cap_bandwidth = 120
cap_storage = 140
cap_specialists = 60

# Decision variables: whether each task is selected (0 or 1)
sel = [Bool(f'sel_{i}') for i in range(num_tasks)]

# Helper: sum of resource usage for selected tasks
def resource_sum(res_list):
    return Sum([If(sel[i], res_list[i], 0) for i in range(num_tasks)])

# 1. Resource limits
opt.add(resource_sum(compute) <= cap_compute)
opt.add(resource_sum(bandwidth) <= cap_bandwidth)
opt.add(resource_sum(storage) <= cap_storage)

# 5. Conditional Specialist Cost:
# If at least one Development task (4-7) is selected, each selected Deployment task (8-11) incurs +5 specialists
any_dev = Or([sel[i] for i in range(4, 8)])
# Count selected deployment tasks
num_deploy_selected = Sum([If(sel[i], 1, 0) for i in range(8, 12)])
# Additional specialist cost = 5 * num_deploy_selected if any_dev else 0
additional_specialists = If(any_dev, 5 * num_deploy_selected, 0)
# Total specialists = base + additional
opt.add(resource_sum(specialists) + additional_specialists <= cap_specialists)

# 3. Prerequisite: Task 4 requires Task 0
opt.add(Implies(sel[4], sel[0]))

# 4. Mutual Exclusion: Task 1 and Task 7 cannot both be selected
opt.add(Not(And(sel[1], sel[7])))

# 6. Diversity Bonus: at least one from each category
has_research = Or([sel[i] for i in range(0, 4)])
has_development = Or([sel[i] for i in range(4, 8)])
has_deployment = Or([sel[i] for i in range(8, 12)])
bonus_achieved = And(has_research, has_development, has_deployment)

# Objective: maximize total value = sum of selected task values + 100 if bonus achieved
base_value = Sum([If(sel[i], values[i], 0) for i in range(num_tasks)])
total_value = base_value + If(bonus_achieved, 100, 0)

opt.maximize(total_value)

# Solve
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    selected = [i for i in range(num_tasks) if is_true(m[sel[i]])]
    base_val = sum(values[i] for i in selected)
    bonus = all([
        any(i in selected for i in range(0, 4)),
        any(i in selected for i in range(4, 8)),
        any(i in selected for i in range(8, 12))
    ])
    total_val = base_val + (100 if bonus else 0)
    
    # Compute resource usage
    comp_used = sum(compute[i] for i in selected)
    bw_used = sum(bandwidth[i] for i in selected)
    stor_used = sum(storage[i] for i in selected)
    spec_base = sum(specialists[i] for i in selected)
    any_dev_sel = any(i in selected for i in range(4, 8))
    deploy_count = sum(1 for i in selected if i in range(8, 12))
    spec_extra = 5 * deploy_count if any_dev_sel else 0
    spec_total = spec_base + spec_extra
    
    print("STATUS: sat")
    print(f"selected_tasks: {sorted(selected)}")
    print(f"total_value: {total_val}")
    print(f"bonus_achieved: {bonus}")
    print(f"resource_usage:")
    print(f"  compute: {comp_used}")
    print(f"  bandwidth: {bw_used}")
    print(f"  storage: {stor_used}")
    print(f"  specialists: {spec_total}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")