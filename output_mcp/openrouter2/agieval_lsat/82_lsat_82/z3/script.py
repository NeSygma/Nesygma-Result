from z3 import *

solver = Solver()
# Define reps
reps = ['Kim','Mahr','Parra','Quinn','Stuckey','Tiao','Udall']
rep_vars = {name: Int(name) for name in reps}
# Domain constraints
for v in rep_vars.values():
    solver.add(v >= 1, v <= 3)
# Base constraints
# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(rep_vars['Parra'] == 1, rep_vars['Tiao'] == 1))
# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(rep_vars['Tiao'] == 2, rep_vars['Udall'] == 2))
# Parra and Quinn work in the same sales zone
solver.add(rep_vars['Parra'] == rep_vars['Quinn'])
# Stuckey and Udall work in the same sales zone
solver.add(rep_vars['Stuckey'] == rep_vars['Udall'])
# More reps in Zone 3 than in Zone 2
zone3_count = Sum([If(rep_vars[r] == 3, 1, 0) for r in reps])
zone2_count = Sum([If(rep_vars[r] == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Define option constraints
opt_a_constr = And(
    rep_vars['Kim'] == 1,
    rep_vars['Parra'] == 1,
    rep_vars['Stuckey'] == 2,
    rep_vars['Udall'] == 2,
    rep_vars['Mahr'] == 3,
    rep_vars['Quinn'] == 3,
    rep_vars['Tiao'] == 3
)
opt_b_constr = And(
    rep_vars['Kim'] == 1,
    rep_vars['Tiao'] == 1,
    rep_vars['Stuckey'] == 2,
    rep_vars['Udall'] == 2,
    rep_vars['Mahr'] == 3,
    rep_vars['Parra'] == 3,
    rep_vars['Quinn'] == 3
)
opt_c_constr = And(
    rep_vars['Parra'] == 1,
    rep_vars['Quinn'] == 1,
    rep_vars['Kim'] == 2,
    rep_vars['Udall'] == 2,
    rep_vars['Mahr'] == 3,
    rep_vars['Stuckey'] == 3,
    rep_vars['Tiao'] == 3
)
opt_d_constr = And(
    rep_vars['Stuckey'] == 1,
    rep_vars['Udall'] == 1,
    rep_vars['Kim'] == 2,
    rep_vars['Tiao'] == 2,
    rep_vars['Mahr'] == 3,
    rep_vars['Parra'] == 3,
    rep_vars['Quinn'] == 3
)
opt_e_constr = And(
    rep_vars['Tiao'] == 1,
    rep_vars['Kim'] == 2,
    rep_vars['Parra'] == 2,
    rep_vars['Quinn'] == 2,
    rep_vars['Stuckey'] == 3,
    rep_vars['Udall'] == 3
)

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