from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Slots 1-6
U, V, W, X, Y, Z = Ints('U V W X Y Z')

# Each band gets a distinct slot from 1 to 6
bands = [U, V, W, X, Y, Z]
solver.add(Distinct(bands))
for b in bands:
    solver.add(b >= 1, b <= 6)

# Constraints:
# 1. Vegemite performs in an earlier slot than Zircon.
solver.add(V < Z)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(W < X)
solver.add(Z < X)

# 3. Uneasy performs in one of the last three slots (4, 5, or 6).
solver.add(Or(U == 4, U == 5, U == 6))

# 4. Yardsign performs in one of the first three slots (1, 2, or 3).
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Now evaluate each option: which bands could be in slot 1?
# Option A: Yardsign only
opt_a = (Y == 1)
# Option B: Vegemite, Wellspring
opt_b = Or(V == 1, W == 1)
# Option C: Vegemite, Yardsign
opt_c = Or(V == 1, Y == 1)
# Option D: Vegemite, Wellspring, Yardsign
opt_d = Or(V == 1, W == 1, Y == 1)
# Option E: Vegemite, Wellspring, Yardsign, Zircon
opt_e = Or(V == 1, W == 1, Y == 1, Z == 1)

# But the question asks: which is a complete and accurate list of bands any one of which COULD be slot one.
# So we need to test each band individually for possibility in slot 1.
# Then see which option exactly matches the set of possible bands.

# First, find which bands can be in slot 1.
possible_slot1 = []
for letter, band_var, band_name in [("V", V, "Vegemite"), ("W", W, "Wellspring"), ("Y", Y, "Yardsign"), ("Z", Z, "Zircon"), ("U", U, "Uneasy"), ("X", X, "Xpert")]:
    solver.push()
    solver.add(band_var == 1)
    if solver.check() == sat:
        possible_slot1.append(band_name)
    solver.pop()

print("Bands that can be in slot 1:", possible_slot1)

# Now check each option against the set of possible bands
possible_set = set(possible_slot1)

# Map option letters to their band sets
option_sets = {
    "A": {"Yardsign"},
    "B": {"Vegemite", "Wellspring"},
    "C": {"Vegemite", "Yardsign"},
    "D": {"Vegemite", "Wellspring", "Yardsign"},
    "E": {"Vegemite", "Wellspring", "Yardsign", "Zircon"}
}

found_options = []
for letter, opt_set in option_sets.items():
    if opt_set == possible_set:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")