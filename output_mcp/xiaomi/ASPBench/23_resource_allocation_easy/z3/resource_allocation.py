from z3 import *

# Create optimizer
opt = Optimize()

# Decision variables: binary selection for each task (0 or 1)
tasks = [Int(f'task_{i}') for i in range(6)]

# Each task is binary (0 or 1)
for i in range(6):
    opt.add(Or(tasks[i] == 0, tasks[i] == 1))

# Task data
values = [50, 40, 60, 35, 70, 45]
res_a = [30, 25, 20, 15, 40, 20]
res_b = [20, 15, 30, 25, 10, 20]
res_c = [10, 15, 20, 10, 25, 15]

# Resource capacity constraints
opt.add(Sum([tasks[i] * res_a[i] for i in range(6)]) <= 100)
opt.add(Sum([tasks[i] * res_b[i] for i in range(6)]) <= 80)
opt.add(Sum([tasks[i] * res_c[i] for i in range(6)]) <= 60)

# Objective: maximize total value
total_value = Sum([tasks[i] * values[i] for i in range(6)])
opt.maximize(total_value)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    selected = []
    for i in range(6):
        if m[tasks[i]].as_long() == 1:
            selected.append(i)
    selected.sort()
    
    total_val = sum(values[i] for i in selected)
    usage_a = sum(res_a[i] for i in selected)
    usage_b = sum(res_b[i] for i in selected)
    usage_c = sum(res_c[i] for i in selected)
    
    print("STATUS: sat")
    print(f"selected_tasks = {selected}")
    print(f"total_value = {total_val}")
    print(f"resource_a = {usage_a}")
    print(f"resource_b = {usage_b}")
    print(f"resource_c = {usage_c}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")