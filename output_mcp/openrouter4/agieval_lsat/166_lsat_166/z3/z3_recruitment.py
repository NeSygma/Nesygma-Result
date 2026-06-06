from z3 import *

solver = Solver()

# Define positions 1-7 for each person
persons = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']
# Position variables
pos = {p: Int(f'pos_{p}') for p in persons}

# Domain: each position between 1 and 7
for p in persons:
    solver.add(pos[p] >= 1, pos[p] <= 7)

# All positions are distinct
solver.add(Distinct(list(pos.values())))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao.
# |pos(Stanton) - pos(Tao)| != 1
solver.add(Not(Or(pos['Stanton'] + 1 == pos['Tao'], pos['Stanton'] - 1 == pos['Tao'])))

# Constraint 2: Quinn was recruited earlier than Rovero.
solver.add(pos['Quinn'] < pos['Rovero'])

# Constraint 3: Villas was recruited immediately before White.
solver.add(pos['Villas'] + 1 == pos['White'])

# Constraint 4: Peters was recruited fourth.
solver.add(pos['Peters'] == 4)

# Additional constraints for the scenario:
# White was recruited earlier than Rovero
solver.add(pos['White'] < pos['Rovero'])
# Rovero was recruited earlier than Tao
solver.add(pos['Rovero'] < pos['Tao'])

# Now test each option
# (A) Quinn was recruited first.
opt_a = (pos['Quinn'] == 1)
# (B) Rovero was recruited third.
opt_b = (pos['Rovero'] == 3)
# (C) Stanton was recruited second.
opt_c = (pos['Stanton'] == 2)
# (D) Tao was recruited sixth.
opt_d = (pos['Tao'] == 6)
# (E) Villas was recruited sixth.
opt_e = (pos['Villas'] == 6)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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