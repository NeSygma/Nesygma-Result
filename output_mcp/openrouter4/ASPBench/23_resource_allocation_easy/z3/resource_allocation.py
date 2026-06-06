from z3 import *

# Create optimizer
opt = Optimize()

# 6 tasks, each can be selected (1) or not (0)
tasks = [Bool(f'task_{i}') for i in range(6)]

# Task data
values = [50, 40, 60, 35, 70, 45]
res_a = [30, 25, 20, 15, 40, 20]
res_b = [20, 15, 30, 25, 10, 20]
res_c = [10, 15, 20, 10, 25, 15]

# Resource capacity constraints
total_a = Sum([If(tasks[i], res_a[i], 0) for i in range(6)])
total_b = Sum([If(tasks[i], res_b[i], 0) for i in range(6)])
total_c = Sum([If(tasks[i], res_c[i], 0) for i in range(6)])

opt.add(total_a <= 100)
opt.add(total_b <= 80)
opt.add(total_c <= 60)

# Objective: maximize total value
total_value_expr = Sum([If(tasks[i], values[i], 0) for i in range(6)])
opt.maximize(total_value_expr)

# Solve
result = opt.check()

BENCHMARK_MODE = True

if result == sat:
    m = opt.model()
    
    # Extract selected tasks (sorted)
    selected = [i for i in range(6) if is_true(m.eval(tasks[i], model_completion=True))]
    
    total_value = sum(values[i] for i in selected)
    used_a = sum(res_a[i] for i in selected)
    used_b = sum(res_b[i] for i in selected)
    used_c = sum(res_c[i] for i in selected)
    
    print("STATUS: sat")
    print(f"selected_tasks = {selected}")
    print(f"total_value = {total_value}")
    print(f"resource_usage = {{'resource_a': {used_a}, 'resource_b': {used_b}, 'resource_c': {used_c}}}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")