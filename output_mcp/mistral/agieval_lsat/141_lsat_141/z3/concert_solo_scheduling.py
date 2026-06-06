from z3 import *

solver = Solver()

# Declare variables for each band member's solo position
# Solo positions are 1 to 6
solo_positions = {}
for member in ["guitarist", "keyboardist", "percussionist", "saxophonist", "trumpeter", "violinist"]:
    solo_positions[member] = Int(f"{member}")

# Helper to extract variables
G = solo_positions["guitarist"]
K = solo_positions["keyboardist"]
P = solo_positions["percussionist"]
S = solo_positions["saxophonist"]
T = solo_positions["trumpeter"]
V = solo_positions["violinist"]

# 1. All solo positions are between 1 and 6 (inclusive)
for member in solo_positions.values():
    solver.add(member >= 1, member <= 6)

# 2. All solo positions are distinct
solver.add(Distinct(list(solo_positions.values())))

# 3. The guitarist does not perform the fourth solo
solver.add(G != 4)

# 4. The percussionist performs a solo at some time before the keyboard player
solver.add(P < K)

# 5. The keyboard player performs a solo at some time after the violinist and at some time before the guitarist
solver.add(V < K)
solver.add(K < G)

# 6. The saxophonist performs a solo at some time after either the percussionist or the trumpeter, but not both
# This means: (S > P and S <= T) or (S > T and S <= P)
solver.add(Or(And(S > P, S <= T), And(S > T, S <= P)))

# Base constraints are now fully encoded

# Now evaluate the multiple-choice options
# We will check each option to see if it is possible under the constraints

# Option A: The keyboard player performs the first solo
opt_a_constr = (K == 1)

# Option B: The guitarist performs the second solo
opt_b_constr = (G == 2)

# Option C: The guitarist performs a solo at some time before the saxophonist does
opt_c_constr = (G < S)

# Option D: The guitarist performs a solo at some time before the percussionist does
opt_d_constr = (G < P)

# Option E: The keyboard player performs a solo at some time before the saxophonist does
opt_e_constr = (K < S)

# Now check each option
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