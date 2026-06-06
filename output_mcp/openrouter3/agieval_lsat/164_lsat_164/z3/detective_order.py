from z3 import *

# Declare position variables for each person
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

solver = Solver()

# Base constraints
# All positions are between 1 and 7
solver.add(Peters >= 1, Peters <= 7)
solver.add(Quinn >= 1, Quinn <= 7)
solver.add(Rovero >= 1, Rovero <= 7)
solver.add(Stanton >= 1, Stanton <= 7)
solver.add(Tao >= 1, Tao <= 7)
solver.add(Villas >= 1, Villas <= 7)
solver.add(White >= 1, White <= 7)

# All positions are distinct
solver.add(Distinct([Peters, Quinn, Rovero, Stanton, Tao, Villas, White]))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(Stanton == Tao - 1, Stanton == Tao + 1)))

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Quinn < Rovero)

# Constraint 3: Villas was recruited immediately before White
solver.add(Villas == White - 1)

# Constraint 4: Peters was recruited fourth
solver.add(Peters == 4)

# Constraint 5: Tao was recruited second (given condition)
solver.add(Tao == 2)

# Define options as constraints
opt_a_constr = (Quinn == 3)
opt_b_constr = (Rovero == 5)
opt_c_constr = (Stanton == 6)
opt_d_constr = (Villas == 6)
opt_e_constr = (White == 3)

# Test each option using the required skeleton
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