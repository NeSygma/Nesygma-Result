from z3 import *

solver = Solver()

# Define positions for each person as Int variables
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]

# Domain constraints: positions 1..7 and all distinct
for p in people:
    solver.add(p >= 1, p <= 7)
solver.add(Distinct(people))

# Base constraints from problem
solver.add(Peters == 4)  # Peters was recruited fourth
solver.add(Villas + 1 == White)  # Villas immediately before White
solver.add(Quinn < Rovero)  # Quinn earlier than Rovero
# Stanton neither immediately before nor after Tao
solver.add(Not(Stanton + 1 == Tao))
solver.add(Not(Tao + 1 == Stanton))

# Additional premises for the question
solver.add(White < Rovero)  # White earlier than Rovero
solver.add(Rovero < Tao)    # Rovero earlier than Tao

# Define option constraints
opt_a_constr = Quinn == 1
opt_b_constr = Rovero == 3
opt_c_constr = Stanton == 2
opt_d_constr = Tao == 6
opt_e_constr = Villas == 6

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