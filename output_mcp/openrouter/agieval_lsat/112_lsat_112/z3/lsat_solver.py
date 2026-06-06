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

# Domain constraints: positions 1..7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All positions distinct
solver.add(Distinct(articles))

# Consecutive articles cannot cover same topic: enforce distance != 1 for same-topic pairs
finance = [G, H, J]
nutrition = [Q, R, S]
# finance pairs
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Abs(finance[i] - finance[j]) != 1)
# nutrition pairs
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Abs(nutrition[i] - nutrition[j]) != 1)

# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(S < Q, Q == 3))
# S earlier than Y
solver.add(S < Y)
# J earlier than G
solver.add(J < G)
# G earlier than R
solver.add(G < R)

# Define option constraints
opt_a = G == 2          # A: G is second
opt_b = H == 2          # B: H is second
opt_c = S == 2          # C: S is second
opt_d = R == 3          # D: R is third
opt_e = Y == 3          # E: Y is third

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
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