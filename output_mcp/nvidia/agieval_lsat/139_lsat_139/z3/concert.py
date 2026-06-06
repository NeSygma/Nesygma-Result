from z3 import *

solver = Solver()

# Variables
g = Int('g')  # guitarist position
k = Int('k')  # keyboard position
p = Int('p')  # percussionist position
s = Int('s')  # saxophonist position
t = Int('t')  # trumpeter position
v = Int('v')  # violinist position

# Domain
for var in [g, k, p, s, t, v]:
    solver.add(var >= 1, var <= 6)

# AllDifferent
solver.add(Distinct([g, k, p, s, t, v]))

# Constraints
solver.add(g != 4)  # guitarist not fourth
solver.add(p < k)   # percussionist before keyboard
solver.add(v < k)   # violinist before keyboard
solver.add(k < g)   # keyboard before guitarist
solver.add(Xor(s > p, s > t))  # sax after exactly one of percussionist or trumpeter

# Answer constraints
found_options = []
# A
solver.push()
solver.add(v == 1)
solver.add(p == 2)
solver.add(s == 3)
solver.add(g == 4)
solver.add(t == 5)
solver.add(k == 6)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# B
solver.push()
solver.add(p == 1)
solver.add(v == 2)
solver.add(k == 3)
solver.add(t == 4)
solver.add(s == 5)
solver.add(g == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# C
solver.push()
solver.add(v == 1)
solver.add(t == 2)
solver.add(s == 3)
solver.add(p == 4)
solver.add(k == 5)
solver.add(g == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# D
solver.push()
solver.add(k == 1)
solver.add(t == 2)
solver.add(v == 3)
solver.add(s == 4)
solver.add(g == 5)
solver.add(p == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# E
solver.push()
solver.add(g == 1)
solver.add(v == 2)
solver.add(k == 3)
solver.add(p == 4)
solver.add(s == 5)
solver.add(t == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")