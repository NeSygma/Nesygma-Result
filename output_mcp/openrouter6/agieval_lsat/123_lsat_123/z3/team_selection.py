from z3 import *

# Declare Boolean variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

# Base constraints
solver = Solver()

# Constraint 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Or(Not(Myers), Not(Ortega)))
solver.add(Or(Not(Myers), Not(Paine)))

# Constraint 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Or(Not(Schmidt), Paine))
solver.add(Or(Not(Schmidt), Thomson))

# Constraint 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Or(Not(Wong), Myers))
solver.add(Or(Not(Wong), Yoder))

# Constraint: Team includes at least four employees
employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]
solver.add(Sum([If(emp, 1, 0) for emp in employees]) >= 4)

# Define the options as constraints that exactly those employees are selected
opt_a_constr = And(Myers, Paine, Schmidt, Thomson,
                   Not(Ortega), Not(Wong), Not(Yoder), Not(Zayre))
opt_b_constr = And(Ortega, Paine, Thomson, Zayre,
                   Not(Myers), Not(Schmidt), Not(Wong), Not(Yoder))
opt_c_constr = And(Paine, Schmidt, Yoder, Zayre,
                   Not(Myers), Not(Ortega), Not(Thomson), Not(Wong))
opt_d_constr = And(Schmidt, Thomson, Yoder, Zayre,
                   Not(Myers), Not(Ortega), Not(Paine), Not(Wong))
opt_e_constr = And(Thomson, Wong, Yoder, Zayre,
                   Not(Myers), Not(Ortega), Not(Paine), Not(Schmidt))

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