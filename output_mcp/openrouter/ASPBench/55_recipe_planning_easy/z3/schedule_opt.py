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

# Create start time variables
starts = { (r,s): Int(f'start_{r}_{s}') for (r,s,_,_) in steps }
ends   = { (r,s): Int(f'end_{r}_{s}')   for (r,s,_,_) in steps }

opt = Optimize()

# Add duration constraints and non-negative start
for (r,s,dur,res) in steps:
    st = starts[(r,s)]
    en = ends[(r,s)]
    opt.add(st >= 0)
    opt.add(en == st + dur)

# Precedence constraints
# Pasta: prep -> boil -> serve
opt.add(ends[('pasta','prep')] <= starts[('pasta','boil')])
opt.add(ends[('pasta','boil')] <= starts[('pasta','serve')])
# Salad: chop -> mix
opt.add(ends[('salad','chop')] <= starts[('salad','mix')])
# Bread has none

# Resource conflict constraints: for each pair sharing same resource
for i in range(len(steps)):
    r1,s1,d1,res1 = steps[i]
    for j in range(i+1, len(steps)):
        r2,s2,d2,res2 = steps[j]
        if res1 == res2:
            # enforce non-overlap
            opt.add(Or(ends[(r1,s1)] <= starts[(r2,s2)], ends[(r2,s2)] <= starts[(r1,s1)]))

# Define total_time as max end
total_time = Int('total_time')
opt.add(total_time >= 0)
for (r,s,_,_) in steps:
    opt.add(total_time >= ends[(r,s)])

# Minimize total_time
opt.minimize(total_time)

result = opt.check()
if result == sat:
    m = opt.model()
    print('STATUS: sat')
    print('total_time =', m[total_time].as_long())
    # Print schedule
    for (r,s,_,res) in steps:
        st = m[starts[(r,s)]].as_long()
        en = m[ends[(r,s)]].as_long()
        print(f"recipe: {r}, step: {s}, start_time: {st}, end_time: {en}, resources: [{res}]")
else:
    print('STATUS: unsat')