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

# Resource capacities
capacity_a = 100
capacity_b = 80
capacity_c = 60

# Create solver
opt = Optimize()

# Decision variables: selected[i] = 1 if task i is selected, 0 otherwise
selected = [Bool(f"selected_{i}") for i in range(6)]

# Convert Bool to Int for arithmetic (1 for True, 0 for False)
selected_int = [If(sel, 1, 0) for sel in selected]

# Resource usage calculations
resource_a_usage = Sum([selected_int[i] * tasks[i]["a"] for i in range(6)])
resource_b_usage = Sum([selected_int[i] * tasks[i]["b"] for i in range(6)])
resource_c_usage = Sum([selected_int[i] * tasks[i]["c"] for i in range(6)])

# Total value calculation
total_value = Sum([selected_int[i] * tasks[i]["value"] for i in range(6)])

# Add constraints
opt.add(resource_a_usage <= capacity_a)
opt.add(resource_b_usage <= capacity_b)
opt.add(resource_c_usage <= capacity_c)

# Maximize total value
opt.maximize(total_value)

# Check and get solution
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract selected tasks
    selected_tasks = []
    for i in range(6):
        if is_true(model[selected[i]]):
            selected_tasks.append(i)
    
    # Calculate final values
    final_value = sum(tasks[i]["value"] for i in selected_tasks)
    final_a = sum(tasks[i]["a"] for i in selected_tasks)
    final_b = sum(tasks[i]["b"] for i in selected_tasks)
    final_c = sum(tasks[i]["c"] for i in selected_tasks)
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected_tasks}")
    print(f"total_value: {final_value}")
    print(f"resource_usage:")
    print(f"  resource_a: {final_a}")
    print(f"  resource_b: {final_b}")
    print(f"  resource_c: {final_c}")
    
    # Verify optimal value matches expected
    if final_value == 180:
        print("Optimal value matches expected: 180")
    else:
        print(f"Note: Found value {final_value}, expected 180")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution exists")
else:
    print("STATUS: unknown")
    print("Solver could not determine feasibility")