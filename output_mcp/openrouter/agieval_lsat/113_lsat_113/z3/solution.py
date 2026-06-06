from z3 import *

solver = Solver()
# Position variables for each article
G = Int('G')
H = Int('H')
J = Int('J')
Q = Int('Q')
R = Int('R')
S = Int('S')
Y = Int('Y')
positions = [G,H,J,Q,R,S,Y]
# Domain constraints: positions 1..7 and all distinct
for v in positions:
    solver.add(v >= 1, v <= 7)
solver.add(Distinct(positions))
# Base constraints
solver.add(J == 3)          # J is third
solver.add(J < G)           # J earlier than G
solver.add(G < R)           # G earlier than R
solver.add(S < Y)           # S earlier than Y
# Consecutive same-topic not allowed
finance = [G, H, J]
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Abs(finance[i] - finance[j]) != 1)
nutrition = [Q, R, S]
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Abs(nutrition[i] - nutrition[j]) != 1)
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(S < Q, Q == 3))

# Option constraints
opt_a = (G == 4)   # A: G is fourth
opt_b = (H == 6)   # B: H is sixth
opt_c = (Q == 1)   # C: Q is first
opt_d = (S == 2)   # D: S is second
opt_e = (Y == 5)   # E: Y is fifth

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