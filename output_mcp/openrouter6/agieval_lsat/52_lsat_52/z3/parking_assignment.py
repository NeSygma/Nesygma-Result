from z3 import *

solver = Solver()

# Declare variables for each employee's parking space number
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

# Base constraints
# 1. Young > Togowa
solver.add(Y > T)
# 2. Xu > Souza
solver.add(X > S)
# 3. Robertson > Young
solver.add(R > Y)
# 4. Robertson must be assigned a parking space #1, #2, #3, or #4
solver.add(R <= 4)
# 5. All parking spaces are between 1 and 6
solver.add(R >= 1, R <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)
# 6. All employees have distinct parking spaces
solver.add(Distinct([R, S, T, V, X, Y]))

# Extra condition from the question: Young > Souza
solver.add(Y > S)

# Now evaluate each option
found_options = []

# Option A: Togowa is assigned parking space #1
opt_a_constr = (T == 1)
# Option B: Young is assigned parking space #2
opt_b_constr = (Y == 2)
# Option C: Robertson is assigned parking space #3
opt_c_constr = (R == 3)
# Option D: Souza is assigned parking space #3
opt_d_constr = (S == 3)
# Option E: Vaughn is assigned parking space #4
opt_e_constr = (V == 4)

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