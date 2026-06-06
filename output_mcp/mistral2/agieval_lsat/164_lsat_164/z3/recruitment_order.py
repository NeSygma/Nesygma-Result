from z3 import *

# Create a solver instance
solver = Solver()

# Declare symbolic variables for each accomplice's position
# Positions are 1 through 7
peters = Int('peters')
quinn = Int('quinn')
rovero = Int('rovero')
stanton = Int('stanton')
tao = Int('tao')
villas = Int('villas')
white = Int('white')

# All positions are between 1 and 7 and distinct
positions = [peters, quinn, rovero, stanton, tao, villas, white]
solver.add(Distinct(positions))
for pos in positions:
    solver.add(pos >= 1, pos <= 7)

# Given constraints
solver.add(peters == 4)  # Peters was recruited fourth
solver.add(tao == 2)     # Tao was recruited second

# Quinn was recruited earlier than Rovero
solver.add(quinn < rovero)

# Villas was recruited immediately before White
solver.add(villas + 1 == white)

# Stanton was recruited neither immediately before nor immediately after Tao
# Tao is in position 2, so Stanton cannot be in 1 or 3
solver.add(stanton != 1)
solver.add(stanton != 3)

# Base constraints are set. Now evaluate each option.

# Option A: Quinn was recruited third
opt_a_constr = (quinn == 3)

# Option B: Rovero was recruited fifth
opt_b_constr = (rovero == 5)

# Option C: Stanton was recruited sixth
opt_c_constr = (stanton == 6)

# Option D: Villas was recruited sixth
opt_d_constr = (villas == 6)

# Option E: White was recruited third
opt_e_constr = (white == 3)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")