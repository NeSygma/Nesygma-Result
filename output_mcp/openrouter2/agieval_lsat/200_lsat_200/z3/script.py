from z3 import *
solver = Solver()

# declare variables
harmonica_day = Int('harmonica_day')
lamp_day = Int('lamp_day')
mirror_day = Int('mirror_day')
sundial_day = Int('sundial_day')
table_day = Int('table_day')
vase_day = Int('vase_day')

# domain constraints
for d in [harmonica_day, lamp_day, mirror_day, sundial_day, table_day, vase_day]:
    solver.add(d >= 1, d <= 6)

# distinct
solver.add(Distinct([harmonica_day, lamp_day, mirror_day, sundial_day, table_day, vase_day]))

# sundial not on June 1
solver.add(sundial_day != 1)

# If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Implies(harmonica_day < lamp_day, mirror_day < lamp_day))

# sundial earlier than mirror and vase
solver.add(sundial_day < mirror_day)
solver.add(sundial_day < vase_day)

# table earlier than harmonica or vase but not both
solver.add(Xor(table_day < harmonica_day, table_day < vase_day))

# option constraints
opt_a_constr = (mirror_day == 2)
opt_b_constr = (lamp_day == 2)
opt_c_constr = (vase_day == 2)
opt_d_constr = (lamp_day == 3)
opt_e_constr = (mirror_day == 5)

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