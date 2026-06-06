from z3 import *

# Problem data
tasks = [
    # ID, Category, Value, Compute, Bandwidth, Storage, Specialists
    (0, "Research", 40, 20, 10, 30, 5),
    (1, "Research", 60, 30, 25, 20, 10),
    (2, "Research", 70, 25, 20, 15, 5),
    (3, "Research", 55, 20, 15, 25, 10),
    (4, "Development", 80, 40, 30, 20, 20),
    (5, "Development", 90, 35, 25, 30, 15),
    (6, "Development", 75, 30, 40, 25, 18),
    (7, "Development", 85, 45, 35, 15, 22),
    (8, "Deployment", 65, 15, 20, 40, 8),
    (9, "Deployment", 80, 20, 30, 35, 12),
    (10, "Deployment", 70, 25, 25, 30, 10),
    (11, "Deployment", 95, 30, 35, 45, 15)
]

# Resource capacities
CAP_COMPUTE = 150
CAP_BANDWIDTH = 120
CAP_STORAGE = 140
CAP_SPECIALISTS = 60

# Create solver
solver = Optimize()

# Binary selection variables for each task
selected = [Bool(f"task_{i}") for i in range(12)]

# Helper functions to get task properties
def get_value(i): return tasks[i][2]
def get_compute(i): return tasks[i][3]
def get_bandwidth(i): return tasks[i][4]
def get_storage(i): return tasks[i][5]
def get_specialists(i): return tasks[i][6]
def get_category(i): return tasks[i][1]

# 1. Resource constraints
# Compute usage
compute_usage = Sum([If(selected[i], get_compute(i), 0) for i in range(12)])
solver.add(compute_usage <= CAP_COMPUTE)

# Bandwidth usage
bandwidth_usage = Sum([If(selected[i], get_bandwidth(i), 0) for i in range(12)])
solver.add(bandwidth_usage <= CAP_BANDWIDTH)

# Storage usage
storage_usage = Sum([If(selected[i], get_storage(i), 0) for i in range(12)])
solver.add(storage_usage <= CAP_STORAGE)

# Specialist usage (base + conditional)
# Base specialists
base_specialists = Sum([If(selected[i], get_specialists(i), 0) for i in range(12)])

# Conditional specialist cost: if any Development task selected, each Deployment task gets +5
# Check if any Development task (4-7) is selected
any_development_selected = Or([selected[i] for i in range(4, 8)])

# Additional specialists for Deployment tasks (8-11) if any Development selected
additional_specialists = Sum([If(And(selected[i], any_development_selected), 5, 0) for i in range(8, 12)])

total_specialists = base_specialists + additional_specialists
solver.add(total_specialists <= CAP_SPECIALISTS)

# 2. Prerequisite: Task 4 requires Task 0
# If task 4 is selected, task 0 must be selected
solver.add(Implies(selected[4], selected[0]))

# 3. Mutual exclusion: Task 1 and Task 7 cannot both be selected
solver.add(Not(And(selected[1], selected[7])))

# 4. Diversity bonus calculation
# Check if at least one task from each category is selected
has_research = Or([selected[i] for i in range(4)])  # Tasks 0-3
has_development = Or([selected[i] for i in range(4, 8)])  # Tasks 4-7
has_deployment = Or([selected[i] for i in range(8, 12)])  # Tasks 8-11

diversity_achieved = And(has_research, has_development, has_deployment)

# 5. Objective: Maximize total value
# Base value from selected tasks
base_value = Sum([If(selected[i], get_value(i), 0) for i in range(12)])

# Total value with bonus
total_value = base_value + If(diversity_achieved, 100, 0)

# Maximize total value
solver.maximize(total_value)

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract selected tasks
    selected_tasks = []
    for i in range(12):
        if is_true(model[selected[i]]):
            selected_tasks.append(i)
    
    # Calculate actual values from model
    actual_base_value = sum(get_value(i) for i in selected_tasks)
    
    # Check diversity bonus
    categories = set()
    for i in selected_tasks:
        categories.add(get_category(i))
    bonus_achieved = len(categories) == 3
    
    total_value_actual = actual_base_value + (100 if bonus_achieved else 0)
    
    # Calculate resource usage
    compute_used = sum(get_compute(i) for i in selected_tasks)
    bandwidth_used = sum(get_bandwidth(i) for i in selected_tasks)
    storage_used = sum(get_storage(i) for i in selected_tasks)
    
    # Specialist usage with conditional cost
    specialists_used = sum(get_specialists(i) for i in selected_tasks)
    if any(get_category(i) == "Development" for i in selected_tasks):
        specialists_used += sum(5 for i in selected_tasks if get_category(i) == "Deployment")
    
    # Print results
    print(f"selected_tasks: {sorted(selected_tasks)}")
    print(f"total_value: {total_value_actual}")
    print(f"bonus_achieved: {bonus_achieved}")
    print(f"resource_usage:")
    print(f"  compute: {compute_used}")
    print(f"  bandwidth: {bandwidth_used}")
    print(f"  storage: {storage_used}")
    print(f"  specialists: {specialists_used}")
    
    # Verify constraints
    print("\nConstraint verification:")
    print(f"Compute limit: {compute_used} <= {CAP_COMPUTE} ✓" if compute_used <= CAP_COMPUTE else f"Compute limit: {compute_used} <= {CAP_COMPUTE} ✗")
    print(f"Bandwidth limit: {bandwidth_used} <= {CAP_BANDWIDTH} ✓" if bandwidth_used <= CAP_BANDWIDTH else f"Bandwidth limit: {bandwidth_used} <= {CAP_BANDWIDTH} ✗")
    print(f"Storage limit: {storage_used} <= {CAP_STORAGE} ✓" if storage_used <= CAP_STORAGE else f"Storage limit: {storage_used} <= {CAP_STORAGE} ✗")
    print(f"Specialists limit: {specialists_used} <= {CAP_SPECIALISTS} ✓" if specialists_used <= CAP_SPECIALISTS else f"Specialists limit: {specialists_used} <= {CAP_SPECIALISTS} ✗")
    
    # Check prerequisite
    if 4 in selected_tasks and 0 not in selected_tasks:
        print("Prerequisite violation: Task 4 selected without Task 0 ✗")
    else:
        print("Prerequisite satisfied ✓")
    
    # Check mutual exclusion
    if 1 in selected_tasks and 7 in selected_tasks:
        print("Mutual exclusion violation: Tasks 1 and 7 both selected ✗")
    else:
        print("Mutual exclusion satisfied ✓")
    
    # Check expected optimal value
    if total_value_actual == 470:
        print(f"\n✓ OPTIMAL VALUE ACHIEVED: {total_value_actual}")
    else:
        print(f"\nNote: Expected optimal value 470, got {total_value_actual}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")