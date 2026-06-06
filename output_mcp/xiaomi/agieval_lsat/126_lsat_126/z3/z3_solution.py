from z3 import *

solver = Solver()

# Boolean variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# At least four employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Given: Paine is NOT on the team
solver.add(Not(Paine))

# Define option constraints
# (A) Neither Myers nor Ortega is on the team
opt_a_constr = And(Not(Myers), Not(Ortega))

# (B) Neither Myers nor Thomson is on the team
opt_b_constr = And(Not(Myers), Not(Thomson))

# (C) Neither Myers nor Zayre is on the team
opt_c_constr = And(Not(Myers), Not(Zayre))

# (D) Neither Ortega nor Thomson is on the team
opt_d_constr = And(Not(Ortega), Not(Thomson))

# (E) Neither Ortega nor Yoder is on the team
opt_e_constr = And(Not(Ortega), Not(Yoder))

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