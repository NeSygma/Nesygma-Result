from z3 import *

solver = Solver()

# Positions 1-7
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

articles = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# Domain: each position is between 1 and 7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All positions are distinct
solver.add(Distinct(articles))

# Given: J is third
solver.add(pos_J == 3)

# Constraint 1: Consecutive articles cannot cover the same topic
# Finance: G, H, J
solver.add(And(pos_G - pos_H != 1, pos_H - pos_G != 1))
solver.add(And(pos_G - pos_J != 1, pos_J - pos_G != 1))
solver.add(And(pos_H - pos_J != 1, pos_J - pos_H != 1))

# Nutrition: Q, R, S
solver.add(And(pos_Q - pos_R != 1, pos_R - pos_Q != 1))
solver.add(And(pos_Q - pos_S != 1, pos_S - pos_Q != 1))
solver.add(And(pos_R - pos_S != 1, pos_S - pos_R != 1))

# Wildlife: Y (single article, no same-topic adjacency constraint needed)

# Constraint 2: S can be earlier than Q only if Q is third.
# Implies(S < Q, Q == 3)
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Note: J = 3, so G > 3 and R > G > 3

# Also need to enforce that positions 1-7 are all used exactly once (Distinct does this already)

# Now evaluate each option
# (A) G is fourth => pos_G == 4
opt_a = (pos_G == 4)

# (B) H is sixth => pos_H == 6
opt_b = (pos_H == 6)

# (C) Q is first => pos_Q == 1
opt_c = (pos_Q == 1)

# (D) S is second => pos_S == 2
opt_d = (pos_S == 2)

# (E) Y is fifth => pos_Y == 5
opt_e = (pos_Y == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Print the model for debugging
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        print(f"  G={m[pos_G]}, H={m[pos_H]}, J={m[pos_J]}, Q={m[pos_Q]}, R={m[pos_R]}, S={m[pos_S]}, Y={m[pos_Y]}")
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