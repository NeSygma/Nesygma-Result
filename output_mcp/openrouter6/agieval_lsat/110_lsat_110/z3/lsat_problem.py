from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
G, H, J, Q, R, S, Y = 0, 1, 2, 3, 4, 5, 6
articles = [G, H, J, Q, R, S, Y]

# Position variables for each article
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

solver = Solver()

# Domain constraints: positions 1..7
for p in [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]:
    solver.add(p >= 1, p <= 7)

# All positions distinct
solver.add(Distinct(pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y))

# Article at each position
article_at_pos = [Int(f'article_at_pos_{i}') for i in range(1, 8)]
for i in range(1, 8):
    solver.add(article_at_pos[i-1] >= 0, article_at_pos[i-1] <= 6)
solver.add(Distinct(article_at_pos))

# Link article_at_pos to pos_* variables
article_to_pos = {G: pos_G, H: pos_H, J: pos_J, Q: pos_Q, R: pos_R, S: pos_S, Y: pos_Y}
for art, pos_var in article_to_pos.items():
    solver.add(Or([And(article_at_pos[i-1] == art, pos_var == i) for i in range(1, 8)]))

# Topic function
def topic_of(art):
    return If(Or(art == G, art == H, art == J), 0,
              If(Or(art == Q, art == R, art == S), 1, 2))

# Consecutive topics differ
for i in range(1, 7):
    art1 = article_at_pos[i-1]
    art2 = article_at_pos[i]
    solver.add(topic_of(art1) != topic_of(art2))

# Conditional: S can be earlier than Q only if Q is third.
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# S must be earlier than Y
solver.add(pos_S < pos_Y)

# J earlier than G, and G earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Y is fourth
solver.add(pos_Y == 4)

# Now evaluate each option
found_options = []

# Option A: J is second
opt_a_constr = (pos_J == 2)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J is third
opt_b_constr = (pos_J == 3)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
opt_c_constr = (pos_Q == 1)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Q is third
opt_d_constr = (pos_Q == 3)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: R is seventh
opt_e_constr = (pos_R == 7)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output according to required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")