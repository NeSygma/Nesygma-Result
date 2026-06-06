from z3 import *

solver = Solver()

# Articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Domain: each article is at a position 1-7
all_articles = [G, H, J, Q, R, S, Y]
for a in all_articles:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(all_articles))

# Condition 1: Consecutive articles cannot cover the same topic.
# Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# For any pair of articles that share a topic, they cannot be consecutive.
# We need to ensure that if two articles have the same topic, |pos_i - pos_j| != 1.

# Finance articles: G, H, J
# No two finance articles can be consecutive
for a, b in [(G, H), (G, J), (H, J)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# Nutrition articles: Q, R, S
for a, b in [(Q, R), (Q, S), (R, S)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# Wildlife: only Y, so no constraint from same topic

# Condition 2: S can be earlier than Q only if Q is third.
# If S < Q, then Q == 3. Equivalently: Or(Q == 3, Q < S)
solver.add(Implies(S < Q, Q == 3))

# Condition 3: S must be earlier than Y.
solver.add(S < Y)

# Condition 4: J must be earlier than G, and G must be earlier than R.
solver.add(J < G)
solver.add(G < R)

# Additional: Y is fourth.
solver.add(Y == 4)

# Now test each option
# (A) J is second -> J == 2
# (B) J is third -> J == 3
# (C) Q is first -> Q == 1
# (D) Q is third -> Q == 3
# (E) R is seventh -> R == 7

found_options = []
for letter, constr in [("A", J == 2), ("B", J == 3), ("C", Q == 1), ("D", Q == 3), ("E", R == 7)]:
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