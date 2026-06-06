from z3 import *

solver = Solver()

# Declare variables for each employee
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

# Domain constraints: each parking space between 1 and 6
solver.add(R >= 1, R <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)

# All distinct
solver.add(Distinct(R, S, T, V, X, Y))

# Rule 1: Young must be assigned a higher-numbered parking space than Togowa
solver.add(Y > T)

# Rule 2: Xu must be assigned a higher-numbered parking space than Souza
solver.add(X > S)

# Rule 3: Robertson must be assigned a higher-numbered parking space than Young
solver.add(R > Y)

# Rule 4: Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or(R == 1, R == 2, R == 3, R == 4))

# Additional condition: Robertson is assigned parking space #3
solver.add(R == 3)

# Now evaluate each answer choice
found_options = []

# Option A: Souza is assigned parking space #4
opt_a_constr = (S == 4)
# Option B: Togowa is assigned parking space #2
opt_b_constr = (T == 2)
# Option C: Vaughn is assigned parking space #5
opt_c_constr = (V == 5)
# Option D: Xu is assigned parking space #6
opt_d_constr = (X == 6)
# Option E: Young is assigned parking space #2
opt_e_constr = (Y == 2)

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