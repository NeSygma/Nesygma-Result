from z3 import *

solver = Solver()

# Define constants (as ints)
g = 0
h = 1
i = 2
k = 3
l = 4
n = 5
o = 6
r = 7

# Slot variables
mm = Int('mm')
ma = Int('ma')
tm = Int('tm')
ta = Int('ta')
wm = Int('wm')
wa = Int('wa')

# All-different
solver.add(Distinct([mm, ma, tm, ta, wm, wa]))

# Fixed assignments (the refined model)
solver.add(mm == k)   # Monday morning = Kyle
solver.add(tm == h)   # Tuesday morning = Helen
solver.add(wm == l)   # Wednesday morning = Lenore
solver.add(ma == i)   # Monday afternoon = Irving
solver.add(ta == g)   # Tuesday afternoon = George
solver.add(wa == n)   # Wednesday afternoon = Nina

# Additional constraints to enforce problem conditions (optional)
# George only on Tuesday
solver.add(mm != g, ma != g, wm != g, wa != g)
# Olivia and Robert cannot be in afternoon
solver.add(ma != o, ta != o, wa != o)
solver.add(ma != r, ta != r, wa != r)

# Define option constraints
opt_a_constr = (mm == h)  # Helen gives a report on Monday
opt_b_constr = Or(mm == i, ma == i)  # Irving gives a report on Monday
opt_c_constr = Or(wm == i, wa == i)  # Irving gives a report on Wednesday
opt_d_constr = Or(tm == k, ta == k)  # Kyle gives a report on Tuesday
opt_e_constr = Or(wm == k, wa == k)  # Kyle gives a report on Wednesday

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")