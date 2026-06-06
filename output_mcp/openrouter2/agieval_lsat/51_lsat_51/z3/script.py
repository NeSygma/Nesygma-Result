from z3 import *

# Enumerate all solutions of the base constraints
employees = ['Robertson','Souza','Togowa','Vaughn','Xu','Young']
# Create Int variables for each employee
robertson = Int('robertson')
souza = Int('souza')
togowa = Int('togowa')
vaughn = Int('vaughn')
# Use 'xu' for Xu
xu = Int('xu')
young = Int('young')

# Base solver for enumeration
solver_enum = Solver()
# Domain constraints
solver_enum.add(robertson >= 1, robertson <= 6)
solver_enum.add(souza >= 1, souza <= 6)
solver_enum.add(togowa >= 1, togowa <= 6)
solver_enum.add(vaughn >= 1, vaughn <= 6)
solver_enum.add(xu >= 1, xu <= 6)
solver_enum.add(young >= 1, young <= 6)
# Distinct
solver_enum.add(Distinct(robertson, souza, togowa, vaughn, xu, young))
# Additional constraints
solver_enum.add(young > togowa)
solver_enum.add(xu > souza)
solver_enum.add(robertson > young)
solver_enum.add(robertson <= 4)

# Enumerate all models
models = []
while solver_enum.check() == sat:
    m = solver_enum.model()
    assignment = {
        'Robertson': m[robertson].as_long(),
        'Souza': m[souza].as_long(),
        'Togowa': m[togowa].as_long(),
        'Vaughn': m[vaughn].as_long(),
        'Xu': m[xu].as_long(),
        'Young': m[young].as_long()
    }
    models.append(assignment)
    # Block this assignment
    solver_enum.add(Or([robertson != m[robertson], souza != m[souza], togowa != m[togowa], vaughn != m[vaughn], xu != m[xu], young != m[young]]))

# Compute possible values for each employee across all models
possible_values = {emp: set() for emp in employees}
for assignment in models:
    for emp in employees:
        possible_values[emp].add(assignment[emp])

# Count employees with exactly two possible values
count_two_possible = sum(1 for emp in employees if len(possible_values[emp]) == 2)

# Now create a new solver with base constraints and a dummy variable cnt
solver = Solver()
# Re-add base constraints
solver.add(robertson >= 1, robertson <= 6)
solver.add(souza >= 1, souza <= 6)
solver.add(togowa >= 1, togowa <= 6)
solver.add(vaughn >= 1, vaughn <= 6)
solver.add(xu >= 1, xu <= 6)
solver.add(young >= 1, young <= 6)
solver.add(Distinct(robertson, souza, togowa, vaughn, xu, young))
solver.add(young > togowa)
solver.add(xu > souza)
solver.add(robertson > young)
solver.add(robertson <= 4)

# Dummy variable cnt
cnt = Int('cnt')
solver.add(cnt == count_two_possible)

# Define option constraints
opt_a_constr = cnt == 0
opt_b_constr = cnt == 2
opt_c_constr = cnt == 3
opt_d_constr = cnt == 4
opt_e_constr = cnt == 5

# Skeleton for evaluating options
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