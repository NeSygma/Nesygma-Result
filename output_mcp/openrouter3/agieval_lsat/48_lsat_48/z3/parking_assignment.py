from z3 import *

# Declare symbolic variables for each employee's parking space
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

# Create solver
solver = Solver()

# Add base constraints
# Each employee assigned to a unique parking space (1-6)
employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
for emp in employees:
    solver.add(emp >= 1, emp <= 6)

# All different
solver.add(Distinct(employees))

# Constraint 1: Young > Togowa
solver.add(Young > Togowa)

# Constraint 2: Xu > Souza
solver.add(Xu > Souza)

# Constraint 3: Robertson > Young
solver.add(Robertson > Young)

# Constraint 4: Robertson ∈ {1,2,3,4}
solver.add(Or(Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4))

# Define option constraints
# Option A: #1: Young; #2: Souza; #3: Vaughn; #4: Robertson; #5: Togowa; #6: Xu
opt_a_constr = And(
    Young == 1,
    Souza == 2,
    Vaughn == 3,
    Robertson == 4,
    Togowa == 5,
    Xu == 6
)

# Option B: #1: Vaughn; #2: Togowa; #3: Young; #4: Souza; #5: Robertson; #6: Xu
opt_b_constr = And(
    Vaughn == 1,
    Togowa == 2,
    Young == 3,
    Souza == 4,
    Robertson == 5,
    Xu == 6
)

# Option C: #1: Togowa; #2: Young; #3: Xu; #4: Robertson; #5: Souza; #6: Vaughn
opt_c_constr = And(
    Togowa == 1,
    Young == 2,
    Xu == 3,
    Robertson == 4,
    Souza == 5,
    Vaughn == 6
)

# Option D: #1: Togowa; #2: Robertson; #3: Young; #4: Souza; #5: Vaughn; #6: Xu
opt_d_constr = And(
    Togowa == 1,
    Robertson == 2,
    Young == 3,
    Souza == 4,
    Vaughn == 5,
    Xu == 6
)

# Option E: #1: Souza; #2: Togowa; #3: Young; #4: Robertson; #5: Xu; #6: Vaughn
opt_e_constr = And(
    Souza == 1,
    Togowa == 2,
    Young == 3,
    Robertson == 4,
    Xu == 5,
    Vaughn == 6
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")