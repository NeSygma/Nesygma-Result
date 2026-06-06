from z3 import *

solver = Solver()

# Seven articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
# Position variables: 1-7
G, H, J = Ints('G H J')
Q, R, S = Ints('Q R S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]

# Each article is in a position 1-7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All different positions
solver.add(Distinct(articles))

# Topic assignments
finance = [G, H, J]
nutrition = [Q, R, S]
wildlife = [Y]

# Consecutive articles cannot cover the same topic
# For each pair of articles, if they are consecutive (diff == 1), they can't be same topic
for i in range(len(articles)):
    for j in range(i+1, len(articles)):
        # Check if they are consecutive
        consec = Or(articles[i] - articles[j] == 1, articles[j] - articles[i] == 1)
        # If consecutive, they must not be same topic
        # Finance articles: G, H, J
        # Nutrition articles: Q, R, S
        # Wildlife: Y
        same_finance = Or(
            And(articles[i] == G, articles[j] == H),
            And(articles[i] == G, articles[j] == J),
            And(articles[i] == H, articles[j] == G),
            And(articles[i] == H, articles[j] == J),
            And(articles[i] == J, articles[j] == G),
            And(articles[i] == J, articles[j] == H)
        )
        same_nutrition = Or(
            And(articles[i] == Q, articles[j] == R),
            And(articles[i] == Q, articles[j] == S),
            And(articles[i] == R, articles[j] == Q),
            And(articles[i] == R, articles[j] == S),
            And(articles[i] == S, articles[j] == Q),
            And(articles[i] == S, articles[j] == R)
        )
        # Y is alone in wildlife, so no same-topic conflict with Y
        solver.add(Implies(consec, Not(Or(same_finance, same_nutrition))))

# S can be earlier than Q only if Q is third
# Equivalently: if S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Additional condition: J is third
solver.add(J == 3)

# Now test each option
found_options = []

# (A) G is fourth
solver.push()
solver.add(G == 4)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) H is sixth
solver.push()
solver.add(H == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Q is first
solver.push()
solver.add(Q == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) S is second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Y is fifth
solver.push()
solver.add(Y == 5)
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