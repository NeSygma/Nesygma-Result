from z3 import *

# Problem data
recipes = {
    "pasta": [
        {"name": "prep", "duration": 10, "resource": "prep_area"},
        {"name": "boil", "duration": 15, "resource": "stove"},
        {"name": "serve", "duration": 5, "resource": "prep_area"}
    ],
    "salad": [
        {"name": "chop", "duration": 15, "resource": "prep_area"},
        {"name": "mix", "duration": 5, "resource": "prep_area"}
    ],
    "bread": [
        {"name": "bake", "duration": 30, "resource": "oven"}
    ]
}

resources = ["oven", "stove", "prep_area"]

# Create solver
opt = Optimize()

# Create variables for each step: start_time
step_vars = {}
for recipe_name, steps in recipes.items():
    for step in steps:
        step_id = f"{recipe_name}_{step['name']}"
        step_vars[step_id] = Int(f"start_{step_id}")
        # Non-negative start times
        opt.add(step_vars[step_id] >= 0)

# Precedence constraints within recipes
for recipe_name, steps in recipes.items():
    for i in range(len(steps) - 1):
        current_step = steps[i]
        next_step = steps[i + 1]
        current_id = f"{recipe_name}_{current_step['name']}"
        next_id = f"{recipe_name}_{next_step['name']}"
        # Current step must finish before next step starts
        opt.add(step_vars[next_id] >= step_vars[current_id] + current_step['duration'])

# Resource constraints: no overlapping usage for same resource
# Group steps by resource
steps_by_resource = {res: [] for res in resources}
for recipe_name, steps in recipes.items():
    for step in steps:
        step_id = f"{recipe_name}_{step['name']}"
        steps_by_resource[step['resource']].append((step_id, step['duration']))

# For each resource, ensure no overlapping intervals
for resource, step_list in steps_by_resource.items():
    for i in range(len(step_list)):
        for j in range(i + 1, len(step_list)):
            step1_id, dur1 = step_list[i]
            step2_id, dur2 = step_list[j]
            # Either step1 finishes before step2 starts OR step2 finishes before step1 starts
            opt.add(Or(
                step_vars[step1_id] + dur1 <= step_vars[step2_id],
                step_vars[step2_id] + dur2 <= step_vars[step1_id]
            ))

# Objective: minimize total completion time (max end time)
# Create a variable for total time
total_time = Int('total_time')
opt.add(total_time >= 0)

# Total time must be at least the end time of every step
for recipe_name, steps in recipes.items():
    for step in steps:
        step_id = f"{recipe_name}_{step['name']}"
        opt.add(total_time >= step_vars[step_id] + step['duration'])

# Minimize total time
opt.minimize(total_time)

# Check and get model
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for recipe_name, steps in recipes.items():
        for step in steps:
            step_id = f"{recipe_name}_{step['name']}"
            start = model[step_vars[step_id]].as_long()
            end = start + step['duration']
            schedule.append({
                "recipe": recipe_name,
                "step": step['name'],
                "start_time": start,
                "end_time": end,
                "resources": [step['resource']]
            })
    
    # Calculate total time
    total_time_val = model[total_time].as_long()
    
    # Build resource usage summary
    resource_usage = {}
    for resource in resources:
        resource_usage[resource] = []
        for recipe_name, steps in recipes.items():
            for step in steps:
                if step['resource'] == resource:
                    step_id = f"{recipe_name}_{step['name']}"
                    start = model[step_vars[step_id]].as_long()
                    end = start + step['duration']
                    resource_usage[resource].append({
                        "start": start,
                        "end": end,
                        "recipe": recipe_name
                    })
        # Sort by start time
        resource_usage[resource].sort(key=lambda x: x['start'])
    
    # Print results
    print(f"total_time: {total_time_val}")
    print("schedule:")
    for s in schedule:
        print(f"  {s}")
    print("resource_usage:")
    for resource, intervals in resource_usage.items():
        print(f"  {resource}: {intervals}")
    
    # Verify expected optimal time
    if total_time_val == 35:
        print("✓ Optimal time matches expected 35 minutes")
    else:
        print(f"⚠ Total time {total_time_val} differs from expected 35 minutes")
        
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")