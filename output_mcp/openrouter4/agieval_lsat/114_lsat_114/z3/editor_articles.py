from z3 import *

solver = Solver()

pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

positions = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# All positions between 1 and 7
for p in positions:
    solver.add(p >= 1, p <= 7)

# All distinct
solver.add(Distinct(positions))

# Topic constraints: same-topic articles cannot be adjacent
# Finance: G, H, J - no two can be adjacent
solver.add(And(pos_G - pos_H != 1, pos_H - pos_G != 1))
solver.add(And(pos_G - pos_J != 1, pos_J - pos_G != 1))
solver.add(And(pos_H - pos_J != 1, pos_J - pos_H != 1))

# Nutrition: Q, R, S - no two can be adjacent
solver.add(And(pos_Q - pos_R != 1, pos_R - pos_Q != 1))
solver.add(And(pos_Q - pos_S != 1, pos_S - pos_Q != 1))
solver.add(And(pos_R - pos_S != 1, pos_S - pos_R != 1))

# S can be earlier than Q only if Q is third
# (S < Q) → (Q == 3)
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# S must be earlier than Y
solver.add(pos_S < pos_Y)

# J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Evaluate each position option
possible = []
impossible = []

for letter, pos_val in [("A", 1), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(pos_S == pos_val)
    if solver.check() == sat:
        possible.append(letter)
    else:
        impossible.append(letter)
    solver.pop()

# For a "which position is NOT possible" question, the answer is the impossible one
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible positions found {impossible}")
elif len(impossible) == 0:
    print("STATUS: unsat")
    print(f"Refine: All positions are possible, none is the exception")