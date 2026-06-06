from z3 import *

# Define tasks with durations and resources
tasks = [
    ('preheat_oven', 10, 'oven'),
    ('prep_chicken', 15, 'prep_area'),
    ('bake_chicken', 50, 'oven'),
    ('rest_chicken', 10, 'prep_area'),
    ('chop_veg_soup', 20, 'prep_area'),
    ('simmer_stock', 30, 'stove'),
    ('chop_onion', 5, 'prep_area'),
    ('cook_risotto', 25, 'stove'),
    ('wash_greens', 5, 'prep_area'),
    ('mix_dressing', 10, 'prep_area'),
]

# Create start time Int variables for each task
starts = {name: Int(f'start_{name}') for name, _, _ in tasks}
ends = {name: Int(f'end_{name}') for name, _, _ in tasks}

opt = Optimize()

# Add basic constraints: start >= 0, end = start + duration
for name, dur, _ in tasks:
    opt.add(starts[name] >= 0)
    opt.add(ends[name] == starts[name] + dur)

# Precedences within recipes
precedences = [
    ('prep_chicken', 'bake_chicken'),
    ('bake_chicken', 'rest_chicken'),
    ('chop_veg_soup', 'simmer_stock'),
    ('chop_onion', 'cook_risotto'),
    ('wash_greens', 'mix_dressing'),
    # oven preheat before baking
    ('preheat_oven', 'bake_chicken'),
    # inter-recipe dependency
    ('simmer_stock', 'cook_risotto'),
]
for a, b in precedences:
    opt.add(ends[a] <= starts[b])

# Resource capacity constraints
# Oven (capacity 1) tasks: preheat_oven, bake_chicken
oven_tasks = ['preheat_oven', 'bake_chicken']
for i in range(len(oven_tasks)):
    for j in range(i+1, len(oven_tasks)):
        t1 = oven_tasks[i]
        t2 = oven_tasks[j]
        opt.add(Or(ends[t1] <= starts[t2], ends[t2] <= starts[t1]))

# Stove (capacity 1) tasks: simmer_stock, cook_risotto
stove_tasks = ['simmer_stock', 'cook_risotto']
for i in range(len(stove_tasks)):
    for j in range(i+1, len(stove_tasks)):
        t1 = stove_tasks[i]
        t2 = stove_tasks[j]
        opt.add(Or(ends[t1] <= starts[t2], ends[t2] <= starts[t1]))

# Prep area (capacity 2) tasks
prep_tasks = [name for name, _, res in tasks if res == 'prep_area']
# We'll bound makespan to an upper limit for minute iteration
MAX_TIME = 200
# For each minute, sum of active prep tasks <= 2
for t in range(MAX_TIME):
    active = []
    for name in prep_tasks:
        # Bool: task is active at minute t if start <= t < end
        active.append(If(And(starts[name] <= t, t < ends[name]), 1, 0))
    opt.add(Sum(active) <= 2)

# Define total_time variable
total_time = Int('total_time')
opt.add(total_time >= 0)
for name in starts:
    opt.add(total_time >= ends[name])

# Objective: minimize total_time
opt.minimize(total_time)

# Solve
if opt.check() == sat:
    m = opt.model()
    print('STATUS: sat')
    print('total_time =', m[total_time].as_long())
    # Print schedule
    for name, _, _ in tasks:
        s = m[starts[name]].as_long()
        e = m[ends[name]].as_long()
        print(f'{name}: start={s}, end={e}')
else:
    print('STATUS: unsat')