from z3 import *

solver = Solver()

# Variables for each employee: the parking space number (1-6)
R, S, T, V, X, Y = Ints('R S T V X Y')

# Domain: each must be between 1 and 6
for emp in [R, S, T, V, X, Y]:
    solver.add(emp >= 1, emp <= 6)

# All distinct
solver.add(Distinct(R, S, T, V, X, Y))

# Rules
solver.add(Y > T)                     # Young > Togowa
solver.add(X > S)                     # Xu > Souza
solver.add(R > Y)                     # Robertson > Young
solver.add(Or([R == i for i in [1,2,3,4]]))  # Robertson in {1,2,3,4}

# Now define each option's constraints
# Option A: #1:Young, #2:Souza, #3:Vaughn, #4:Robertson, #5:Togowa, #6:Xu
opt_a = And(Y == 1, S == 2, V == 3, R == 4, T == 5, X == 6)

# Option B: #1:Vaughn, #2:Togowa, #3:Young, #4:Souza, #5:Robertson, #6:Xu
opt_b = And(V == 1, T == 2, Y == 3, S == 4, R == 5, X == 6)

# Option C: #1:Togowa, #2:Young, #3:Xu, #4:Robertson, #5:Souza, #6:Vaughn
opt_c = And(T == 1, Y == 2, X == 3, R == 4, S == 5, V == 6)

# Option D: #1:Togowa, #2:Robertson, #3:Young, #4:Souza, #5:Vaughn, #6:Xu
opt_d = And(T == 1, R == 2, Y == 3, S == 4, V == 5, X == 6)

# Option E: #1:Souza, #2:Togowa, #3:Young, #4:Robertson, #5:Xu, #6:Vaughn
opt_e = And(S == 1, T == 2, Y == 3, R == 4, X == 5, V == 6)

# Evaluate each option
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