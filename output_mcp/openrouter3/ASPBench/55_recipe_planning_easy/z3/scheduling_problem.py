from z3 import *

# Create optimizer
opt = Optimize()

# Define recipes and steps with durations and resources
recipes = {
    "pasta": [
        ("prep", 10, "prep_area"),
        ("boil", 15, "stove"),
        ("serve", 5, "prep_area")
    ],
    "salad": [
        ("chop", 15, "prep_area"),
        ("mix", 5, "prep_area")
    ],
    "bread": [
        ("bake", 30, "oven")
    ]
}

# Create symbolic variables for start times
start_times = {}
end_times = {}
durations = {}

for recipe, steps in recipes.items():
    for step, duration, resource in steps:
        step_id = f"{recipe}_{step}"
        start_times[step_id] = Int(f"start_{step_id}")
        end_times[step_id] = Int(f"end_{step_id}")
        durations[step_id] = duration
        # Add duration constraint: end = start + duration
        opt.add(end_times[step_id] == start_times[step_id] + duration)
        # Non-negative start time
        opt.add(start_times[step_id] >= 0)

# Precedence constraints
# Pasta: prep -> boil -> serve
opt.add(end_times["pasta_prep"] <= start_times["pasta_boil"])
opt.add(end_times["pasta_boil"] <= start_times["pasta_serve"])

# Salad: chop -> mix
opt.add(end_times["salad_chop"] <= start_times["salad_mix"])

# Bread: no internal dependencies

# Resource conflict constraints
# Group steps by resource
resources = {
    "oven": ["bread_bake"],
    "stove": ["pasta_boil"],
    "prep_area": ["pasta_prep", "pasta_serve", "salad_chop", "salad_mix"]
}

# For each resource, ensure no overlapping intervals
for resource, steps in resources.items():
    for i in range(len(steps)):
        for j in range(i+1, len(steps)):
            step1 = steps[i]
            step2 = steps[j]
            # Non-overlap: either step1 ends before step2 starts OR step2 ends before step1 starts
            opt.add(Or(
                end_times[step1] <= start_times[step2],
                end_times[step2] <= start_times[step1]
            ))

# Objective: minimize total completion time (max end time)
total_time = Int("total_time")
for step_id in end_times:
    opt.add(total_time >= end_times[step_id])
opt.minimize(total_time)

# Check and get model
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Calculate total time
    total_time_val = model.eval(total_time).as_long()
    print(f"total_time = {total_time_val}")
    
    # Build schedule
    schedule = []
    for recipe, steps in recipes.items():
        for step, duration, resource in steps:
            step_id = f"{recipe}_{step}"
            start_val = model.eval(start_times[step_id]).as_long()
            end_val = model.eval(end_times[step_id]).as_long()
            schedule.append({
                "recipe": recipe,
                "step": step,
                "start_time": start_val,
                "end_time": end_val,
                "resources": [resource]
            })
    
    print("schedule = [")
    for item in schedule:
        print(f"  {item},")
    print("]")
    
    # Build resource usage summary
    resource_usage = {}
    for resource, steps in resources.items():
        intervals = []
        for step_id in steps:
            start_val = model.eval(start_times[step_id]).as_long()
            end_val = model.eval(end_times[step_id]).as_long()
            # Find recipe for this step
            recipe_name = step_id.split("_")[0]
            intervals.append({
                "start": start_val,
                "end": end_val,
                "recipe": recipe_name
            })
        resource_usage[resource] = intervals
    
    print("resource_usage = {")
    for resource, intervals in resource_usage.items():
        print(f"  '{resource}': {intervals},")
    print("}")
    
    # Verify optimal time is 35 minutes
    if total_time_val == 35:
        print("Optimal schedule found: 35 minutes")
    else:
        print(f"Note: Found schedule with total time {total_time_val} minutes")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule exists")
else:
    print("STATUS: unknown")