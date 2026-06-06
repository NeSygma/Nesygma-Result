from z3 import *

solver = Solver()

# Declare color assignment variables (rug index: 0,1,2 or -1=unused)
f, o, p, t, w, y = Int('f'), Int('o'), Int('p'), Int('t'), Int('w'), Int('y')

# Domain: each color is either unused (-1) or assigned to rug 0,1,2
for var in (f, o, p, t, w, y):
    solver.add(Or(var == -1, var == 0, var == 1, var == 2))

# Exactly five colors are used (one color unused)
used_count = If(f != -1, 1, 0) + If(o != -1, 1, 0) + If(p != -1, 1, 0) + \
             If(t != -1, 1, 0) + If(w != -1, 1, 0) + If(y != -1, 1, 0)
solver.add(used_count == 5)

# Pairwise exclusion constraints
solver.add(f != t)   # forest and turquoise not together
solver.add(p != t)   # peach and turquoise not together
solver.add(p != y)   # peach and yellow not together

# Olive implies peach (same rug)
solver.add(Or(o == -1, And(p != -1, p == o)))

# White rule: if white is used, exactly three colors are on that rug
count_white = If(w != -1, (If(f == w, 1, 0) + If(o == w, 1, 0) + If(p == w, 1, 0) + If(t == w, 1, 0) + If(y == w, 1, 0)) + 1, 0)
solver.add(Or(w == -1, count_white == 3))

# One rug is solid peach (peach alone on its rug)
solid_peach = Or(
    And(p == 0, o != 0, f != 0, t != 0, w != 0, y != 0),
    And(p == 1, o != 1, f != 1, t != 1, w != 1, y != 1),
    And(p == 2, o != 2, f != 2, t != 2, w != 2, y != 2)
)
solver.add(solid_peach)

# Add negation of (E): white and yellow are NOT together
# For each rug i, not (w == i and y == i)
solver.add(Or(w != 0, y != 0))
solver.add(Or(w != 1, y != 1))
solver.add(Or(w != 2, y != 2))

# Check satisfiability
result = solver.check()
print("Result:", result)
if result == sat:
    model = solver.model()
    print("Model found:")
    print("f =", model[f])
    print("o =", model[o])
    print("p =", model[p])
    print("t =", model[t])
    print("w =", model[w])
    print("y =", model[y])
else:
    print("Unsatisfiable")