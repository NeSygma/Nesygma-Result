from z3 import *

# Define data
values = [40,60,70,55,80,90,75,85,65,80,70,95]
compute = [20,30,25,20,40,35,30,45,15,20,25,30]
bandwidth = [10,25,20,15,30,25,40,35,20,30,25,35]
storage = [30,20,15,25,20,30,25,15,40,35,30,45]
specialists_base = [5,10,5,10,20,15,18,22,8,12,10,15]

# Indices
research_indices = [0,1,2,3]
dev_indices = [4,5,6,7]
deploy_indices = [8,9,10,11]

# Decision variables
selected = [Int(f'sel_{i}') for i in range(12)]

solver = Optimize()

# 0-1 constraints
for i in range(12):
    solver.add(selected[i] >= 0, selected[i] <= 1)

# Prerequisite: Task 4 requires Task 0
solver.add(selected[4] <= selected[0])

# Mutual exclusion: Task 1 and Task 7 cannot both be selected
solver.add(selected[1] + selected[7] <= 1)

# Booleans for categories
hasResearch = Or([selected[i] == 1 for i in research_indices])
hasDev = Or([selected[i] == 1 for i in dev_indices])
hasDeploy = Or([selected[i] == 1 for i in deploy_indices])

# Bonus
bonus = And(hasResearch, hasDev, hasDeploy)

# Resource usage expressions
total_compute = Sum([selected[i] * compute[i] for i in range(12)])
total_bandwidth = Sum([selected[i] * bandwidth[i] for i in range(12)])
total_storage = Sum([selected[i] * storage[i] for i in range(12)])
# Conditional specialist cost
dev_selected_any = Or([selected[i] == 1 for i in dev_indices])
# Sum of selected deployment tasks
selected_deploy_count = Sum([selected[i] for i in deploy_indices])
# Base specialists sum
base_specialists = Sum([selected[i] * specialists_base[i] for i in range(12)])
# Total specialists with conditional cost
total_specialists = base_specialists + If(dev_selected_any, 5 * selected_deploy_count, 0)

# Resource limits
solver.add(total_compute <= 150)
solver.add(total_bandwidth <= 120)
solver.add(total_storage <= 140)
solver.add(total_specialists <= 60)

# Objective: maximize total value + bonus
total_value_expr = Sum([selected[i] * values[i] for i in range(12)]) + If(bonus, 100, 0)
solver.maximize(total_value_expr)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    # Extract selected tasks
    selected_tasks = [i for i in range(12) if model.eval(selected[i]).as_long() == 1]
    selected_tasks.sort()
    # Compute resource usage
    compute_used = sum(model.eval(selected[i]).as_long() * compute[i] for i in range(12))
    bandwidth_used = sum(model.eval(selected[i]).as_long() * bandwidth[i] for i in range(12))
    storage_used = sum(model.eval(selected[i]).as_long() * storage[i] for i in range(12))
    base_spec_used = sum(model.eval(selected[i]).as_long() * specialists_base[i] for i in range(12))
    deploy_selected = sum(model.eval(selected[i]).as_long() for i in deploy_indices)
    dev_any = any(model.eval(selected[i]).as_long() == 1 for i in dev_indices)
    conditional_spec = 5 * deploy_selected if dev_any else 0
    specialists_used = base_spec_used + conditional_spec
    # Bonus achieved
    bonus_achieved = bool(model.eval(bonus))
    # Total value
    total_value = sum(model.eval(selected[i]).as_long() * values[i] for i in range(12)) + (100 if bonus_achieved else 0)
    # Output
    print("STATUS: sat")
    print(f"selected_tasks = {selected_tasks}")
    print(f"total_value = {total_value}")
    print(f"bonus_achieved = {bonus_achieved}")
    print("resource_usage = {")
    print(f"  compute: {compute_used},")
    print(f"  bandwidth: {bandwidth_used},")
    print(f"  storage: {storage_used},")
    print(f"  specialists: {specialists_used}")
    print("}")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")