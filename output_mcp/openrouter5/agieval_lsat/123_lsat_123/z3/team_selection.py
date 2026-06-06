from z3 import *

# Define boolean variables for each employee
Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre = Bools('Myers Ortega Paine Schmidt Thomson Wong Yoder Zayre')
employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

solver = Solver()

# At least four employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(Myers, Not(Ortega)))
solver.add(Implies(Myers, Not(Paine)))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(Schmidt, Paine))
solver.add(Implies(Schmidt, Thomson))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(Wong, Myers))
solver.add(Implies(Wong, Yoder))

# Define each option's constraint
opt_a = And(Myers, Paine, Schmidt, Thomson)
opt_b = And(Ortega, Paine, Thomson, Zayre)
opt_c = And(Paine, Schmidt, Yoder, Zayre)
opt_d = And(Schmidt, Thomson, Yoder, Zayre)
opt_e = And(Thomson, Wong, Yoder, Zayre)

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