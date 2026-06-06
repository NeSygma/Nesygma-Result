from z3 import *

# BENCHMARK_MODE: ON (model-finding)
BENCHMARK_MODE = True

# Declare symbolic variables for time points
# We will model each step as a start and end time
# Total time is the maximum end time across all steps

# Recipes and their steps
recipes = {
    "pasta": ["prep", "boil", "serve"],
    "salad": ["chop", "mix"],
    "bread": ["bake"]
}

# Step durations and resources
step_info = {
    ("pasta", "prep"): (10, ["prep_area"]),
    ("pasta", "boil"): (15, ["stove"]),
    ("pasta", "serve"): (5, ["prep_area"]),
    ("salad", "chop"): (15, ["prep_area"]),
    ("salad", "mix"): (5, ["prep_area"]),
    ("bread", "bake"): (30, ["oven"])
}

# Precedence constraints within recipes
precedence = {
    ("pasta", "prep"): [("pasta", "boil")],
    ("pasta", "boil"): [("pasta", "serve")],
    ("salad", "chop"): [("salad", "mix")],
    ("bread", "bake"): []
}

# Resources
resources = ["oven", "stove", "prep_area"]

# Create start and end times for each step
start_times = {}
end_times = {}
for recipe, steps in recipes.items():
    for step in steps:
        start_times[(recipe, step)] = Int(f"start_{recipe}_{step}")
        end_times[(recipe, step)] = Int(f"end_{recipe}_{step}")

# Total time is the maximum end time
total_time = Int("total_time")
solver = Optimize()

# Objective: minimize total_time
solver.minimize(total_time)

# Constraints

# 1. All steps must be scheduled: start and end times must be defined and end >= start
for recipe, steps in recipes.items():
    for step in steps:
        solver.add(start_times[(recipe, step)] >= 0)
        solver.add(end_times[(recipe, step)] == start_times[(recipe, step)] + step_info[(recipe, step)][0])
        solver.add(end_times[(recipe, step)] <= total_time)

# 2. Precedence constraints within recipes
for recipe, steps in recipes.items():
    for step in steps:
        if (recipe, step) in precedence:
            for next_step in precedence[(recipe, step)]:
                solver.add(end_times[(recipe, step)] <= start_times[next_step])

# 3. No resource conflicts: same resource cannot be used by multiple steps at overlapping times
for resource in resources:
    # Collect all steps that use this resource
    steps_using_resource = []
    for recipe, steps in recipes.items():
        for step in steps:
            if resource in step_info[(recipe, step)][1]:
                steps_using_resource.append((recipe, step))

    # For each pair of steps using the same resource, ensure no overlap
    for i in range(len(steps_using_resource)):
        for j in range(i + 1, len(steps_using_resource)):
            r1, s1 = steps_using_resource[i]
            r2, s2 = steps_using_resource[j]
            # Either step1 finishes before step2 starts, or step2 finishes before step1 starts
            solver.add(Or(
                end_times[(r1, s1)] <= start_times[(r2, s2)],
                end_times[(r2, s2)] <= start_times[(r1, s1)]
            ))

# 4. Correct durations and non-negative times are already handled above

# Check and print result
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("total_time =", model[total_time])

    # Extract schedule
    schedule = []
    for recipe, steps in recipes.items():
        for step in steps:
            start = model[start_times[(recipe, step)]]
            end = model[end_times[(recipe, step)]]
            resources_used = step_info[(recipe, step)][1]
            schedule.append({
                "recipe": recipe,
                "step": step,
                "start_time": start,
                "end_time": end,
                "resources": resources_used
            })
    print("schedule =", schedule)

    # Extract resource usage
    resource_usage = {}
    for resource in resources:
        usage = []
        for recipe, steps in recipes.items():
            for step in steps:
                if resource in step_info[(recipe, step)][1]:
                    start = model[start_times[(recipe, step)]]
                    end = model[end_times[(recipe, step)]]
                    usage.append({
                        "start": start,
                        "end": end,
                        "recipe": recipe
                    })
        resource_usage[resource] = usage
    print("resource_usage =", resource_usage)

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")