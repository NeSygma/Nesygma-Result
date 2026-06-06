from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solvable problems)
BENCHMARK_MODE = True

# Create an Optimize solver for minimization
opt = Optimize()

# --- Task Definitions ---
# Roast Chicken steps
tasks = {
    "prep_chicken": {"duration": 15, "resource": "prep_area"},
    "bake_chicken": {"duration": 50, "resource": "oven"},
    "rest_chicken": {"duration": 10, "resource": "prep_area"},
    
    # Vegetable Soup steps
    "chop_veg_soup": {"duration": 20, "resource": "prep_area"},
    "simmer_stock": {"duration": 30, "resource": "stove"},
    
    # Risotto steps
    "chop_onion": {"duration": 5, "resource": "prep_area"},
    "cook_risotto": {"duration": 25, "resource": "stove"},
    
    # Side Salad steps
    "wash_greens": {"duration": 5, "resource": "prep_area"},
    "mix_dressing": {"duration": 10, "resource": "prep_area"},
    
    # Special task
    "preheat_oven": {"duration": 10, "resource": "oven"},
}

# --- Declare start and end times for all tasks ---
start = {task: Int(f"start_{task}") for task in tasks}
end = {task: Int(f"end_{task}") for task in tasks}

# --- Add duration constraints: end = start + duration ---
for task in tasks:
    opt.add(end[task] == start[task] + tasks[task]["duration"])

# --- Step precedences within recipes ---
# Roast Chicken: prep_chicken → bake_chicken → rest_chicken
opt.add(start["bake_chicken"] >= end["prep_chicken"])
opt.add(start["rest_chicken"] >= end["bake_chicken"])

# Vegetable Soup: chop_veg_soup → simmer_stock
opt.add(start["simmer_stock"] >= end["chop_veg_soup"])

# Risotto: chop_onion → cook_risotto
opt.add(start["cook_risotto"] >= end["chop_onion"])

# Side Salad: wash_greens → mix_dressing
opt.add(start["mix_dressing"] >= end["wash_greens"])

# --- Inter-recipe dependency: simmer_stock must finish before cook_risotto starts ---
opt.add(start["cook_risotto"] >= end["simmer_stock"])

# --- Oven preheating: preheat_oven must finish before bake_chicken starts ---
opt.add(start["bake_chicken"] >= end["preheat_oven"])

# --- Resource constraints ---
# prep_area: capacity 2 (no more than 2 tasks overlapping)
prep_area_tasks = [t for t in tasks if tasks[t]["resource"] == "prep_area"]
for i in range(len(prep_area_tasks)):
    for j in range(i + 1, len(prep_area_tasks)):
        task_i = prep_area_tasks[i]
        task_j = prep_area_tasks[j]
        # Ensure no more than 2 tasks overlap
        opt.add(Not(And(
            start[task_i] < end[task_j],
            start[task_j] < end[task_i]
        )))

# oven: capacity 1 (no more than 1 task overlapping)
oven_tasks = [t for t in tasks if tasks[t]["resource"] == "oven"]
for i in range(len(oven_tasks)):
    for j in range(i + 1, len(oven_tasks)):
        task_i = oven_tasks[i]
        task_j = oven_tasks[j]
        opt.add(Not(And(
            start[task_i] < end[task_j],
            start[task_j] < end[task_i]
        )))

# stove: capacity 1 (no more than 1 task overlapping)
stove_tasks = [t for t in tasks if tasks[t]["resource"] == "stove"]
for i in range(len(stove_tasks)):
    for j in range(i + 1, len(stove_tasks)):
        task_i = stove_tasks[i]
        task_j = stove_tasks[j]
        opt.add(Not(And(
            start[task_i] < end[task_j],
            start[task_j] < end[task_i]
        )))

# --- Objective: Minimize makespan (total time) ---
total_time = Int("total_time")
opt.add(total_time >= end[task] for task in tasks)
opt.minimize(total_time)

# --- Check and print results ---
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Optimal total_time: {model[total_time]}")
    print("\nSchedule:")
    for task in tasks:
        print(f"{task}: start={model[start[task]]}, end={model[end[task]]}, resource={tasks[task]['resource']}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")