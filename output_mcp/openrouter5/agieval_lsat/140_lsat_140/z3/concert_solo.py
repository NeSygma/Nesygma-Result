from z3 import *

# Six members: guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist
# Each performs exactly one solo, positions 1 through 6.
# We'll use Int variables for each member's solo position.

g, k, p, s, t, v = Ints('g k p s t v')

solver = Solver()

# Domain: positions 1 to 6
members = [g, k, p, s, t, v]
for m in members:
    solver.add(m >= 1, m <= 6)

# All distinct positions
solver.add(Distinct(members))

# Constraints:
# 1. The guitarist does not perform the fourth solo.
solver.add(g != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(p < k)

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(v < k)
solver.add(k < g)

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# "after either P or T, but not both" means: (s > p) XOR (s > t)
# XOR: (s > p) != (s > t)
solver.add(If(s > p, 1, 0) + If(s > t, 1, 0) == 1)

# Additional condition from the question stem:
# "If the percussionist performs a solo at some time before the saxophonist does"
# This is a conditional question: we add this as an extra premise.
solver.add(p < s)

# Now evaluate each option as "must be true" under these constraints.
# "Must be true" means: if we add the negation of the option, the system becomes unsat.
# So we check: base + option_negation -> unsat means option must be true.

found_options = []

# Option A: The percussionist performs the first solo.
opt_a = (p == 1)
solver.push()
solver.add(Not(opt_a))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: The percussionist performs the second solo.
opt_b = (p == 2)
solver.push()
solver.add(Not(opt_b))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: The violinist performs a solo at some time before the saxophonist does.
opt_c = (v < s)
solver.push()
solver.add(Not(opt_c))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: The percussionist performs a solo at some time before the trumpeter does.
opt_d = (p < t)
solver.push()
solver.add(Not(opt_d))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: The saxophonist performs a solo at some time before the keyboard player does.
opt_e = (s < k)
solver.push()
solver.add(Not(opt_e))
if solver.check() == unsat:
    found_options.append("E")
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