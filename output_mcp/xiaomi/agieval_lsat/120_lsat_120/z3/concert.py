from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Each band assigned to a slot 1-6
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6, all different
for b in bands:
    solver.add(And(b >= 1, b <= 6))
solver.add(Distinct(bands))

# Constraints:
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(V < Z)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(W < X)
solver.add(Z < X)

# 3. Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(U == 4, U == 5, U == 6))

# 4. Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Now test which bands CAN be in slot 1
# Option A: Only Yardsign
opt_a = (Y == 1)
# Option B: Vegemite, Wellspring
opt_b = Or(V == 1, W == 1)
# Option C: Vegemite, Yardsign
opt_c = Or(V == 1, Y == 1)
# Option D: Vegemite, Wellspring, Yardsign
opt_d = Or(V == 1, W == 1, Y == 1)
# Option E: Vegemite, Wellspring, Yardsign, Zircon
opt_e = Or(V == 1, W == 1, Y == 1, Z == 1)

# The question asks: which is the COMPLETE and ACCURATE list of bands
# that COULD be in slot 1?
# We need to check: for each option, is it possible that slot 1 is filled
# by one of the listed bands, AND is it impossible for any unlisted band
# to be in slot 1?

# First, let's find which bands can individually be in slot 1
band_names = {U: "Uneasy", V: "Vegemite", W: "Wellspring", X: "Xpert", Y: "Yardsign", Z: "Zircon"}
can_be_slot1 = []

for b, name in band_names.items():
    s = Solver()
    # Add all base constraints
    s.add(Distinct(bands))
    for band in bands:
        s.add(And(band >= 1, band <= 6))
    s.add(V < Z)
    s.add(W < X)
    s.add(Z < X)
    s.add(Or(U == 4, U == 5, U == 6))
    s.add(Or(Y == 1, Y == 2, Y == 3))
    # This band in slot 1
    s.add(b == 1)
    if s.check() == sat:
        can_be_slot1.append(name)

print("Bands that can be in slot 1:", can_be_slot1)

# Now check each answer option
found_options = []

# Option A: Only Yardsign
opt_a_constr = And(
    # Yardsign can be in slot 1
    Y == 1
)
# But we need to verify: is Yardsign the ONLY band that can be slot 1?
# Option A says the list is just {Yardsign}
# This is correct if Yardsign can be in slot 1 AND no other band can be
# We already know from above which bands can be in slot 1

# Option B: Vegemite, Wellspring
# Correct if exactly {Vegemite, Wellspring} can be in slot 1

# Option C: Vegemite, Yardsign
# Correct if exactly {Vegemite, Yardsign} can be in slot 1

# Option D: Vegemite, Wellspring, Yardsign
# Correct if exactly {Vegemite, Wellspring, Yardsign} can be in slot 1

# Option E: Vegemite, Wellspring, Yardsign, Zircon
# Correct if exactly {Vegemite, Wellspring, Yardsign, Zircon} can be in slot 1

# The correct answer is the option whose set matches exactly the set of bands
# that can be in slot 1

# Let's determine the exact set
possible_set = set(can_be_slot1)

option_sets = {
    "A": {"Yardsign"},
    "B": {"Vegemite", "Wellspring"},
    "C": {"Vegemite", "Yardsign"},
    "D": {"Vegemite", "Wellspring", "Yardsign"},
    "E": {"Vegemite", "Wellspring", "Yardsign", "Zircon"},
}

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