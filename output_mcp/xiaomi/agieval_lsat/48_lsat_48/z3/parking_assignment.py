from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: 1-6
# Each employee gets a unique parking space

R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Each assigned a space 1-6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Constraints:
# Young must be assigned a higher-numbered parking space than Togowa
solver.add(Y > T)

# Xu must be assigned a higher-numbered parking space than Souza
solver.add(X > S)

# Robertson must be assigned a higher-numbered parking space than Young
solver.add(R > Y)

# Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(R <= 4)

# Define each option as a complete assignment
# Option A: #1: Young; #2: Souza; #3: Vaughn; #4: Robertson; #5: Togowa; #6: Xu
opt_a = And(Y == 1, S == 2, V == 3, R == 4, T == 5, X == 6)

# Option B: #1: Vaughn; #2: Togowa; #3: Young; #4: Souza; #5: Robertson; #6: Xu
opt_b = And(V == 1, T == 2, Y == 3, S == 4, R == 5, X == 6)

# Option C: #1: Togowa; #2: Young; #3: Xu; #4: Robertson; #5: Souza; #6: Vaughn
opt_c = And(T == 1, Y == 2, X == 3, R == 4, S == 5, V == 6)

# Option D: #1: Togowa; #2: Robertson; #3: Young; #4: Souza; #5: Vaughn; #6: Xu
opt_d = And(T == 1, R == 2, Y == 3, S == 4, V == 5, X == 6)

# Option E: #1: Souza; #2: Togowa; #3: Young; #4: Robertson; #5: Xu; #6: Vaughn
opt_e = And(S == 1, T == 2, Y == 3, R == 4, X == 5, V == 6)

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