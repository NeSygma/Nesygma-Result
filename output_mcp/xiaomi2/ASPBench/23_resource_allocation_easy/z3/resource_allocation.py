from z3 import *

# Create optimizer
opt = Optimize()

# Task data
tasks = [0, 1, 2, 3, 4, 5]
values = [50, 40, 60, 35, 70, 45]
res_a = [30, 25, 20, 15, 40, 20]
res_b = [20, 15, 30, 25, 10, 20]
res_c = [10, 15, 20, 10, 25, 15]

# Resource capacities
cap_a = 100
cap_b = 80
cap_c = 60

# Binary decision variables: 1 if task is selected, 0 otherwise
x = [Int(f'x_{i}') for i in tasks]

# Each task is binary (0 or 1)
for i in tasks:
    opt.add(Or(x[i] == 0, x[i] == 1))

# Resource capacity constraints
opt.add(Sum([x[i] * res_a[i] for i in tasks]) <= cap_a)
opt.add(Sum([x[i] * res_b[i] for i in tasks]) <= cap_b)
opt.add(Sum([x[i] * res_c[i] for i in tasks]) <= cap_c)

# Objective: maximize total value
total_value = Sum([x[i] * values[i] for i in tasks])
opt.maximize(total_value)

# Solve
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract selected tasks
    selected = []
    for i in tasks:
        if model[x[i]].as_long() == 1:
            selected.append(i)
    selected.sort()
    
    # Calculate resource usage
    usage_a = sum(res_a[i] for i in selected)
    usage_b = sum(res_b[i] for i in selected)
    usage_c = sum(res_c[i] for i in selected)
    total_val = sum(values[i] for i in selected)
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected}")
    print(f"total_value: {total_val}")
    print(f"resource_usage:")
    print(f"  resource_a: {usage_a}")
    print(f"  resource_b: {usage_b}")
    print(f"  resource_c: {usage_c}")
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")