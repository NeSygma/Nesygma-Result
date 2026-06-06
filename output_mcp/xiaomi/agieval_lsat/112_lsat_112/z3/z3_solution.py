from z3 import *

solver = Solver()

# Seven articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
# Position variables: 1 through 7
G = Int('G')
H = Int('H')
J = Int('J')
Q = Int('Q')
R = Int('R')
S = Int('S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]

# Each article is assigned a position from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All articles are in distinct positions
solver.add(Distinct(articles))

# Topics: G,H,J = finance; Q,R,S = nutrition; Y = wildlife
# Consecutive articles cannot cover the same topic
# Finance-Finance consecutive forbidden: G-H, G-J, H-G, H-J, J-G, J-H
# Nutrition-Nutrition consecutive forbidden: Q-R, Q-S, R-Q, R-S, S-Q, S-R

def not_consecutive(a, b):
    """a and b are not in consecutive positions"""
    return And(a - b != 1, b - a != 1)

# Finance pairs
solver.add(not_consecutive(G, H))
solver.add(not_consecutive(G, J))
solver.add(not_consecutive(H, J))

# Nutrition pairs
solver.add(not_consecutive(Q, R))
solver.add(not_consecutive(Q, S))
solver.add(not_consecutive(R, S))

# S can be earlier than Q only if Q is third
# Equivalently: if S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now test each option
found_options = []

# (A) G is second
solver.push()
solver.add(G == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) H is second
solver.push()
solver.add(H == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) S is second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) R is third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Y is third
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