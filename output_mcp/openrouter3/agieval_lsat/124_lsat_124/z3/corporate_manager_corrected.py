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
employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]
team_size = Sum([If(emp, 1, 0) for emp in employees])
solver.add(team_size >= 4)

# 2. If Myers is on team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# 3. If Schmidt is on team, both Paine and Thomson must be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# 4. If Wong is on team, both Myers and Yoder must be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Define the answer choices as constraints that both employees are on team
opt_a_constr = And(Myers, Thomson)      # Myers and Thomson
opt_b_constr = And(Ortega, Yoder)       # Ortega and Yoder
opt_c_constr = And(Paine, Zayre)        # Paine and Zayre
opt_d_constr = And(Schmidt, Wong)       # Schmidt and Wong
opt_e_constr = And(Wong, Yoder)         # Wong and Yoder

# Evaluate each option: check if adding the pair makes the problem UNSATISFIABLE
# A pair CANNOT be together if adding it makes the problem UNSAT
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
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