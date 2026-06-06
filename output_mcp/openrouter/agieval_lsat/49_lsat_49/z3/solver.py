from z3 import *

# Create solver and variables
solver = Solver()
# Employees: Robertson (R), Souza (S), Togowa (T), Vaughn (V), Xu (X), Young (Y)
R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Domain constraints: each between 1 and 6
for e in employees:
    solver.add(e >= 1, e <= 6)
# All distinct
solver.add(Distinct(employees))

# Base rules
solver.add(Y > T)          # Young higher-numbered than Togowa
solver.add(X > S)          # Xu higher-numbered than Souza
solver.add(R > Y)          # Robertson higher-numbered than Young
solver.add(R <= 4)         # Robertson must be 1-4

# Question premise: Togowa higher-numbered than Souza
solver.add(T > S)

# Define option constraints
opt_a_constr = (Y == 2)          # A: Young is assigned parking space #2
opt_b_constr = (V == 5)          # B: Vaughn is assigned parking space #5
opt_c_constr = (T == 3)          # C: Togowa is assigned parking space #3
opt_d_constr = (S == 2)          # D: Souza is assigned parking space #2
opt_e_constr = (R == 3)          # E: Robertson is assigned parking space #3

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