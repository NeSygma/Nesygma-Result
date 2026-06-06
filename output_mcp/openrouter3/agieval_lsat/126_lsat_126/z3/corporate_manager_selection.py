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

# Create solver
solver = Solver()

# Base constraints
# 1. Team size at least 4
team_size = Sum([If(Myers, 1, 0), If(Ortega, 1, 0), If(Paine, 1, 0), 
                 If(Schmidt, 1, 0), If(Thomson, 1, 0), If(Wong, 1, 0), 
                 If(Yoder, 1, 0), If(Zayre, 1, 0)])
solver.add(team_size >= 4)

# 2. If Myers is on team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# 3. If Schmidt is on team, both Paine and Thomson must be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# 4. If Wong is on team, both Myers and Yoder must be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Additional condition: Paine is NOT on the team
solver.add(Not(Paine))

# Define answer choice constraints
opt_a_constr = And(Not(Myers), Not(Ortega))
opt_b_constr = And(Not(Myers), Not(Thomson))
opt_c_constr = And(Not(Myers), Not(Zayre))
opt_d_constr = And(Not(Ortega), Not(Thomson))
opt_e_constr = And(Not(Ortega), Not(Yoder))

# Evaluate each option using the exact skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
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