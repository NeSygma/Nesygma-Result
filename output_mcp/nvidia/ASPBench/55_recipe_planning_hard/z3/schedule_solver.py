from z3 import *

# Define durations
durations = {
    'prep_chicken': 15,
    'bake_chicken': 50,
    'rest_chicken': 10,
    'chop_veg_soup': 20,
    'simmer_stock': 30,
    'chop_onion': 5,
    'cook_risotto': 25,
    'wash_greens': 5,
    'mix_dressing': 10,
    'preheat_oven': 10
}

# Resource mapping
resource_of = {
    'prep_chicken': 'prep_area',
    'bake_chicken': 'oven',
    'rest_chicken': 'prep_area',
    'chop_veg_soup': 'prep_area',
    'simmer_stock': 'stove',
    'chop_onion': 'prep_area',
    'cook_risotto': 'stove',
    'wash_greens': 'prep_area',
    'mix_dressing': 'prep_area',
    'preheat_oven': 'oven'
}

# Capacity per resource
capacity = {'prep_area': 2, 'oven': 1, 'stove': 1}

# List of tasks
tasks = list(durations.keys())

# Create optimizer
opt = Optimize()

# Start variables
starts = {t: Int(f'start_{t}') for t in tasks}

# Makespan variable
makespan = Int('makespan')

# Upper bound for time horizon
MAX_TIME = 100

# Add basic constraints for each task
for t in tasks:
    # Non-negative start
    opt.add(starts[t] >= 0)
    # End time <= makespan
    end_expr = starts[t] + durations[t]
    opt.add(end_expr <= makespan)

# Precedence constraints
opt.add(starts['bake_chicken'] >= starts['prep_chicken'] + durations['prep_chicken'])
opt.add(starts['rest_chicken'] >= starts['bake_chicken'] + durations['bake_chicken'])
opt.add(starts['simmer_stock'] >= starts['chop_veg_soup'] + durations['chop_veg_soup'])
opt.add(starts['cook_risotto'] >= starts['chop_onion'] + durations['chop_onion'])
opt.add(starts['cook_risotto'] >= starts['simmer_stock'] + durations['simmer_stock'])
opt.add(starts['bake_chicken'] >= starts['preheat_oven'] + durations['preheat_oven'])

# Helper to add capacity constraints for a resource
def add_capacity(resource, tasks_list, cap):
    for tt in range(MAX_TIME):
        active = []
        for task in tasks_list:
            dur = durations[task]
            st = starts[task]
            # active if tt is within [start, start+dur)
            active.append(If(And(tt >= st, tt < st + dur), 1, 0))
        opt.add(Sum(active) <= cap)

# Add capacity constraints
add_capacity('prep_area', [t for t in tasks if resource_of[t] == 'prep_area'], capacity['prep_area'])
add_capacity('oven', [t for t in tasks if resource_of[t] == 'oven'], capacity['oven'])
add_capacity('stove', [t for t in tasks if resource_of[t] == 'stove'], capacity['stove'])

# Objective: minimize makespan
opt.minimize(makespan)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"total_time = {model[makespan].as_long()}")
    # Mapping task to recipe and step
    recipe_step = {
        'prep_chicken': ('Roast Chicken', 'prep_chicken'),
        'bake_chicken': ('Roast Chicken', 'bake_chicken'),
        'rest_chicken': ('Roast Chicken', 'rest_chicken'),
        'chop_veg_soup': ('Vegetable Soup', 'chop_veg_soup'),
        'simmer_stock': ('Vegetable Soup', 'simmer_stock'),
        'chop_onion': ('Risotto', 'chop_onion'),
        'cook_risotto': ('Risotto', 'cook_risotto'),
        'wash_greens': ('Side Salad', 'wash_greens'),
        'mix_dressing': ('Side Salad', 'mix_dressing'),
        'preheat_oven': ('Special', 'preheat_oven')
    }
    for t in tasks:
        st = model[starts[t]].as_long()
        end = st + durations[t]
        recipe, step = recipe_step[t]
        resource = resource_of[t]
        print(f"{recipe} {step} {st} {end} {resource}")
    print("feasible: True")
else:
    print("STATUS: unsat")