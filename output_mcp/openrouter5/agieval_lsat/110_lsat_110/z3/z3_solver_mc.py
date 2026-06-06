from z3 import *

solver = Solver()

# 7 positions (1-indexed)
# Variables: each article's position
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article gets a distinct position from 1 to 7
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct(articles))
for a in articles:
    solver.add(a >= 1, a <= 7)

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic.
# For each pair of articles from the same topic, they cannot be consecutive.
# Finance: G, H, J
for a1, a2 in [(G, H), (G, J), (H, J)]:
    solver.add(Abs(a1 - a2) != 1)
# Nutrition: Q, R, S
for a1, a2 in [(Q, R), (Q, S), (R, S)]:
    solver.add(Abs(a1 - a2) != 1)

# S can be earlier than Q only if Q is third.
# If S < Q, then Q == 3.
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Given: Y is fourth
solver.add(Y == 4)

# Now test each option: which MUST be true?
# An option "must be true" if adding its negation makes the problem unsat.
# i.e., the option is forced by the constraints.

found_options = []

# Option A: J is second
solver.push()
solver.add(J != 2)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: J is third
solver.push()
solver.add(J != 3)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
solver.push()
solver.add(Q != 1)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Q is third
solver.push()
solver.add(Q != 3)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: R is seventh
solver.push()
solver.add(R != 7)
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