from z3 import *

# Data
num_tasks = 6
values = [50, 40, 60, 35, 70, 45]
res_a = [30, 25, 20, 15, 40, 20]
res_b = [20, 15, 30, 25, 10, 20]
res_c = [10, 15, 20, 10, 25, 15]

capacity_a = 100
capacity_b = 80
capacity_c = 60

# Optimization
opt = Optimize()

# Decision variables: 0-1 selection for each task
selected = [Bool(f'task_{i}') for i in range(num_tasks)]

# Constraints
opt.add(Sum([If(selected[i], res_a[i], 0) for i in range(num_tasks)]) <= capacity_a)
opt.add(Sum([If(selected[i], res_b[i], 0) for i in range(num_tasks)]) <= capacity_b)
opt.add(Sum([If(selected[i], res_c[i], 0) for i in range(num_tasks)]) <= capacity_c)

# Objective
total_value = Sum([If(selected[i], values[i], 0) for i in range(num_tasks)])
opt.maximize(total_value)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    selected_tasks = [i for i in range(num_tasks) if is_true(m[selected[i]])]
    val = m.evaluate(total_value)
    usage_a = m.evaluate(Sum([If(selected[i], res_a[i], 0) for i in range(num_tasks)]))
    usage_b = m.evaluate(Sum([If(selected[i], res_b[i], 0) for i in range(num_tasks)]))
    usage_c = m.evaluate(Sum([If(selected[i], res_c[i], 0) for i in range(num_tasks)]))
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected_tasks}")
    print(f"total_value: {val}")
    print(f"resource_usage: {{'resource_a': {usage_a}, 'resource_b': {usage_b}, 'resource_c': {usage_c}}}")
else:
    print("STATUS: unsat")