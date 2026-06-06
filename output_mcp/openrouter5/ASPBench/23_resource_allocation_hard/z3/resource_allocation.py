from z3 import *

# Task data
tasks = list(range(12))
categories = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]  # 0=Research, 1=Development, 2=Deployment
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

# Decision variables: x[i] = 1 if task i is selected, 0 otherwise
x = [Bool(f'x_{i}') for i in range(12)]

opt = Optimize()

# Resource constraints (base costs)
opt.add(Sum([If(x[i], compute[i], 0) for i in range(12)]) <= cap_compute)
opt.add(Sum([If(x[i], bandwidth[i], 0) for i in range(12)]) <= cap_bandwidth)
opt.add(Sum([If(x[i], storage[i], 0) for i in range(12)]) <= cap_storage)

# Specialist cost: base + conditional
# Conditional: if at least one Development task (4-7) selected, each selected Deployment task (8-11) adds 5 specialists
dev_selected = Or([x[i] for i in range(4, 8)])
# Total specialists = sum of base specialists + conditional extra
# conditional extra = If(dev_selected, 5 * (number of selected deployment tasks), 0)
num_deploy_selected = Sum([If(x[i], 1, 0) for i in range(8, 12)])
extra_specialists = If(dev_selected, 5 * num_deploy_selected, 0)
total_specialists = Sum([If(x[i], specialists[i], 0) for i in range(12)]) + extra_specialists
opt.add(total_specialists <= cap_specialists)

# Prerequisite: Task 4 requires Task 0
opt.add(Implies(x[4], x[0]))

# Mutual exclusion: Task 1 and Task 7 cannot both be selected
opt.add(Not(And(x[1], x[7])))

# Diversity bonus: if at least one from each category, add 100
research_selected = Or([x[i] for i in range(0, 4)])
development_selected = Or([x[i] for i in range(4, 8)])
deployment_selected = Or([x[i] for i in range(8, 12)])
diversity_bonus = If(And(research_selected, development_selected, deployment_selected), 100, 0)

# Total value
total_value = Sum([If(x[i], values[i], 0) for i in range(12)]) + diversity_bonus

# Maximize total value
opt.maximize(total_value)

result = opt.check()

if result == sat:
    m = opt.model()
    selected = [i for i in range(12) if is_true(m.eval(x[i]))]
    total_val = m.eval(total_value)
    bonus_achieved = is_true(m.eval(And(research_selected, development_selected, deployment_selected)))
    
    # Compute resource usage
    comp_used = sum(compute[i] for i in selected)
    bw_used = sum(bandwidth[i] for i in selected)
    stor_used = sum(storage[i] for i in selected)
    spec_base = sum(specialists[i] for i in selected)
    dev_sel = any(i in selected for i in range(4, 8))
    deploy_sel = [i for i in selected if i in range(8, 12)]
    spec_extra = 5 * len(deploy_sel) if dev_sel else 0
    spec_used = spec_base + spec_extra
    
    print("STATUS: sat")
    print(f"selected_tasks = {sorted(selected)}")
    print(f"total_value = {total_val}")
    print(f"bonus_achieved = {bonus_achieved}")
    print(f"resource_usage = {{")
    print(f"  compute: {comp_used}")
    print(f"  bandwidth: {bw_used}")
    print(f"  storage: {stor_used}")
    print(f"  specialists: {spec_used}")
    print(f"}}")
else:
    print("STATUS: unsat")