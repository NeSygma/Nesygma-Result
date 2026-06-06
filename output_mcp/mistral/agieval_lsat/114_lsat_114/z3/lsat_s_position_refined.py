from z3 import *

solver = Solver()

# Articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Order: order[i] is the article at position i+1 (1-indexed)
order = [Int(f'order_{i}') for i in range(7)]
solver.add(Distinct(order))
for i in range(7):
    solver.add(order[i] >= 1, order[i] <= 7)

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

# Position variables for S, Q, Y, J, G, R
pos_S = Int('pos_S')
pos_Q = Int('pos_Q')
pos_Y = Int('pos_Y')
pos_J = Int('pos_J')
pos_G = Int('pos_G')
pos_R = Int('pos_R')

solver.add(pos_S == Sum([If(order[i] == S, i+1, 0) for i in range(7)]))
solver.add(pos_Q == Sum([If(order[i] == Q, i+1, 0) for i in range(7)]))
solver.add(pos_Y == Sum([If(order[i] == Y, i+1, 0) for i in range(7)]))
solver.add(pos_J == Sum([If(order[i] == J, i+1, 0) for i in range(7)]))
solver.add(pos_G == Sum([If(order[i] == G, i+1, 0) for i in range(7)]))
solver.add(pos_R == Sum([If(order[i] == R, i+1, 0) for i in range(7)]))

# Constraints:
# 1. S can be earlier than Q only if Q is third
#    => If pos_S < pos_Q, then pos_Q == 3
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))
# 2. S must be earlier than Y
solver.add(pos_S < pos_Y)
# 3. J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

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