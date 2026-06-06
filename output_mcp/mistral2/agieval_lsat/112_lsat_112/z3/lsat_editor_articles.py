from z3 import *

solver = Solver()

# Declare the positions (1st to 7th)
positions = range(1, 8)

# Declare the articles as symbolic integers representing their positions
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article must be assigned a unique position from 1 to 7
solver.add(Distinct(G, H, J, Q, R, S, Y))
for pos in positions:
    solver.add(Or(G == pos, H == pos, J == pos, Q == pos, R == pos, S == pos, Y == pos))

# Topics:
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y

# Helper function to get the topic of an article
def get_topic(article):
    # Finance: G, H, J
    finance = Or(article == G, article == H, article == J)
    # Nutrition: Q, R, S
    nutrition = Or(article == Q, article == R, article == S)
    # Wildlife: Y
    wildlife = (article == Y)
    return Or(finance, nutrition, wildlife)

# For all pairs of articles assigned to consecutive positions, their topics must differ
# We will enforce this by iterating over all pairs of articles and all pairs of consecutive positions
articles = [G, H, J, Q, R, S, Y]
for a in articles:
    for b in articles:
        if a is not b:  # Use 'is not' to compare Z3 expression objects
            for i in range(1, 7):
                # If a is at position i and b is at position i+1, their topics must differ
                solver.add(Implies(And(a == i, b == i + 1), get_topic(a) != get_topic(b)))
                # If b is at position i and a is at position i+1, their topics must differ
                solver.add(Implies(And(b == i, a == i + 1), get_topic(a) != get_topic(b)))

# S can be earlier than Q only if Q is third
# This means: If S < Q, then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now, evaluate the multiple choice options
found_options = []

# Option A: G is second
solver.push()
solver.add(G == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is second
solver.push()
solver.add(H == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: R is third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is third
solver.push()
solver.add(Y == 3)
if solver.check() == sat:
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