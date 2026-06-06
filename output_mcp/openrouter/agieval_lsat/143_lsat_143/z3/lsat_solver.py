from z3 import *

solver = Solver()
# Variables for positions 1..6
g = Int('g')  # guitarist
k = Int('k')  # keyboard
p = Int('p')  # percussionist
s = Int('s')  # saxophonist
t = Int('t')  # trumpeter
v = Int('v')  # violinist
vars = [g,k,p,s,t,v]
# Domain constraints
for var in vars:
    solver.add(var >= 1, var <= 6)
# All distinct
solver.add(Distinct(vars))
# Base constraints
solver.add(g != 4)               # guitarist not fourth
solver.add(p < k)                # percussionist before keyboard
solver.add(v < k, k < g)        # keyboard after violinist and before guitarist
# saxophonist after either percussionist or trumpeter, but not both
# XOR: (s > p) != (s > t)
solver.add(Xor(s > p, s > t))
# Condition: violinist is fourth
solver.add(v == 4)

# Define negations for each option
negations = []
# A: p < v  => negation p >= v
negations.append(("A", p >= v))
# B: t < v  => negation t >= v
negations.append(("B", t >= v))
# C: t < g  => negation t >= g
negations.append(("C", t >= g))
# D: s < v  => negation s >= v
negations.append(("D", s >= v))
# E: t < s  => negation t >= s
negations.append(("E", t >= s))

found_options = []
for letter, constr in negations:
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