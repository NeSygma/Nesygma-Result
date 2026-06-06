from z3 import *

# We have 6 slots (1-6) and 6 bands.
# We'll model each band's slot as an integer variable.
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]
band_names = ['U', 'V', 'W', 'X', 'Y', 'Z']

solver = Solver()

# Each band in a distinct slot 1..6
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Original constraints:
# 1. Vegemite (V) earlier than Zircon (Z): V < Z
solver.add(V < Z)

# 2. Wellspring (W) and Zircon (Z) each earlier than Xpert (X): W < X, Z < X
solver.add(W < X)
solver.add(Z < X)

# 3. Uneasy (U) in one of the last three slots: U >= 4
solver.add(U >= 4)

# 4. Yardsign (Y) in one of the first three slots: Y <= 3
solver.add(Y <= 3)

# Now we need to test each option as a REPLACEMENT for constraint #2 (W < X and Z < X).
# The replacement must have the SAME EFFECT in determining the order.
# So we need to check: does the replacement, together with the other original constraints
# (V<Z, U>=4, Y<=3), produce exactly the same set of possible orderings as the original?

# Approach: For each option, we check if the set of solutions with the replacement
# is a subset of the set of solutions with the original constraint, AND vice versa.
# But since we're doing multiple choice, we can test each option by checking if
# the replacement is logically equivalent to the original given the other constraints.

# Actually, the standard LSAT approach: "which substitution has the same effect"
# means: if we replace the original constraint with the new one, the set of
# possible orders is identical. So we need to check equivalence.

# Let's enumerate all solutions of the original problem, then for each option,
# enumerate all solutions with that option replacing the original constraint,
# and compare.

# First, get all solutions for the original problem
original_solutions = set()
solver.push()  # save state
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(b).as_long() for b in bands)
    original_solutions.add(sol)
    solver.add(Or([b != m.eval(b) for b in bands]))
solver.pop()

print(f"Original solutions count: {len(original_solutions)}")
for sol in sorted(original_solutions):
    print(f"  U={sol[0]}, V={sol[1]}, W={sol[2]}, X={sol[3]}, Y={sol[4]}, Z={sol[5]}")

# Now test each option
options = {
    "A": lambda: [X < U],  # Only Uneasy can perform in a later slot than Xpert. Means: if a band is later than X, it must be U. So any band later than X is U. Equivalently: for all bands B != U, B < X. But we only have 6 bands. So: V < X, W < X, Y < X, Z < X. Actually "Only Uneasy can perform in a later slot than Xpert" means: no band other than Uneasy can be later than Xpert. So all bands except U must be earlier than X.
    "B": lambda: [V < W, W < Z],  # Vegemite earlier than Wellspring, Wellspring earlier than Zircon
    "C": lambda: [V < X, W < X],  # Vegemite and Wellspring each earlier than Xpert
    "D": lambda: [Or(And(X == U - 1, X >= 1), And(X == U + 1, X <= 6))],  # Xpert immediately before or after Uneasy
    "E": lambda: [Or(X == 5, X == 6)],  # Xpert in slot 5 or 6
}

found_options = []

for letter, constr_fn in options.items():
    # Build solver with all original constraints EXCEPT the replaced one
    s = Solver()
    for b in bands:
        s.add(b >= 1, b <= 6)
    s.add(Distinct(bands))
    s.add(V < Z)  # original constraint 1
    s.add(U >= 4)  # original constraint 3
    s.add(Y <= 3)  # original constraint 4
    # Add the replacement constraint instead of W<X and Z<X
    for c in constr_fn():
        s.add(c)
    
    # Get all solutions for this option
    option_solutions = set()
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(b).as_long() for b in bands)
        option_solutions.add(sol)
        s.add(Or([b != m.eval(b) for b in bands]))
    
    print(f"\nOption {letter} solutions count: {len(option_solutions)}")
    for sol in sorted(option_solutions):
        print(f"  U={sol[0]}, V={sol[1]}, W={sol[2]}, X={sol[3]}, Y={sol[4]}, Z={sol[5]}")
    
    # Check if option_solutions == original_solutions
    if option_solutions == original_solutions:
        found_options.append(letter)
        print(f"  -> MATCHES original")

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")