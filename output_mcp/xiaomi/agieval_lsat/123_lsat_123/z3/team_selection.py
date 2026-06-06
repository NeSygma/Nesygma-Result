from z3 import *

solver = Solver()

# Declare Boolean variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# Base constraints from the problem
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(Wong, And(Myers, Yoder)))

# Define constraints for each answer choice
# Each choice specifies exactly those employees are on the team (others are not)
# A: Myers, Paine, Schmidt, Thomson
opt_a = And(Myers, Paine, Schmidt, Thomson, Not(Ortega), Not(Wong), Not(Yoder), Not(Zayre))

# B: Ortega, Paine, Thomson, Zayre
opt_b = And(Ortega, Paine, Thomson, Zayre, Not(Myers), Not(Schmidt), Not(Wong), Not(Yoder))

# C: Paine, Schmidt, Yoder, Zayre
opt_c = And(Paine, Schmidt, Yoder, Zayre, Not(Myers), Not(Ortega), Not(Thomson), Not(Wong))

# D: Schmidt, Thomson, Yoder, Zayre
opt_d = And(Schmidt, Thomson, Yoder, Zayre, Not(Myers), Not(Ortega), Not(Paine), Not(Wong))

# E: Thomson, Wong, Yoder, Zayre
opt_e = And(Thomson, Wong, Yoder, Zayre, Not(Myers), Not(Ortega), Not(Paine), Not(Schmidt))

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