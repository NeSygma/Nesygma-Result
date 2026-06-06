from z3 import *

# Create solver
solver = Solver()

# Define positions 1-8 as variables holding composition IDs
pos = [Int(f'pos_{i}') for i in range(1, 9)]  # pos[0] is position 1, pos[7] is position 8

# Composition IDs
F, H, L, O, P, R, S, T = 0, 1, 2, 3, 4, 5, 6, 7
compositions = [F, H, L, O, P, R, S, T]

# Each position has exactly one composition, and each composition appears exactly once
for i in range(8):
    solver.add(pos[i] >= 0, pos[i] <= 7)
solver.add(Distinct(pos))

# Helper to get position of a composition (1-indexed)
def get_pos(comp):
    result = 8  # default
    for i in range(8):
        result = If(pos[i] == comp, i+1, result)
    return result

pos_F = get_pos(F)
pos_H = get_pos(H)
pos_L = get_pos(L)
pos_O = get_pos(O)
pos_P = get_pos(P)
pos_R = get_pos(R)
pos_S = get_pos(S)
pos_T = get_pos(T)

# Constraint 1: T is immediately before F OR immediately after R
solver.add(Or(
    pos_T == pos_F - 1,  # T before F
    pos_T == pos_R + 1   # T after R
))

# Constraint 2: At least two compositions between F and R (in either order)
# This means |pos_F - pos_R| >= 3
solver.add(Or(
    pos_F >= pos_R + 3,  # F after R with at least 2 between
    pos_R >= pos_F + 3   # R after F with at least 2 between
))

# Constraint 3: O is first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(pos[7] == L, pos[7] == H))

# Constraint 5: P before S (already satisfied with P=3, S=6)
solver.add(pos_P < pos_S)

# Constraint 6: At least one composition between O and S
solver.add(Or(
    pos_O >= pos_S + 2,  # O after S with at least 1 between
    pos_S >= pos_O + 2   # S after O with at least 1 between
))

# Additional given: P is third, S is sixth
solver.add(pos_P == 3)
solver.add(pos_S == 6)

# Let's enumerate all possible models to see what's at position 5
print("Enumerating all possible models...")
models = []
while solver.check() == sat:
    m = solver.model()
    # Get the composition at each position
    model_dict = {}
    for i in range(8):
        comp_val = m.eval(pos[i])
        model_dict[i+1] = comp_val
    models.append(model_dict)
    
    # Add blocking clause to find next model
    # Block by position 5 composition
    comp_at_5 = m.eval(pos[4])
    solver.add(pos[4] != comp_at_5)

print(f"Total models found: {len(models)}")
for i, model in enumerate(models):
    print(f"Model {i+1}: {model}")

# Now let's check what must be at position 5
# Get all possible compositions at position 5
pos5_comps = set()
for model in models:
    pos5_comps.add(model[5])

print(f"\nPossible compositions at position 5: {pos5_comps}")

# Map composition IDs to names
comp_names = {0: 'F', 1: 'H', 2: 'L', 3: 'O', 4: 'P', 5: 'R', 6: 'S', 7: 'T'}
pos5_names = {comp_names[c] for c in pos5_comps}
print(f"Possible names at position 5: {pos5_names}")

# Now check each answer choice
# Reset solver
solver = Solver()

# Re-add all constraints
for i in range(8):
    solver.add(pos[i] >= 0, pos[i] <= 7)
solver.add(Distinct(pos))

# Re-add constraints
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))
solver.add(Or(pos_F >= pos_R + 3, pos_R >= pos_F + 3))
solver.add(Or(pos_O == 1, pos_O == 5))
solver.add(Or(pos[7] == L, pos[7] == H))
solver.add(pos_P < pos_S)
solver.add(Or(pos_O >= pos_S + 2, pos_S >= pos_O + 2))
solver.add(pos_P == 3)
solver.add(pos_S == 6)

# Define options based on what we found
# If position 5 must be F or H, then option A is correct
# If position 5 must be F or O, then option B is correct
# etc.

# Let's check which option is forced
# Option A: F or H
opt_a_constr = Or(pos[4] == F, pos[4] == H)
# Option B: F or O
opt_b_constr = Or(pos[4] == F, pos[4] == O)
# Option C: F or T
opt_c_constr = Or(pos[4] == F, pos[4] == T)
# Option D: H or L
opt_d_constr = Or(pos[4] == H, pos[4] == L)
# Option E: O or R
opt_e_constr = Or(pos[4] == O, pos[4] == R)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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