from z3 import *

solver = Solver()

# 7 positions (0-indexed: 0=first, 1=second, ..., 6=seventh)
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article gets a distinct position from 0 to 6
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct(articles))
for a in articles:
    solver.add(a >= 0, a <= 6)

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic.
# For each pair in the same topic group, they cannot be consecutive.

# Finance group
for a, b in [(G, H), (G, J), (H, J)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# Nutrition group
for a, b in [(Q, R), (Q, S), (R, S)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# Also Y (wildlife) is alone, so no constraint needed for Y with itself.

# S can be earlier than Q only if Q is third.
# "S can be earlier than Q only if Q is third" means:
# If S < Q, then Q == 2 (third position, 0-indexed).
solver.add(Implies(S < Q, Q == 2))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now evaluate each option: S could be in position X?
# Option A: first (position 0)
# Option B: third (position 2)
# Option C: fourth (position 3)
# Option D: fifth (position 4)
# Option E: sixth (position 5)

found_options = []
for letter, pos in [("A", 0), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    solver.add(S == pos)
    res = solver.check()
    if res == sat:
        m = solver.model()
        print(f"Option {letter} (S={pos}): SAT")
        for a in articles:
            print(f"  {a} = {m[a]}")
        found_options.append(letter)
    else:
        print(f"Option {letter} (S={pos}): UNSAT")
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