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

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for var in [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]:
        sol[var] = m.eval(var, model_completion=True)
    solutions.append(sol)
    # Blocking clause: at least one position different
    solver.add(Or([var != sol[var] for var in [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]]))

print(f"Total solutions: {len(solutions)}")
for idx, sol in enumerate(solutions):
    print(f"Solution {idx+1}:")
    for var, val in sol.items():
        print(f"  {var} = {val}")
    # Compute article order
    order = sorted([(val, var) for var, val in sol.items()])
    print("  Order:", [str(var) for _, var in order])
    print()

# Check which options are always true
opt_a = all(sol[pos_J] == 2 for sol in solutions)
opt_b = all(sol[pos_J] == 3 for sol in solutions)
opt_c = all(sol[pos_Q] == 1 for sol in solutions)
opt_d = all(sol[pos_Q] == 3 for sol in solutions)
opt_e = all(sol[pos_R] == 7 for sol in solutions)

print("Options always true:")
print(f"A: J is second: {opt_a}")
print(f"B: J is third: {opt_b}")
print(f"C: Q is first: {opt_c}")
print(f"D: Q is third: {opt_d}")
print(f"E: R is seventh: {opt_e}")