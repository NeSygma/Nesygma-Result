from z3 import *

solver = Solver()

# Seven articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
# Position variables: 1-7
G, H, J = Ints('G H J')
Q, R, S = Ints('Q R S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]

# Each article gets a unique position from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)
solver.add(Distinct(articles))

# Topic assignments
finance = [G, H, J]
nutrition = [Q, R, S]
wildlife = [Y]

# Consecutive articles cannot cover the same topic
# For each pair of articles, if they are consecutive (diff == 1), they can't be same topic
for i in range(len(articles)):
    for j in range(i+1, len(articles)):
        a, b = articles[i], articles[j]
        # Check if they are consecutive
        consecutive = Or(a - b == 1, b - a == 1)
        # If consecutive, they must not be same topic
        # Same topic pairs: (G,H), (G,J), (H,J), (Q,R), (Q,S), (R,S)
        same_topic_pairs = [
            (G, H), (G, J), (H, J),
            (Q, R), (Q, S), (R, S)
        ]
        if (a, b) in same_topic_pairs or (b, a) in same_topic_pairs:
            solver.add(Implies(consecutive, False))  # They can't be consecutive

# S can be earlier than Q only if Q is third
# "S < Q" implies "Q == 3"
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Y is fourth
solver.add(Y == 4)

# Now check each option
found_options = []

# (A) J is second
solver.push()
solver.add(J == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) J is third
solver.push()
solver.add(J == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Q is first
solver.push()
solver.add(Q == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Q is third
solver.push()
solver.add(Q == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) R is seventh
solver.push()
solver.add(R == 7)
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