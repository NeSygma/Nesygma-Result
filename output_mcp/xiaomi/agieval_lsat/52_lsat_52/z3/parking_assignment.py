from z3 import *

solver = Solver()

# Declare parking space variables for each employee (1-6)
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

employees = [R, S, T, V, X, Y]

# Each employee gets a parking space 1-6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Base constraints from the problem
solver.add(Y > T)       # Young must be assigned a higher-numbered parking space than Togowa
solver.add(X > S)       # Xu must be assigned a higher-numbered parking space than Souza
solver.add(R > Y)       # Robertson must be assigned a higher-numbered parking space than Young
solver.add(And(R >= 1, R <= 4))  # Robertson must be assigned parking space #1, #2, #3, or #4

# Additional condition: Young is assigned a higher-numbered parking space than Souza
solver.add(Y > S)

# Define option constraints
opt_a_constr = (T == 1)           # Togowa is assigned parking space #1
opt_b_constr = (Y == 2)           # Young is assigned parking space #2
opt_c_constr = (R == 3)           # Robertson is assigned parking space #3
opt_d_constr = (S == 3)           # Souza is assigned parking space #3
opt_e_constr = (V == 4)           # Vaughn is assigned parking space #4

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