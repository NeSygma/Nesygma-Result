from z3 import *

solver = Solver()

# Variables for positions
G = Int('G')
H = Int('H')
J = Int('J')
Q = Int('Q')
R = Int('R')
S = Int('S')
Y = Int('Y')
articles = [G, H, J, Q, R, S, Y]

# Domain constraints
for a in articles:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(articles))

# Consecutive articles cannot cover same topic
# Finance: G, H, J
finance = [G, H, J]
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Abs(finance[i] - finance[j]) != 1)
# Nutrition: Q, R, S
nutrition = [Q, R, S]
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Abs(nutrition[i] - nutrition[j]) != 1)

# S can be earlier than Q only if Q is third
solver.add(Implies(S < Q, Q == 3))
# S earlier than Y
solver.add(S < Y)
# J earlier than G
solver.add(J < G)
# G earlier than R
solver.add(G < R)
# Y is fourth
solver.add(Y == 4)

# Option constraints
opt_a_constr = (J == 2)
opt_b_constr = (J == 3)
opt_c_constr = (Q == 1)
opt_d_constr = (Q == 3)
opt_e_constr = (R == 7)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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