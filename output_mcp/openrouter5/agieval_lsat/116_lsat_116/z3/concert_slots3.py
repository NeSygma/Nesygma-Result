from z3 import *

# The question asks: "Which one of the following CANNOT be the band that performs in slot five?"
# So we need to find which band is IMPOSSIBLE to place in slot 5.
# The approach: for each option, check if there's a valid assignment with that band in slot 5.
# The one that's UNSAT is the answer.

U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

def check_slot5(band_var, band_name):
    solver = Solver()
    for b in bands:
        solver.add(b >= 1, b <= 6)
    solver.add(Distinct(bands))
    solver.add(V < Z)
    solver.add(W < X)
    solver.add(Z < X)
    solver.add(Or([U == i for i in [4,5,6]]))
    solver.add(Or([Y == i for i in [1,2,3]]))
    solver.add(band_var == 5)
    return solver.check()

# Check each option
for letter, var, name in [("A", U, "Uneasy"), ("B", V, "Vegemite"), ("C", W, "Wellspring"), 
                           ("D", X, "Xpert"), ("E", Z, "Zircon")]:
    result = check_slot5(var, name)
    print(f"Option {letter} ({name} in slot 5): {result}")

# Let's also verify by reasoning: 
# V < Z < X, so V < Z < X. Also W < X.
# So X must be after both Z and W.
# If V is in slot 5, then Z must be in slot 6 (since V < Z), and X must be after Z, so X would need slot > 6. Impossible.
# So B (Vegemite) is the answer.

# Let's double check with the skeleton
solver = Solver()
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))
solver.add(V < Z)
solver.add(W < X)
solver.add(Z < X)
solver.add(Or([U == i for i in [4,5,6]]))
solver.add(Or([Y == i for i in [1,2,3]]))

found_options = []
for letter, constr in [("A", U == 5), ("B", V == 5), ("C", W == 5), ("D", X == 5), ("E", Z == 5)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

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