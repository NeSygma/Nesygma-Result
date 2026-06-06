from z3 import *

solver = Solver()

# Position variables (1-indexed)
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

# Domain constraints
solver.add(pos_G >= 1, pos_G <= 7)
solver.add(pos_H >= 1, pos_H <= 7)
solver.add(pos_J >= 1, pos_J <= 7)
solver.add(pos_Q >= 1, pos_Q <= 7)
solver.add(pos_R >= 1, pos_R <= 7)
solver.add(pos_S >= 1, pos_S <= 7)
solver.add(pos_Y >= 1, pos_Y <= 7)

# All different
solver.add(Distinct([pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]))

# Consecutive same-topic forbidden
solver.add(Not(Or(pos_G == pos_H + 1, pos_H == pos_G + 1)))
solver.add(Not(Or(pos_G == pos_J + 1, pos_J == pos_G + 1)))
solver.add(Not(Or(pos_H == pos_J + 1, pos_J == pos_H + 1)))
solver.add(Not(Or(pos_Q == pos_R + 1, pos_R == pos_Q + 1)))
solver.add(Not(Or(pos_Q == pos_S + 1, pos_S == pos_Q + 1)))
solver.add(Not(Or(pos_R == pos_S + 1, pos_S == pos_R + 1)))

# Conditional: S earlier than Q only if Q is third
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# S earlier than Y
solver.add(pos_S < pos_Y)

# J earlier than G, G earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Given condition: Y is fourth
solver.add(pos_Y == 4)

# Option constraints
option_constraints = {
    "A": pos_J == 2,
    "B": pos_J == 3,
    "C": pos_Q == 1,
    "D": pos_Q == 3,
    "E": pos_R == 7
}

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    solver.add(option_constraints[letter])
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    # Retrieve model for the satisfying option
    chosen = found_options[0]
    solver.push()
    solver.add(option_constraints[chosen])
    if solver.check() == sat:
        m = solver.model()
        print("STATUS: sat")
        print(f"answer:{chosen}")
        print("model:", m)
    solver.pop()
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")