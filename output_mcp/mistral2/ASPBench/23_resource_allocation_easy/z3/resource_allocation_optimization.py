from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solvable instance)
BENCHMARK_MODE = True

# Initialize optimizer for maximization
opt = Optimize()

# Decision variables: whether each task is selected (0-1)
selected = [Bool(f"selected_{i}") for i in range(6)]

# Resource capacities
resource_a_capacity = 100
resource_b_capacity = 80
resource_c_capacity = 60

# Task data: [value, resource_a, resource_b, resource_c]
task_data = [
    (50, 30, 20, 10),
    (40, 25, 15, 15),
    (60, 20, 30, 20),
    (35, 15, 25, 10),
    (70, 40, 10, 25),
    (45, 20, 20, 15),
]

# Total value to maximize
total_value = Int('total_value')
opt.add(total_value == Sum([If(selected[i], task_data[i][0], 0) for i in range(6)]))
opt.maximize(total_value)

# Resource usage constraints
resource_a_used = Sum([If(selected[i], task_data[i][1], 0) for i in range(6)])
resource_b_used = Sum([If(selected[i], task_data[i][2], 0) for i in range(6)])
resource_c_used = Sum([If(selected[i], task_data[i][3], 0) for i in range(6)])

opt.add(resource_a_used <= resource_a_capacity)
opt.add(resource_b_used <= resource_b_capacity)
opt.add(resource_c_used <= resource_c_capacity)

# Each task selected at most once (already enforced by 0-1 selection)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract selected tasks
    selected_tasks = [i for i in range(6) if is_true(model[selected[i]])]
    selected_tasks.sort()
    print(f"selected_tasks = {selected_tasks}")
    
    # Extract total value
    total_value_model = model[total_value]
    print(f"total_value = {total_value_model}")
    
    # Extract resource usage using model.eval
    resource_a_used_model = model.eval(resource_a_used)
    resource_b_used_model = model.eval(resource_b_used)
    resource_c_used_model = model.eval(resource_c_used)
    print(f"resource_usage = {{")
    print(f"  resource_a = {resource_a_used_model},")
    print(f"  resource_b = {resource_b_used_model},")
    print(f"  resource_c = {resource_c_used_model}")
    print(f"}}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")