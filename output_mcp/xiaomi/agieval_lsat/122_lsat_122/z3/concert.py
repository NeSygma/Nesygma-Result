from z3 import *

# Variables: slot positions for each band (1..6)
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Base constraints (common to all)
base = Solver()
for b in bands:
    base.add(And(b >= 1, b <= 6))
base.add(Distinct(bands))

# Original constraints (excluding the one to be substituted)
# Vegemite < Zircon
base.add(V < Z)
# Uneasy in last three slots (4,5,6)
base.add(U >= 4)
# Yardsign in first three slots (1,2,3)
base.add(Y <= 3)

# Original constraint to be substituted: W < X and Z < X
original = And(W < X, Z < X)

# Define options
# "Only Uneasy can perform in a later slot than Xpert" means:
# No band other than Uneasy performs later than Xpert.
# So: V <= X, W <= X, Y <= X, Z <= X
options = {
    "A": And(V <= X, W <= X, Y <= X, Z <= X),
    "B": And(V < W, W < Z),
    "C": And(V < X, W < X),
    "D": Or(X == U - 1, X == U + 1),  # Xpert immediately before or after Uneasy
    "E": Or(X == 5, X == 6),
}

found_options = []

for letter, opt_constr in options.items():
    # Check: base + option ↔ base + original
    # Direction 1: (base + option) => (base + original)
    # i.e., base + option + NOT(original) is unsat
    s1 = Solver()
    for c in base.assertions():
        s1.add(c)
    s1.add(opt_constr)
    s1.add(Not(original))
    dir1 = s1.check()

    # Direction 2: (base + original) => (base + option)
    # i.e., base + original + NOT(option) is unsat
    s2 = Solver()
    for c in base.assertions():
        s2.add(c)
    s2.add(original)
    s2.add(Not(opt_constr))
    dir2 = s2.check()

    if dir1 == unsat and dir2 == unsat:
        found_options.append(letter)
        print(f"Option {letter}: EQUIVALENT")
    else:
        print(f"Option {letter}: NOT equivalent (dir1={dir1}, dir2={dir2})")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")