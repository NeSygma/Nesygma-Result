from z3 import *

# Define tasks: (name, duration, resource)
tasks = [
    ('preheat_oven', 10, 'oven'),
    ('roast_prep', 15, 'prep_area'),
    ('roast_bake', 50, 'oven'),
    ('roast_rest', 10, 'prep_area'),
    ('veg_chop', 20, 'prep_area'),
    ('veg_simmer', 30, 'stove'),
    ('risotto_chop', 5, 'prep_area'),
    ('risotto_cook', 25, 'stove'),
    ('salad_wash', 5, 'prep_area'),
    ('salad_mix', 10, 'prep_area')
]

# Resource capacities
capacities = {
    'prep_area': 2,
    'oven': 1,
    'stove': 1
}

num_tasks = len(tasks)

# Create solver
opt = Optimize()

# Variables for start and end times
start = [Int(f'start_{i}') for i in range(num_tasks)]
end = [Int(f'end_{i}') for i in range(num_tasks)]

# Makespan variable
makespan = Int('makespan')

# Domain bounds
MAX_TIME = 200
for i in range(num_tasks):
    opt.add(start[i] >= 0)
    opt.add(start[i] <= MAX_TIME)
    opt.add(end[i] == start[i] + tasks[i][1])
    opt.add(end[i] <= makespan)

# Makespan bounds
opt.add(makespan >= 0)
opt.add(makespan <= MAX_TIME)

# Precedence constraints within recipes
# Map task names to indices for convenience
name_to_idx = {name: idx for idx, (name, _, _) in enumerate(tasks)}

# Roast Chicken: prep -> bake -> rest
opt.add(end[name_to_idx['roast_prep']] <= start[name_to_idx['roast_bake']])
opt.add(end[name_to_idx['roast_bake']] <= start[name_to_idx['roast_rest']])
# Vegetable Soup: chop -> simmer
opt.add(end[name_to_idx['veg_chop']] <= start[name_to_idx['veg_simmer']])
# Risotto: chop -> cook
opt.add(end[name_to_idx['risotto_chop']] <= start[name_to_idx['risotto_cook']])
# Side Salad: wash -> mix
opt.add(end[name_to_idx['salad_wash']] <= start[name_to_idx['salad_mix']])
# Inter-recipe: simmer_stock -> cook_risotto
opt.add(end[name_to_idx['veg_simmer']] <= start[name_to_idx['risotto_cook']])
# Oven preheat before any baking (roast_bake)
opt.add(end[name_to_idx['preheat_oven']] <= start[name_to_idx['roast_bake']])

# Resource capacity constraints
# For resources with capacity 1, enforce pairwise non-overlap
# Oven: preheat_oven and roast_bake
opt.add(Or(end[name_to_idx['preheat_oven']] <= start[name_to_idx['roast_bake']],
           end[name_to_idx['roast_bake']] <= start[name_to_idx['preheat_oven']]))
# Stove: veg_simmer and risotto_cook
opt.add(Or(end[name_to_idx['veg_simmer']] <= start[name_to_idx['risotto_cook']],
           end[name_to_idx['risotto_cook']] <= start[name_to_idx['veg_simmer']]))

# For prep_area capacity 2, use cumulative constraint over time points
prep_indices = [i for i, (_, _, res) in enumerate(tasks) if res == 'prep_area']
for t in range(MAX_TIME):
    active = [If(And(start[i] <= t, t < end[i]), 1, 0) for i in prep_indices]
    opt.add(Sum(active) <= capacities['prep_area'])

# Objective: minimize makespan
opt.minimize(makespan)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract schedule
    schedule = []
    for i, (name, dur, res) in enumerate(tasks):
        s = m[start[i]].as_long()
        e = m[end[i]].as_long()
        schedule.append((s, name, e, res))
    schedule.sort()  # sort by start time
    total_time = m[makespan].as_long()
    print("STATUS: sat")
    print(f"total_time={total_time}")
    print("schedule:")
    for s, name, e, res in schedule:
        print(f"task: {name}, start: {s}, end: {e}, resource: {res}")
    print("feasible: True")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")