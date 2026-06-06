from z3 import *

# Define the accomplices
accomplices = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# Create position variables for each accomplice (1-7)
pos = {a: Int(f'pos_{a}') for a in accomplices}

solver = Solver()

# Each accomplice has a unique position from 1 to 7
for a in accomplices:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in accomplices]))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(And(
    pos['Stanton'] != pos['Tao'] + 1,
    pos['Stanton'] != pos['Tao'] - 1
))

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(pos['Quinn'] < pos['Rovero'])

# Constraint 3: Villas was recruited immediately before White
solver.add(pos['Villas'] + 1 == pos['White'])

# Constraint 4: Peters was recruited fourth
solver.add(pos['Peters'] == 4)

# Define the order constraints for each option
# Option A: Quinn, Tao, Stanton, Peters, Villas, White, Rovero
opt_a_constr = And(
    pos['Quinn'] == 1,
    pos['Tao'] == 2,
    pos['Stanton'] == 3,
    pos['Peters'] == 4,
    pos['Villas'] == 5,
    pos['White'] == 6,
    pos['Rovero'] == 7
)

# Option B: Quinn, White, Rovero, Peters, Stanton, Villas, Tao
opt_b_constr = And(
    pos['Quinn'] == 1,
    pos['White'] == 2,
    pos['Rovero'] == 3,
    pos['Peters'] == 4,
    pos['Stanton'] == 5,
    pos['Villas'] == 6,
    pos['Tao'] == 7
)

# Option C: Villas, White, Quinn, Stanton, Peters, Tao, Rovero
opt_c_constr = And(
    pos['Villas'] == 1,
    pos['White'] == 2,
    pos['Quinn'] == 3,
    pos['Stanton'] == 4,
    pos['Peters'] == 5,
    pos['Tao'] == 6,
    pos['Rovero'] == 7
)

# Option D: Villas, White, Stanton, Peters, Quinn, Tao, Rovero
opt_d_constr = And(
    pos['Villas'] == 1,
    pos['White'] == 2,
    pos['Stanton'] == 3,
    pos['Peters'] == 4,
    pos['Quinn'] == 5,
    pos['Tao'] == 6,
    pos['Rovero'] == 7
)

# Option E: Villas, White, Stanton, Peters, Rovero, Tao, Quinn
opt_e_constr = And(
    pos['Villas'] == 1,
    pos['White'] == 2,
    pos['Stanton'] == 3,
    pos['Peters'] == 4,
    pos['Rovero'] == 5,
    pos['Tao'] == 6,
    pos['Quinn'] == 7
)

# Test each option
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