from z3 import *

# Define data
values = [40,60,70,55,80,90,75,85,65,80,70,95]
compute = [20,30,25,20,40,35,30,45,15,20,25,30]
bandwidth = [10,25,20,15,30,25,40,35,20,30,25,35]
storage = [30,20,15,25,20,30,25,15,40,35,30,45]
specialists_base = [5,10,5,10,20,15,18,22,8,12,10,15]

# Categories indices
research = list(range(0,4))
development = list(range(4,8))
deployment = list(range(8,12))

# Capacities
cap_compute = 150
cap_bandwidth = 120
cap_storage = 140
cap_specialists = 60

# Solver
opt = Optimize()
# selection booleans
sel = [Bool(f'sel_{i}') for i in range(12)]

# Resource constraints
opt.add(Sum([If(sel[i], compute[i], 0) for i in range(12)]) <= cap_compute)
opt.add(Sum([If(sel[i], bandwidth[i], 0) for i in range(12)]) <= cap_bandwidth)
opt.add(Sum([If(sel[i], storage[i], 0) for i in range(12)]) <= cap_storage)
# Conditional specialist cost
dev_selected = Or([sel[i] for i in development])
# extra cost per selected deployment if any dev selected
extra_per_deploy = If(dev_selected, 5, 0)
opt.add(Sum([If(sel[i], specialists_base[i], 0) for i in range(12)]) +
        Sum([If(sel[i], extra_per_deploy, 0) for i in deployment]) <= cap_specialists)
# Prerequisite: task 4 requires task 0
opt.add(Implies(sel[4], sel[0]))
# Mutual exclusion: task1 and task7 cannot both be selected
opt.add(Not(And(sel[1], sel[7])))
# Diversity bonus condition
bonus_achieved = And(Or([sel[i] for i in research]), Or([sel[i] for i in development]), Or([sel[i] for i in deployment]))
# Objective: maximize total value + bonus
total_value_expr = Sum([If(sel[i], values[i], 0) for i in range(12)]) + If(bonus_achieved, 100, 0)
opt.maximize(total_value_expr)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Extract selections
    selected_ids = [i for i in range(12) if m.eval(sel[i])]
    # Compute resource usage
    compute_used = sum(compute[i] for i in selected_ids)
    bandwidth_used = sum(bandwidth[i] for i in selected_ids)
    storage_used = sum(storage[i] for i in selected_ids)
    # specialists includes extra cost if any dev selected
    dev_sel = any(i in selected_ids for i in development)
    extra = 5 if dev_sel else 0
    specialists_used = sum(specialists_base[i] for i in selected_ids) + extra * sum(1 for i in selected_ids if i in deployment)
    # total value
    base_val = sum(values[i] for i in selected_ids)
    bonus = 100 if (any(i in selected_ids for i in research) and any(i in selected_ids for i in development) and any(i in selected_ids for i in deployment)) else 0
    total_val = base_val + bonus
    # Print results
    print("STATUS: sat")
    print("selected_tasks =", selected_ids)
    print("total_value =", total_val)
    print("bonus_achieved =", bonus == 100)
    print("resource_usage = {")
    print(f"  'compute': {compute_used},")
    print(f"  'bandwidth': {bandwidth_used},")
    print(f"  'storage': {storage_used},")
    print(f"  'specialists': {specialists_used}")
    print("}")
else:
    print("STATUS: unsat")