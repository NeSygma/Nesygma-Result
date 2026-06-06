from z3 import *

# Problem data
tasks = [
    {"id": 0, "value": 50, "a": 30, "b": 20, "c": 10},
    {"id": 1, "value": 40, "a": 25, "b": 15, "c": 15},
    {"id": 2, "value": 60, "a": 20, "b": 30, "c": 20},
    {"id": 3, "value": 35, "a": 15, "b": 25, "c": 10},
    {"id": 4, "value": 70, "a": 40, "b": 10, "c": 25},
    {"id": 5, "value": 45, "a": 20, "b": 20, "c": 15}
]

cap_a = 100
cap_b = 80
cap_c = 60

# Create solver
opt = Optimize()

# Binary decision variables: x[i] = 1 if task i is selected
x = [Bool(f"x_{i}") for i in range(6)]

# Resource usage expressions
usage_a = Sum([If(x[i], tasks[i]["a"], 0) for i in range(6)])
usage_b = Sum([If(x[i], tasks[i]["b"], 0) for i in range(6)])
usage_c = Sum([If(x[i], tasks[i]["c"], 0) for i in range(6)])

# Resource capacity constraints
opt.add(usage_a <= cap_a)
opt.add(usage_b <= cap_b)
opt.add(usage_c <= cap_c)

# Objective: maximize total value
total_value = Sum([If(x[i], tasks[i]["value"], 0) for i in range(6)])
opt.maximize(total_value)

# Check and get model
BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract selected tasks
    selected = []
    for i in range(6):
        if is_true(model[x[i]]):
            selected.append(i)
    selected.sort()
    
    # Calculate total value and resource usage
    total_val = sum(tasks[i]["value"] for i in selected)
    res_a = sum(tasks[i]["a"] for i in selected)
    res_b = sum(tasks[i]["b"] for i in selected)
    res_c = sum(tasks[i]["c"] for i in selected)
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected}")
    print(f"total_value: {total_val}")
    print(f"resource_usage: {{'resource_a': {res_a}, 'resource_b': {res_b}, 'resource_c': {res_c}}}")
    
    # Verify expected optimal value
    if total_val == 180:
        print("Optimal value matches expected: 180")
    else:
        print(f"Warning: Expected 180, got {total_val}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")