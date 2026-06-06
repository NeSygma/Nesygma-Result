from z3 import *

# Define the articles and positions as symbolic constants
Article = EnumSort('Article', ['G', 'H', 'J', 'Q', 'R', 'S', 'Y'])
Position = EnumSort('Position', ['pos0', 'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6'])

G, H, J, Q, R, S, Y = Article
pos0, pos1, pos2, pos3, pos4, pos5, pos6 = Position

# Helper: Map article to its topic
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
def topic(article):
    if article == G or article == H or article == J:
        return "finance"
    elif article == Q or article == R or article == S:
        return "nutrition"
    elif article == Y:
        return "wildlife"
    else:
        return None

# Base solver for the general constraints
solver = Solver()

# Assign each position to an article
# We will use a function: position -> article
position_to_article = Function('position_to_article', Position, Article)

# Each position must be assigned exactly one article
for p in [pos0, pos1, pos2, pos3, pos4, pos5, pos6]:
    solver.add(position_to_article(p) == G)
    solver.add(position_to_article(p) == H)
    solver.add(position_to_article(p) == J)
    solver.add(position_to_article(p) == Q)
    solver.add(position_to_article(p) == R)
    solver.add(position_to_article(p) == S)
    solver.add(position_to_article(p) == Y)
    # This is not correct. Instead, we need to ensure that all articles are used exactly once.

# Instead, let's use a list of articles and ensure all are used exactly once.
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct([position_to_article(p) for p in [pos0, pos1, pos2, pos3, pos4, pos5, pos6]]))

# Constraint 1: Consecutive articles cannot cover the same topic
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    solver.add(Not(topic(position_to_article(p1)) == topic(position_to_article(p2))))

# Constraint 2: S can be earlier than Q only if Q is third (pos2)
# This means: if S is before Q, then Q must be at pos2
# We will handle this in the option evaluation.

# Constraint 3: S must be earlier than Y
# Constraint 4: J must be earlier than G, and G must be earlier than R

# For the multiple-choice evaluation, we will hardcode the order for each option and check if it satisfies all constraints.

# We will now evaluate each option (A-E) by hardcoding the order and checking constraints.

found_options = []

# Option A: H, S, J, Q, Y, G, R
solver.push()
order_A = [H, S, J, Q, Y, G, R]
for i, p in enumerate([pos0, pos1, pos2, pos3, pos4, pos5, pos6]):
    solver.add(position_to_article(p) == order_A[i])

# Check constraints for Option A
# Constraint 1: Consecutive topics must differ
valid_A = True
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    if topic(position_to_article(p1)) == topic(position_to_article(p2)):
        valid_A = False
        break

# Constraint 2: S before Q implies Q is third (pos2)
# In Option A: S is at pos1, Q is at pos3 -> S is before Q, but Q is not third -> invalid

# Constraint 3: S must be before Y
# In Option A: S is at pos1, Y is at pos4 -> valid

# Constraint 4: J before G before R
# In Option A: J is at pos2, G is at pos5, R is at pos6 -> valid

if valid_A and not (order_A.index(S) < order_A.index(Q) and order_A.index(Q) != 2) and (order_A.index(S) < order_A.index(Y)) and (order_A.index(J) < order_A.index(G) < order_A.index(R)):
    if solver.check() == sat:
        found_options.append("A")
else:
    pass
solver.pop()

# Option B: J, Q, G, H, S, Y, R
solver.push()
order_B = [J, Q, G, H, S, Y, R]
for i, p in enumerate([pos0, pos1, pos2, pos3, pos4, pos5, pos6]):
    solver.add(position_to_article(p) == order_B[i])

# Check constraints for Option B
valid_B = True
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    if topic(position_to_article(p1)) == topic(position_to_article(p2)):
        valid_B = False
        break

# Constraint 2: S before Q implies Q is third
# In Option B: Q is at pos1, S is at pos4 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option B: S is at pos4, Y is at pos5 -> valid

# Constraint 4: J before G before R
# In Option B: J is at pos0, G is at pos2, R is at pos6 -> valid

if valid_B and not (order_B.index(S) < order_B.index(Q) and order_B.index(Q) != 2) and (order_B.index(S) < order_B.index(Y)) and (order_B.index(J) < order_B.index(G) < order_B.index(R)):
    if solver.check() == sat:
        found_options.append("B")
else:
    pass
solver.pop()

# Option C: Q, J, S, H, Y, G, R
solver.push()
order_C = [Q, J, S, H, Y, G, R]
for i, p in enumerate([pos0, pos1, pos2, pos3, pos4, pos5, pos6]):
    solver.add(position_to_article(p) == order_C[i])

# Check constraints for Option C
valid_C = True
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    if topic(position_to_article(p1)) == topic(position_to_article(p2)):
        valid_C = False
        break

# Constraint 2: S before Q implies Q is third
# In Option C: S is at pos2, Q is at pos0 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option C: S is at pos2, Y is at pos4 -> valid

# Constraint 4: J before G before R
# In Option C: J is at pos1, G is at pos5, R is at pos6 -> valid

if valid_C and not (order_C.index(S) < order_C.index(Q) and order_C.index(Q) != 2) and (order_C.index(S) < order_C.index(Y)) and (order_C.index(J) < order_C.index(G) < order_C.index(R)):
    if solver.check() == sat:
        found_options.append("C")
else:
    pass
solver.pop()

# Option D: Q, J, Y, S, G, R, H
solver.push()
order_D = [Q, J, Y, S, G, R, H]
for i, p in enumerate([pos0, pos1, pos2, pos3, pos4, pos5, pos6]):
    solver.add(position_to_article(p) == order_D[i])

# Check constraints for Option D
valid_D = True
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    if topic(position_to_article(p1)) == topic(position_to_article(p2)):
        valid_D = False
        break

# Constraint 2: S before Q implies Q is third
# In Option D: S is at pos3, Q is at pos0 -> S is not before Q -> valid

# Constraint 3: S before Y
# In Option D: S is at pos3, Y is at pos2 -> S is not before Y -> invalid

# Constraint 4: J before G before R
# In Option D: J is at pos1, G is at pos4, R is at pos5 -> valid

if valid_D and not (order_D.index(S) < order_D.index(Q) and order_D.index(Q) != 2) and (order_D.index(S) < order_D.index(Y)) and (order_D.index(J) < order_D.index(G) < order_D.index(R)):
    if solver.check() == sat:
        found_options.append("D")
else:
    pass
solver.pop()

# Option E: S, G, Q, J, Y, R, H
solver.push()
order_E = [S, G, Q, J, Y, R, H]
for i, p in enumerate([pos0, pos1, pos2, pos3, pos4, pos5, pos6]):
    solver.add(position_to_article(p) == order_E[i])

# Check constraints for Option E
valid_E = True
for i in range(6):
    p1 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i]
    p2 = [pos0, pos1, pos2, pos3, pos4, pos5, pos6][i+1]
    if topic(position_to_article(p1)) == topic(position_to_article(p2)):
        valid_E = False
        break

# Constraint 2: S before Q implies Q is third
# In Option E: S is at pos0, Q is at pos2 -> S is before Q, and Q is at position 2 (pos2) -> valid

# Constraint 3: S before Y
# In Option E: S is at pos0, Y is at pos4 -> valid

# Constraint 4: J before G before R
# In Option E: J is at pos3, G is at pos1, R is at pos5 -> J is not before G -> invalid

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