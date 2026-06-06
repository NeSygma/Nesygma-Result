from z3 import *

solver = Solver()

# Names of accomplices
names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']
pos = {name: Int(name) for name in names}

# Base constraints
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct([pos[name] for name in names]))

solver.add(pos['Peters'] == 4)                     # Peters was recruited fourth
solver.add(pos['Quinn'] < pos['Rovero'])           # Quinn earlier than Rovero
solver.add(Not(Or(pos['Stanton'] == pos['Tao'] + 1,
                  pos['Stanton'] == pos['Tao'] - 1)))  # Stanton not immediately before/after Tao
solver.add(pos['Villas'] + 1 == pos['White'])      # Villas immediately before White

# Option constraints
opt_a_constr = And(pos['Quinn'] == 2,
                   pos['Stanton'] == 3,
                   pos['Peters'] == 4,
                   pos['Tao'] == 5,
                   pos['Villas'] == 6)

opt_b_constr = And(pos['Quinn'] == 2,
                   pos['Stanton'] == 3,
                   pos['Peters'] == 4,
                   pos['Tao'] == 5,
                   pos['White'] == 6)

opt_c_constr = And(pos['Villas'] == 2,
                   pos['White'] == 3,
                   pos['Peters'] == 4,
                   pos['Quinn'] == 5,
                   pos['Stanton'] == 6)

opt_d_constr = And(pos['Villas'] == 2,
                   pos['White'] == 3,
                   pos['Peters'] == 4,
                   pos['Rovero'] == 5,
                   pos['Stanton'] == 6)

opt_e_constr = And(pos['Villas'] == 2,
                   pos['White'] == 3,
                   pos['Quinn'] == 4,
                   pos['Rovero'] == 5,
                   pos['Stanton'] == 6)

# Evaluate each option
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