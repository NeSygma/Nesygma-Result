from z3 import *

solver = Solver()

# Declare the articles as Int variables representing their positions (1 to 7)
# We will directly assign positions to articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article must be assigned a unique position between 1 and 7
solver.add(G >= 1, G <= 7)
solver.add(H >= 1, H <= 7)
solver.add(J >= 1, J <= 7)
solver.add(Q >= 1, Q <= 7)
solver.add(R >= 1, R <= 7)
solver.add(S >= 1, S <= 7)
solver.add(Y >= 1, Y <= 7)
solver.add(Distinct([G, H, J, Q, R, S, Y]))

# Topic constraints
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y

# Consecutive articles cannot cover the same topic
# Finance articles cannot be consecutive
solver.add(Not(Or(
    And(G == H - 1, True),
    And(G == H + 1, True),
    And(G == J - 1, True),
    And(G == J + 1, True),
    And(H == J - 1, True),
    And(H == J + 1, True)
)))

# Nutrition articles cannot be consecutive
solver.add(Not(Or(
    And(Q == R - 1, True),
    And(Q == R + 1, True),
    And(Q == S - 1, True),
    And(Q == S + 1, True),
    And(R == S - 1, True),
    And(R == S + 1, True)
)))

# Wildlife article cannot be consecutive with itself (only one wildlife article)
# This is already handled by Distinct

# S can be earlier than Q only if Q is third
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now, evaluate the multiple choice options
found_options = []

# Option A: H, S, J, Q, Y, G, R
solver.push()
solver.add(H == 1)
solver.add(S == 2)
solver.add(J == 3)
solver.add(Q == 4)
solver.add(Y == 5)
solver.add(G == 6)
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J, Q, G, H, S, Y, R
solver.push()
solver.add(J == 1)
solver.add(Q == 2)
solver.add(G == 3)
solver.add(H == 4)
solver.add(S == 5)
solver.add(Y == 6)
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q, J, S, H, Y, G, R
solver.push()
solver.add(Q == 1)
solver.add(J == 2)
solver.add(S == 3)
solver.add(H == 4)
solver.add(Y == 5)
solver.add(G == 6)
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Q, J, Y, S, G, R, H
solver.push()
solver.add(Q == 1)
solver.add(J == 2)
solver.add(Y == 3)
solver.add(S == 4)
solver.add(G == 5)
solver.add(R == 6)
solver.add(H == 7)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: S, G, Q, J, Y, R, H
solver.push()
solver.add(S == 1)
solver.add(G == 2)
solver.add(Q == 3)
solver.add(J == 4)
solver.add(Y == 5)
solver.add(R == 6)
solver.add(H == 7)
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