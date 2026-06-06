from z3 import *

solver = Solver()

# Articles and their positions (1-7)
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
articles = [G, H, J, Q, R, S, Y]

# Each article gets a unique position from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)
solver.add(Distinct(articles))

# Topics: G,H,J = finance (0); Q,R,S = nutrition (1); Y = wildlife (2)
# We'll track topic by article name
# finance = {G, H, J}, nutrition = {Q, R, S}, wildlife = {Y}

# Constraint 1: Consecutive articles cannot cover the same topic
# For each pair of positions p and p+1, the articles at those positions
# must not be from the same topic group.
# We need: for each position p (1..6), the article at p and p+1 differ in topic.
# Use helper: topic_of(article) - but we need to express this symbolically.

# Better approach: for each pair of articles that share a topic,
# they cannot be in consecutive positions.
# Finance pairs: (G,H), (G,J), (H,J)
# Nutrition pairs: (Q,R), (Q,S), (R,S)
# Wildlife: only Y, so no constraint needed.

def not_consecutive(a1, a2):
    return And(a1 - a2 != 1, a1 - a2 != -1)

# Finance articles can't be consecutive with each other
solver.add(not_consecutive(G, H))
solver.add(not_consecutive(G, J))
solver.add(not_consecutive(H, J))

# Nutrition articles can't be consecutive with each other
solver.add(not_consecutive(Q, R))
solver.add(not_consecutive(Q, S))
solver.add(not_consecutive(R, S))

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q, then Q == 3
# Equivalently: Or(S >= Q, Q == 3)
solver.add(Or(S >= Q, Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(S < Y)

# Constraint 4: J < G and G < R
solver.add(J < G)
solver.add(G < R)

# Additional condition: J is third
solver.add(J == 3)

# Now test each answer choice
# (A) G is fourth
# (B) H is sixth
# (C) Q is first
# (D) S is second
# (E) Y is fifth

found_options = []

# Option A: G is fourth
solver.push()
solver.add(G == 4)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is sixth
solver.push()
solver.add(H == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
solver.push()
solver.add(Q == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is fifth
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

# Also print a full model for the correct option for verification
print("\n--- Verification ---")
solver.push()
# Add the correct option constraint to show a full model
if len(found_options) == 1:
    opt = found_options[0]
    if opt == "A":
        solver.add(G == 4)
    elif opt == "B":
        solver.add(H == 6)
    elif opt == "C":
        solver.add(Q == 1)
    elif opt == "D":
        solver.add(S == 2)
    elif opt == "E":
        solver.add(Y == 5)
    if solver.check() == sat:
        m = solver.model()
        pos = {}
        for name, var in [("G", G), ("H", H), ("J", J), ("Q", Q), ("R", R), ("S", S), ("Y", Y)]:
            pos[m[var].as_long()] = name
        print("Order:", [pos[i] for i in range(1, 8)])
solver.pop()