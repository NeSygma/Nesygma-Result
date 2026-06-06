from z3 import *

solver = Solver()

# Articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Order: order[i] is the article at position i+1
order = [Int(f'order_{i}') for i in range(7)]
solver.add(Distinct(order))

# Helper: same topic
def same_topic(a1, a2):
    finance = Or(a1 == G, a1 == H, a1 == J)
    finance2 = Or(a2 == G, a2 == H, a2 == J)
    nutrition = Or(a1 == Q, a1 == R, a1 == S)
    nutrition2 = Or(a2 == Q, a2 == R, a2 == S)
    wildlife = And(a1 == Y, a2 == Y)
    return Or(
        And(finance, finance2),
        And(nutrition, nutrition2),
        wildlife
    )

# Consecutive articles cannot have the same topic
for i in range(6):
    a1 = order[i]
    a2 = order[i+1]
    solver.add(Not(same_topic(a1, a2)))

# S can be earlier than Q only if Q is third
pos_S_val = Int('pos_S_val')
pos_Q_val = Int('pos_Q_val')
solver.add(Or([And(order[i] == S, pos_S_val == i+1) for i in range(7)]))
solver.add(Or([And(order[i] == Q, pos_Q_val == i+1) for i in range(7)]))
solver.add(Implies(pos_S_val < pos_Q_val, pos_Q_val == 3))

# S must be earlier than Y
pos_Y_val = Int('pos_Y_val')
solver.add(Or([And(order[i] == Y, pos_Y_val == i+1) for i in range(7)]))
solver.add(pos_S_val < pos_Y_val)

# J must be earlier than G, and G must be earlier than R
pos_J_val = Int('pos_J_val')
pos_G_val = Int('pos_G_val')
pos_R_val = Int('pos_R_val')
solver.add(Or([And(order[i] == J, pos_J_val == i+1) for i in range(7)]))
solver.add(Or([And(order[i] == G, pos_G_val == i+1) for i in range(7)]))
solver.add(Or([And(order[i] == R, pos_R_val == i+1) for i in range(7)]))
solver.add(pos_J_val < pos_G_val)
solver.add(pos_G_val < pos_R_val)

# Now, for multiple choice: check each option
found_options = []
for letter, pos in [("A", 1), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(order[pos-1] == S)
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