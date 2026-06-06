from z3 import *

# Create solver
solver = Solver()

# Define employees as boolean variables (True = selected)
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

# Base constraints from problem statement
# 1. Team will include at least four employees
team_size = Sum([If(Myers, 1, 0), If(Ortega, 1, 0), If(Paine, 1, 0), 
                 If(Schmidt, 1, 0), If(Thomson, 1, 0), If(Wong, 1, 0), 
                 If(Yoder, 1, 0), If(Zayre, 1, 0)])
solver.add(team_size >= 4)

# 2. If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# 3. If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# 4. If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Define the answer choices as constraints
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

# Evaluate each option using the required skeleton
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