from z3 import *

# Declare position variables for each article (1..7)
G = Int('G')
H = Int('H')
J = Int('J')
Q = Int('Q')
R = Int('R')
S = Int('S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]
solver = Solver()
# Domain constraints
for a in articles:
    solver.add(a >= 1, a <= 7)
# All-different positions
solver.add(Distinct(articles))
# Base constraints
solver.add(G == 4)  # G is fourth
# Consecutive articles cannot cover same topic: enforce non-consecutive for same-topic pairs
# Finance pairs
solver.add(Abs(G - H) != 1)
solver.add(Abs(G - J) != 1)
solver.add(Abs(H - J) != 1)
# Nutrition pairs
solver.add(Abs(Q - R) != 1)
solver.add(Abs(Q - S) != 1)
solver.add(Abs(R - S) != 1)
# S earlier than Y
solver.add(S < Y)
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(S < Q, Q == 3))
# J earlier than G
solver.add(J < G)
# G earlier than R
solver.add(G < R)

# Define option constraints
option_constraints = []
# A: H is fifth
opt_a = (H == 5)
option_constraints.append(("A", opt_a))
# B: J is first
opt_b = (J == 1)
option_constraints.append(("B", opt_b))
# C: Q is second
opt_c = (Q == 2)
option_constraints.append(("C", opt_c))
# D: S is fifth
opt_d = (S == 5)
option_constraints.append(("D", opt_d))
# E: Y is sixth
opt_e = (Y == 6)
option_constraints.append(("E", opt_e))

found_options = []
for letter, constr in option_constraints:
    solver.push()
    solver.add(constr)
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