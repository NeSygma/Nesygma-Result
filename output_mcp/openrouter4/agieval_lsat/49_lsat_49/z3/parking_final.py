from z3 import *

solver = Solver()

R, So, T, V, X, Y = Ints('R So T V X Y')

for e in [R, So, T, V, X, Y]:
    solver.add(e >= 1, e <= 6)

solver.add(Distinct([R, So, T, V, X, Y]))

solver.add(Y > T)
solver.add(X > So)
solver.add(R > Y)
solver.add(R >= 1, R <= 4)
solver.add(T > So)

found_options = []
for letter, constr in [("A", Y == 2), ("B", V == 5), ("C", T == 3), ("D", So == 2), ("E", R == 3)]:
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