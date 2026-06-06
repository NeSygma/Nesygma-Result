from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create solver for optimization
opt = Optimize()

# Total time variable (makespan)
total_time = Int('total_time')
opt.add(total_time >= 0)

# Define tasks with their durations and required resources
# Format: (task_name, duration, resource_type)
tasks = [
    # Roast Chicken
    ("prep_chicken", 15, "prep_area"),
    ("bake_chicken", 50, "oven"),
    ("rest_chicken", 10, "prep_area"),
    
    # Vegetable Soup
    ("chop_veg_soup", 20, "prep_area"),
    ("simmer_stock", 30, "stove"),
    
    # Risotto
    ("chop_onion", 5, "prep_area"),
    ("cook_risotto", 25, "stove"),
    
    # Side Salad
    ("wash_greens", 5, "prep_area"),
    ("mix_dressing", 10, "prep_area"),
    
    # Special task
    ("preheat_oven", 10, "oven"),
]

# Create start and end time variables for each task
start = {task: Int(f'start_{task}') for task, _, _ in tasks}
end = {task: Int(f'end_{task}') for task, _, _ in tasks}

# Add duration constraints: end = start + duration
for task, duration, _ in tasks:
    opt.add(end[task] == start[task] + duration)
    opt.add(start[task] >= 0)
    opt.add(end[task] <= total_time)

# Resource capacity constraints
# prep_area: capacity 2
prep_tasks = [task for task, _, res in tasks if res == "prep_area"]
for i in range(len(prep_tasks)):
    for j in range(i+1, len(prep_tasks)):
        task_i = prep_tasks[i]
        task_j = prep_tasks[j]
        opt.add(Not(And(start[task_i] < end[task_j], start[task_j] < end[task_i])))

# oven: capacity 1
oven_tasks = [task for task, _, res in tasks if res == "oven"]
for i in range(len(oven_tasks)):
    for j in range(i+1, len(oven_tasks)):
        task_i = oven_tasks[i]
        task_j = oven_tasks[j]
        opt.add(Not(And(start[task_i] < end[task_j], start[task_j] < end[task_i])))

# stove: capacity 1
stove_tasks = [task for task, _, res in tasks if res == "stove"]
for i in range(len(stove_tasks)):
    for j in range(i+1, len(stove_tasks)):
        task_i = stove_tasks[i]
        task_j = stove_tasks[j]
        opt.add(Not(And(start[task_i] < end[task_j], start[task_j] < end[task_i])))

# Step precedences within each recipe
# Roast Chicken: prep_chicken → bake_chicken → rest_chicken
opt.add(start["bake_chicken"] >= end["prep_chicken"])
opt.add(start["rest_chicken"] >= end["bake_chicken"])

# Vegetable Soup: chop_veg_soup → simmer_stock
opt.add(start["simmer_stock"] >= end["chop_veg_soup"])

# Risotto: chop_onion → cook_risotto
opt.add(start["cook_risotto"] >= end["chop_onion"])

# Side Salad: wash_greens → mix_dressing
opt.add(start["mix_dressing"] >= end["wash_greens"])

# Inter-recipe dependency: simmer_stock must finish before cook_risotto starts
opt.add(start["cook_risotto"] >= end["simmer_stock"])

# Oven preheating: preheat_oven must complete before any bake_chicken step starts
opt.add(start["bake_chicken"] >= end["preheat_oven"])

# Minimize total_time
opt.minimize(total_time)

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"total_time = {model[total_time]}")
    
    # Print schedule
    print("\nSchedule:")
    for task, _, resource in tasks:
        print(f"{task}: start={model[start[task]]}, end={model[end[task]]}, resource={resource}")
    
    # Verify expected optimal value
    if model[total_time].as_long() == 75:
        print("\nOptimal value verified: total_time=75")
    else:
        print(f"\nWARNING: Expected total_time=75, got {model[total_time]}")
    
    # Check feasibility
    print("\nfeasible = True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")