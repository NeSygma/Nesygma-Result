from z3 import *

solver = Solver()

# Declare variables for each employee's parking space number
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

# Base constraints: each space between 1 and 6
solver.add(R >= 1, R <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)

# All spaces distinct
solver.add(Distinct([R, S, T, V, X, Y]))

# Rule constraints
solver.add(Y > T)          # Young higher than Togowa
solver.add(X > S)          # Xu higher than Souza
solver.add(R > Y)          # Robertson higher than Young
solver.add(R <= 4)         # Robertson in #1-#4

# Define option constraints
opt_a_constr = And(Y == 1, S == 2, V == 3, R == 4, T == 5, X == 6)
opt_b_constr = And(V == 1, T == 2, Y == 3, S == 4, R == 5, X == 6)
opt_c_constr = And(T == 1, Y == 2, X == 3, R == 4, S == 5, V == 6)
opt_d_constr = And(T == 1, R == 2, Y == 3, S == 4, V == 5, X == 6)
opt_e_constr = And(S == 1, T == 2, Y == 3, R == 4, X == 5, V == 6)

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