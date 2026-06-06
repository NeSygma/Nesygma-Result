from z3 import *

solver = Solver()

# Boolean variables: True means on the team
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

members = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# Constraint: At least 4 employees on the team
solver.add(Sum([If(m, 1, 0) for m in members]) >= 4)

# Constraint 1: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Constraint 2: If Schmidt is on the team, both Paine and Thomson must be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Constraint 3: If Wong is on the team, both Myers and Yoder must be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Given: Paine is NOT on the team
solver.add(Not(Paine))

# From constraint 2: If Schmidt is on team, Paine must be. Paine is not, so Schmidt is not.
solver.add(Not(Schmidt))

# Define option constraints
# A) Neither Myers nor Ortega is on the team
opt_a = And(Not(Myers), Not(Ortega))
# B) Neither Myers nor Thomson is on the team
opt_b = And(Not(Myers), Not(Thomson))
# C) Neither Myers nor Zayre is on the team
opt_c = And(Not(Myers), Not(Zayre))
# D) Neither Ortega nor Thomson is on the team
opt_d = And(Not(Ortega), Not(Thomson))
# E) Neither Ortega nor Yoder is on the team
opt_e = And(Not(Ortega), Not(Yoder))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: Myers={m[Myers]}, Ortega={m[Ortega]}, Paine={m[Paine]}, Schmidt={m[Schmidt]}, Thomson={m[Thomson]}, Wong={m[Wong]}, Yoder={m[Yoder]}, Zayre={m[Zayre]}")
    else:
        print(f"Option {letter} is UNSAT")
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