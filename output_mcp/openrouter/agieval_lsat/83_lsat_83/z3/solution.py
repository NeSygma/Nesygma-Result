from z3 import *

# Declare variables for each representative
people = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']
vars = {p: Int(p) for p in people}
solver = Solver()
# Domain constraints: each in {1,2,3}
for v in vars.values():
    solver.add(v >= 1, v <= 3)
# Parra and Quinn same zone
solver.add(vars['Parra'] == vars['Quinn'])
# Stuckey and Udall same zone
solver.add(vars['Stuckey'] == vars['Udall'])
# Either Parra or Tiao (but not both) works in Zone1
solver.add(Xor(vars['Parra'] == 1, vars['Tiao'] == 1))
# Either Tiao or Udall (but not both) works in Zone2
solver.add(Xor(vars['Tiao'] == 2, vars['Udall'] == 2))
# More reps in Zone3 than Zone2
cnt2 = Sum([If(v == 2, 1, 0) for v in vars.values()])
cnt3 = Sum([If(v == 3, 1, 0) for v in vars.values()])
solver.add(cnt3 > cnt2)
# Additional condition: more reps in Zone1 than Zone3
cnt1 = Sum([If(v == 1, 1, 0) for v in vars.values()])
solver.add(cnt1 > cnt3)

# Define option constraints
opt_a = vars['Kim'] == 2
opt_b = vars['Mahr'] == 2
opt_c = vars['Parra'] == 3
opt_d = vars['Tiao'] == 1
opt_e = vars['Udall'] == 3

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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