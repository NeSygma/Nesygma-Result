from z3 import *

# Instance data
num_tasks = 6
values = [50, 40, 60, 35, 70, 45]
req_a = [30, 25, 20, 15, 40, 20]
req_b = [20, 15, 30, 25, 10, 20]
req_c = [10, 15, 20, 10, 25, 15]

cap_a = 100
cap_b = 80
cap_c = 60

# Decision variables: 0-1 selection for each task
x = [Bool(f'x_{i}') for i in range(num_tasks)]

opt = Optimize()

# Resource capacity constraints
opt.add(Sum([If(x[i], req_a[i], 0) for i in range(num_tasks)]) <= cap_a)
opt.add(Sum([If(x[i], req_b[i], 0) for i in range(num_tasks)]) <= cap_b)
opt.add(Sum([If(x[i], req_c[i], 0) for i in range(num_tasks)]) <= cap_c)

# Objective: maximize total value
total_value = Sum([If(x[i], values[i], 0) for i in range(num_tasks)])
opt.maximize(total_value)

result = opt.check()

if result == sat:
    m = opt.model()
    selected = [i for i in range(num_tasks) if is_true(m[x[i]])]
    total_val = sum(values[i] for i in selected)
    used_a = sum(req_a[i] for i in selected)
    used_b = sum(req_b[i] for i in selected)
    used_c = sum(req_c[i] for i in selected)
    
    print("STATUS: sat")
    print(f"selected_tasks = {selected}")
    print(f"total_value = {total_val}")
    print(f"resource_usage = {{'resource_a': {used_a}, 'resource_b': {used_b}, 'resource_c': {used_c}}}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")