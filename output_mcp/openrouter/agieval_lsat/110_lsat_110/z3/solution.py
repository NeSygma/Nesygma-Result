from z3 import *

solver = Solver()
# Variables for positions 1..7
G = Int('G')
H = Int('H')
J = Int('J')
Q = Int('Q')
R = Int('R')
S = Int('S')
Y = Int('Y')
positions = [G,H,J,Q,R,S,Y]
# domain 1..7
for v in positions:
    solver.add(v >= 1, v <= 7)
# all distinct
solver.add(Distinct(positions))
# consecutive articles cannot cover same topic
# finance: G,H,J
solver.add(Abs(G - H) != 1)
solver.add(Abs(G - J) != 1)
solver.add(Abs(H - J) != 1)
# nutrition: Q,R,S
solver.add(Abs(Q - R) != 1)
solver.add(Abs(Q - S) != 1)
solver.add(Abs(R - S) != 1)
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(S < Q, Q == 3))
# S earlier than Y
solver.add(S < Y)
# J earlier than G
solver.add(J < G)
# G earlier than R
solver.add(G < R)
# Y is fourth
solver.add(Y == 4)

# Define option constraints
opt_a = (J == 2)
opt_b = (J == 3)
opt_c = (Q == 1)
opt_d = (Q == 3)
opt_e = (R == 7)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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