from z3 import *

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Spaces: #1 through #6
# We'll assign each employee a space number (1-6), all distinct.

# Create integer variables for each employee's space
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]

solver = Solver()

# Domain: each space is 1 to 6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All distinct
solver.add(Distinct(employees))

# Constraints:
# Young must be assigned a higher-numbered parking space than Togowa.
solver.add(Young > Togowa)

# Xu must be assigned a higher-numbered parking space than Souza.
solver.add(Xu > Souza)

# Robertson must be assigned a higher-numbered parking space than Young.
solver.add(Robertson > Young)

# Robertson must be assigned parking space #1, #2, #3, or #4.
solver.add(Or(Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4))

# Now evaluate each option
# Each option gives a mapping from space number to employee.
# We'll encode each option as: for each space number, the employee assigned to it must equal that space number.

# Option A: #1: Young; #2: Souza; #3: Vaughn; #4: Robertson; #5: Togowa; #6: Xu
opt_a = And(
    Young == 1,
    Souza == 2,
    Vaughn == 3,
    Robertson == 4,
    Togowa == 5,
    Xu == 6
)

# Option B: #1: Vaughn; #2: Togowa; #3: Young; #4: Souza; #5: Robertson; #6: Xu
opt_b = And(
    Vaughn == 1,
    Togowa == 2,
    Young == 3,
    Souza == 4,
    Robertson == 5,
    Xu == 6
)

# Option C: #1: Togowa; #2: Young; #3: Xu; #4: Robertson; #5: Souza; #6: Vaughn
opt_c = And(
    Togowa == 1,
    Young == 2,
    Xu == 3,
    Robertson == 4,
    Souza == 5,
    Vaughn == 6
)

# Option D: #1: Togowa; #2: Robertson; #3: Young; #4: Souza; #5: Vaughn; #6: Xu
opt_d = And(
    Togowa == 1,
    Robertson == 2,
    Young == 3,
    Souza == 4,
    Vaughn == 5,
    Xu == 6
)

# Option E: #1: Souza; #2: Togowa; #3: Young; #4: Robertson; #5: Xu; #6: Vaughn
opt_e = And(
    Souza == 1,
    Togowa == 2,
    Young == 3,
    Robertson == 4,
    Xu == 5,
    Vaughn == 6
)

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