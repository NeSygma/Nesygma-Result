from z3 import *

solver = Solver()
# Variables for each employee
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young
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
solver.add(Or(R == 1, R == 2, R == 3, R == 4))  # Robertson in 1..4
# Given condition: Robertson assigned #3
solver.add(R == 3)

# Define option constraints (the statement that the option claims)
opt_a = S == 4
opt_b = T == 2
opt_c = V == 5
opt_d = X == 6
opt_e = Y == 2

found_options = []
for letter, opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # To test if option must be true, add its negation and see if unsat
    solver.add(Not(opt))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No option is forced")