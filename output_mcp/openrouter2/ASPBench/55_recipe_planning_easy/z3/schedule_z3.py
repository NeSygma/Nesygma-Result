from z3 import *

# Define steps
steps = [
    ('pasta', 'prep', 10, 'prep_area'),
    ('pasta', 'boil', 15, 'stove'),
    ('pasta', 'serve', 5, 'prep_area'),
    ('salad', 'chop', 15, 'prep_area'),
    ('salad', 'mix', 5, 'prep_area'),
    ('bread', 'bake', 30, 'oven')
]

solver = Optimize()

# Create start time variables
start_vars = {}
end_vars = {}
for recipe, step, dur, res in steps:
    name = f"{recipe}_{step}_start"
    s = Int(name)
    start_vars[(recipe, step)] = s
    e = Int(f"{recipe}_{step}_end")
    end_vars[(recipe, step)] = e
    # duration constraint
    solver.add(e == s + dur)
    # non-negative start
    solver.add(s >= 0)

# Precedence constraints
# Pasta: prep -> boil -> serve
solver.add(end_vars[('pasta', 'prep')] <= start_vars[('pasta', 'boil')])
solver.add(end_vars[('pasta', 'boil')] <= start_vars[('pasta', 'serve')])
# Salad: chop -> mix
solver.add(end_vars[('salad', 'chop')] <= start_vars[('salad', 'mix')])

# Resource conflict constraints
# For each pair of steps sharing same resource, enforce non-overlap
for i in range(len(steps)):
    r1 = steps[i][3]
    for j in range(i+1, len(steps)):
        r2 = steps[j][3]
        if r1 == r2:
            s1 = start_vars[(steps[i][0], steps[i][1])]
            e1 = end_vars[(steps[i][0], steps[i][1])]
            s2 = start_vars[(steps[j][0], steps[j][1])]
            e2 = end_vars[(steps[j][0], steps[j][1])]
            solver.add(Or(e1 <= s2, e2 <= s1))

# Total time variable
max_end = Int('total_time')
solver.add(max_end >= 0)
for key in end_vars:
    solver.add(max_end >= end_vars[key])

# Objective: minimize total_time
solver.minimize(max_end)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    total_time_val = model[max_end].as_long()
    print("STATUS: sat")
    print("total_time =", total_time_val)
    print("schedule = [")
    for recipe, step, dur, res in steps:
        s_val = model[start_vars[(recipe, step)]].as_long()
        e_val = model[end_vars[(recipe, step)]].as_long()
        print(f"  {{'recipe': '{recipe}', 'step': '{step}', 'start_time': {s_val}, 'end_time': {e_val}, 'resources': ['{res}'] }},")
    print("]")
    # Resource usage summary
    resource_usage = {}
    for recipe, step, dur, res in steps:
        s_val = model[start_vars[(recipe, step)]].as_long()
        e_val = model[end_vars[(recipe, step)]].as_long()
        resource_usage.setdefault(res, []).append((s_val, e_val, recipe))
    print("resource_usage = {")
    for res, intervals in resource_usage.items():
        print(f"  '{res}': [")
        for (s_val, e_val, recipe) in intervals:
            print(f"    ({s_val}, {e_val}, '{recipe}'),")
        print("  ],")
    print("}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")