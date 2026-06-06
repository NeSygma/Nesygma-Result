from z3 import *

# Define solver and variables
solver = Solver()
people = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']
pos = {p: Int(p) for p in people}

# Domain constraints: positions 1..7
for p in people:
    solver.add(pos[p] >= 1, pos[p] <= 7)

# All distinct positions
solver.add(Distinct([pos[p] for p in people]))

# Base constraints
solver.add(pos['Peters'] == 4)               # Peters fourth
solver.add(pos['Villas'] + 1 == pos['White'])  # Villas immediately before White
solver.add(pos['Quinn'] < pos['Rovero'])     # Quinn earlier than Rovero
solver.add(pos['Tao'] == 2)                  # Tao second (given condition)
# Stanton not immediately before nor after Tao
solver.add(pos['Stanton'] != pos['Tao'] - 1)
solver.add(pos['Stanton'] != pos['Tao'] + 1)

# Define option constraints
opt_a_constr = pos['Quinn'] == 3
opt_b_constr = pos['Rovero'] == 5
opt_c_constr = pos['Stanton'] == 6
opt_d_constr = pos['Villas'] == 6
opt_e_constr = pos['White'] == 3

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