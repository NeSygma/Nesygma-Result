from z3 import *

opt = Optimize()

# Define steps with (recipe, step_name, duration, resource)
steps = [
    ("pasta", "prep",   10, "prep_area"),
    ("pasta", "boil",   15, "stove"),
    ("pasta", "serve",   5, "prep_area"),
    ("salad", "chop",   15, "prep_area"),
    ("salad", "mix",     5, "prep_area"),
    ("bread", "bake",   30, "oven"),
]

# Create start and end time variables for each step
start = {}
end = {}
for (recipe, step_name, dur, res) in steps:
    s = Int(f's_{recipe}_{step_name}')
    e = Int(f'e_{recipe}_{step_name}')
    start[(recipe, step_name)] = s
    end[(recipe, step_name)] = e
    # Non-negative times
    opt.add(s >= 0)
    # Correct duration
    opt.add(e == s + dur)

# Precedence constraints within recipes
# Pasta: prep -> boil -> serve
opt.add(end[("pasta", "prep")] <= start[("pasta", "boil")])
opt.add(end[("pasta", "boil")] <= start[("pasta", "serve")])
# Salad: chop -> mix
opt.add(end[("salad", "chop")] <= start[("salad", "mix")])
# Bread: no internal dependencies

# Resource conflict constraints: steps sharing a resource must not overlap
# Group steps by resource
from collections import defaultdict
resource_steps = defaultdict(list)
for (recipe, step_name, dur, res) in steps:
    resource_steps[res].append((recipe, step_name))

for res, rsteps in resource_steps.items():
    for i in range(len(rsteps)):
        for j in range(i+1, len(rsteps)):
            r1, s1 = rsteps[i]
            r2, s2 = rsteps[j]
            # Either step i finishes before step j starts, or vice versa
            opt.add(Or(
                end[(r1, s1)] <= start[(r2, s2)],
                end[(r2, s2)] <= start[(r1, s1)]
            ))

# Objective: minimize total completion time (max end time)
total_time = Int('total_time')
for (recipe, step_name, dur, res) in steps:
    opt.add(total_time >= end[(recipe, step_name)])

opt.minimize(total_time)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    tt = m[total_time].as_long()
    print("STATUS: sat")
    print(f"total_time = {tt}")
    print()
    print("Schedule:")
    schedule_list = []
    for (recipe, step_name, dur, res) in steps:
        s_val = m[start[(recipe, step_name)]].as_long()
        e_val = m[end[(recipe, step_name)]].as_long()
        schedule_list.append((recipe, step_name, s_val, e_val, res))
        print(f"  {recipe}.{step_name}: start={s_val}, end={e_val}, resource={res}")

    # Sort by start time for clarity
    schedule_list.sort(key=lambda x: (x[2], x[0], x[1]))

    print()
    print("Timeline (sorted by start time):")
    for (recipe, step_name, s_val, e_val, res) in schedule_list:
        print(f"  t={s_val:3d}-{e_val:3d}: {recipe}.{step_name} ({res})")

    print()
    print("Resource usage:")
    resource_usage = defaultdict(list)
    for (recipe, step_name, s_val, e_val, res) in schedule_list:
        resource_usage[res].append((s_val, e_val, recipe))
    for res in sorted(resource_usage.keys()):
        intervals = sorted(resource_usage[res])
        print(f"  {res}: {intervals}")

    # Verify optimality
    print()
    print(f"Optimal total time: {tt} minutes")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")