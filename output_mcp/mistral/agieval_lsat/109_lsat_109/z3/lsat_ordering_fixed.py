from z3 import *

# Define the articles as symbolic constants
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Define the positions as integers from 0 to 6
positions = [0, 1, 2, 3, 4, 5, 6]

# Helper: Map article to its topic
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
def topic(article):
    return If(article == G, "finance",
               If(article == H, "finance",
                  If(article == J, "finance",
                     If(article == Q, "nutrition",
                        If(article == R, "nutrition",
                           If(article == S, "nutrition", "wildlife"))))))

# Base solver for the general constraints
solver = Solver()

# Assign each position to an article
# We will use a list to represent the order
order = [Int(f'pos_{i}') for i in positions]

# Each position must be assigned exactly one article
for i in positions:
    solver.add(Or(order[i] == G, order[i] == H, order[i] == J, order[i] == Q, order[i] == R, order[i] == S, order[i] == Y))

# All articles must be used exactly once
solver.add(Distinct(order))

# Constraint 1: Consecutive articles cannot cover the same topic
for i in range(6):
    solver.add(Not(topic(order[i]) == topic(order[i+1])))

# Constraint 2: S can be earlier than Q only if Q is third (position 2)
# We will handle this in the option evaluation.

# Constraint 3: S must be earlier than Y
# Constraint 4: J must be earlier than G, and G must be earlier than R

# For the multiple-choice evaluation, we will hardcode the order for each option and check if it satisfies all constraints.

found_options = []

# Option A: H, S, J, Q, Y, G, R
solver.push()
order_A = [H, S, J, Q, Y, G, R]
for i in positions:
    solver.add(order[i] == order_A[i])

# Check constraints for Option A
# Constraint 1: Consecutive topics must differ
valid_A = True
for i in range(6):
    if topic(order[i]) == topic(order[i+1]):
        valid_A = False
        break

# Constraint 2: S before Q implies Q is third (position 2)
# In Option A: S is at position 1, Q is at position 3 -> S is before Q, but Q is not at position 2 -> invalid

# Constraint 3: S must be before Y
# In Option A: S is at position 1, Y is at position 4 -> valid

# Constraint 4: J before G before R
# In Option A: J is at position 2, G is at position 5, R is at position 6 -> valid

if valid_A and not (order_A.index(S) < order_A.index(Q) and order_A.index(Q) != 2) and (order_A.index(S) < order_A.index(Y)) and (order_A.index(J) < order_A.index(G) < order_A.index(R)):
    if solver.check() == sat:
        found_options.append("A")
else:
    pass
solver.pop()

# Option B: J, Q, G, H, S, Y, R
solver.push()
order_B = [J, Q, G, H, S, Y, R]
for i in positions:
    solver.add(order[i] == order_B[i])

# Check constraints for Option B
valid_B = True
for i in range(6):
    if topic(order[i]) == topic(order[i+1]):
        valid_B = False
        break

# Constraint 2: S before Q implies Q is third
# In Option B: Q is at position 1, S is at position 4 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option B: S is at position 4, Y is at position 5 -> valid

# Constraint 4: J before G before R
# In Option B: J is at position 0, G is at position 2, R is at position 6 -> valid

if valid_B and not (order_B.index(S) < order_B.index(Q) and order_B.index(Q) != 2) and (order_B.index(S) < order_B.index(Y)) and (order_B.index(J) < order_B.index(G) < order_B.index(R)):
    if solver.check() == sat:
        found_options.append("B")
else:
    pass
solver.pop()

# Option C: Q, J, S, H, Y, G, R
solver.push()
order_C = [Q, J, S, H, Y, G, R]
for i in positions:
    solver.add(order[i] == order_C[i])

# Check constraints for Option C
valid_C = True
for i in range(6):
    if topic(order[i]) == topic(order[i+1]):
        valid_C = False
        break

# Constraint 2: S before Q implies Q is third
# In Option C: S is at position 2, Q is at position 0 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option C: S is at position 2, Y is at position 4 -> valid

# Constraint 4: J before G before R
# In Option C: J is at position 1, G is at position 5, R is at position 6 -> valid

if valid_C and not (order_C.index(S) < order_C.index(Q) and order_C.index(Q) != 2) and (order_C.index(S) < order_C.index(Y)) and (order_C.index(J) < order_C.index(G) < order_C.index(R)):
    if solver.check() == sat:
        found_options.append("C")
else:
    pass
solver.pop()

# Option D: Q, J, Y, S, G, R, H
solver.push()
order_D = [Q, J, Y, S, G, R, H]
for i in positions:
    solver.add(order[i] == order_D[i])

# Check constraints for Option D
valid_D = True
for i in range(6):
    if topic(order[i]) == topic(order[i+1]):
        valid_D = False
        break

# Constraint 2: S before Q implies Q is third
# In Option D: S is at position 3, Q is at position 0 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option D: S is at position 3, Y is at position 2 -> S is not before Y -> invalid

# Constraint 4: J before G before R
# In Option D: J is at position 1, G is at position 4, R is at position 5 -> valid

if valid_D and not (order_D.index(S) < order_D.index(Q) and order_D.index(Q) != 2) and (order_D.index(S) < order_D.index(Y)) and (order_D.index(J) < order_D.index(G) < order_D.index(R)):
    if solver.check() == sat:
        found_options.append("D")
else:
    pass
solver.pop()

# Option E: S, G, Q, J, Y, R, H
solver.push()
order_E = [S, G, Q, J, Y, R, H]
for i in positions:
    solver.add(order[i] == order_E[i])

# Check constraints for Option E
valid_E = True
for i in range(6):
    if topic(order[i]) == topic(order[i+1]):
        valid_E = False
        break

# Constraint 2: S before Q implies Q is third
# In Option E: S is at position 0, Q is at position 2 -> S is before Q, and Q is at position 2 -> valid

# Constraint 3: S before Y
# In Option E: S is at position 0, Y is at position 4 -> valid

# Constraint 4: J before G before R
# In Option E: J is at position 3, G is at position 1, R is at position 5 -> J is not before G -> invalid

if valid_E and not (order_E.index(S) < order_E.index(Q) and order_E.index(Q) != 2) and (order_E.index(S) < order_E.index(Y)) and (order_E.index(J) < order_E.index(G) < order_E.index(R)):
    if solver.check() == sat:
        found_options.append("E")
else:
    pass
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")