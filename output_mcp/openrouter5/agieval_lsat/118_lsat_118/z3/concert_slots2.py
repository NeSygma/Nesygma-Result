from z3 import *

solver = Solver()

# Slots 1-6, bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a distinct slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Constraints:
# Vegemite performs in an earlier slot than Zircon.
solver.add(V < Z)

# Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(W < X)
solver.add(Z < X)

# Uneasy performs in one of the last three slots.
solver.add(Or([U == i for i in [4, 5, 6]]))

# Yardsign performs in one of the first three slots.
solver.add(Or([Y == i for i in [1, 2, 3]]))

# Additional condition: Vegemite performs in slot three.
solver.add(V == 3)

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
result = solver.check()
print(f"Result: {result}")
if result == sat:
    m = solver.model()
    print(f"U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")

# Now let's think about what MUST be true.
# With V=3, we have:
# V < Z => Z > 3, so Z in {4,5,6}
# Z < X => X > Z, so X > Z > 3, so X in {5,6} (since Z >= 4)
# W < X => W < X
# U in {4,5,6}
# Y in {1,2,3}

# Let's enumerate all solutions to see what's always true
solver.push()
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {b: m.eval(b, model_completion=True).as_long() for b in bands}
    solutions.append(sol)
    solver.add(Or([b != m.eval(b, model_completion=True).as_long() for b in bands]))
solver.pop()

print(f"\nTotal solutions: {len(solutions)}")
for sol in solutions:
    print(f"U={sol[U]}, V={sol[V]}, W={sol[W]}, X={sol[X]}, Y={sol[Y]}, Z={sol[Z]}")

# Check each option across all solutions
if solutions:
    for letter, name, constr in [
        ("A", "U < X", lambda s: s[U] < s[X]),
        ("B", "W < Z", lambda s: s[W] < s[Z]),
        ("C", "X < U", lambda s: s[X] < s[U]),
        ("D", "Y < W", lambda s: s[Y] < s[W]),
        ("E", "Z < U", lambda s: s[Z] < s[U])
    ]:
        all_true = all(constr(sol) for sol in solutions)
        print(f"Option {letter} ({name}): always true = {all_true}")