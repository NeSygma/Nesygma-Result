from z3 import *

# Base constraints solver
solver = Solver()

# Number of accomplices
N = 7

# Create a list of positions for each accomplice
# We will use a list of integers to represent the order of accomplices
# The list `order` will be a permutation of [0, 1, 2, 3, 4, 5, 6], where each index represents a position,
# and the value at that index represents the accomplice (encoded as an integer for simplicity).
# However, for clarity, we will map each accomplice to a unique integer ID:
# Peters = 0, Quinn = 1, Rovero = 2, Stanton = 3, Tao = 4, Villas = 5, White = 6

# We will use a list of Int variables to represent the position of each accomplice
# pos[p] = position of accomplice p
peters, quinn, rovero, stanton, tao, villas, white = Ints('peters quinn rovero stanton tao villas white')

# Each accomplice has a unique position (0 to 6)
solver.add(peters >= 0, peters < N)
solver.add(quinn >= 0, quinn < N)
solver.add(rovero >= 0, rovero < N)
solver.add(stanton >= 0, stanton < N)
solver.add(tao >= 0, tao < N)
solver.add(villas >= 0, villas < N)
solver.add(white >= 0, white < N)

# All positions are distinct
solver.add(Distinct([peters, quinn, rovero, stanton, tao, villas, white]))

# Peters was recruited fourth (position 3, since positions are 0-indexed)
solver.add(peters == 3)

# Villas was recruited immediately before White
solver.add(villas + 1 == white)

# Quinn was recruited earlier than Rovero
solver.add(quinn < rovero)

# Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Abs(stanton - tao) != 1)

# Now, evaluate each option
found_options = []

# Option A: Quinn, Tao, Stanton, Peters, Villas, White, Rovero
# This corresponds to:
# quinn=0, tao=1, stanton=2, peters=3, villas=4, white=5, rovero=6
opt_a_constr = And(
    quinn == 0,
    tao == 1,
    stanton == 2,
    peters == 3,
    villas == 4,
    white == 5,
    rovero == 6
)

# Option B: Quinn, White, Rovero, Peters, Stanton, Villas, Tao
# quinn=0, white=1, rovero=2, peters=3, stanton=4, villas=5, tao=6
opt_b_constr = And(
    quinn == 0,
    white == 1,
    rovero == 2,
    peters == 3,
    stanton == 4,
    villas == 5,
    tao == 6
)

# Option C: Villas, White, Quinn, Stanton, Peters, Tao, Rovero
# villas=0, white=1, quinn=2, stanton=3, peters=4, tao=5, rovero=6
opt_c_constr = And(
    villas == 0,
    white == 1,
    quinn == 2,
    stanton == 3,
    peters == 4,
    tao == 5,
    rovero == 6
)

# Option D: Villas, White, Stanton, Peters, Quinn, Tao, Rovero
# villas=0, white=1, stanton=2, peters=3, quinn=4, tao=5, rovero=6
opt_d_constr = And(
    villas == 0,
    white == 1,
    stanton == 2,
    peters == 3,
    quinn == 4,
    tao == 5,
    rovero == 6
)

# Option E: Villas, White, Stanton, Peters, Rovero, Tao, Quinn
# villas=0, white=1, stanton=2, peters=3, rovero=4, tao=5, quinn=6
opt_e_constr = And(
    villas == 0,
    white == 1,
    stanton == 2,
    peters == 3,
    rovero == 4,
    tao == 5,
    quinn == 6
)

# Test each option
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