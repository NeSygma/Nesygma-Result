from z3 import *

# Define cargo indices
cargo_names = ['fuel','grain','livestock','machinery','produce','textiles']
indices = {name:i for i,name in enumerate(cargo_names)}

# Bay variables: bay_1 ... bay_6 represent cargo index at that bay
bay = [Int(f'bay_{i}') for i in range(1,7)]

solver = Solver()
# Distinct cargo in each bay
solver.add(Distinct(bay))
# Each bay holds a cargo index 0..5
for b in bay:
    solver.add(b >= 0, b <= 5)
# Bay 4 holds produce
solver.add(bay[3] == indices['produce'])

grain = indices['grain']
livestock = indices['livestock']
textiles = indices['textiles']
fuel = indices['fuel']

# Constraints: grain bay number > livestock bay number
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(bay[i]==grain, bay[j]==livestock), (i+1) > (j+1)))
# livestock > textiles
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(bay[i]==livestock, bay[j]==textiles), (i+1) > (j+1)))
# produce > fuel
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(bay[i]==indices['produce'], bay[j]==fuel), (i+1) > (j+1)))
# textiles adjacent to produce (bay 4)
for i in range(6):
    solver.add(Implies(bay[i]==textiles, Or(i+1==3, i+1==5)))

# Enumerate all models
all_assignments = []
while solver.check() == sat:
    m = solver.model()
    assignment = [m[bay[i]].as_long() for i in range(6)]
    all_assignments.append(assignment)
    # block this model
    solver.add(Or([bay[i] != assignment[i] for i in range(6)]))

# Determine which bays have a unique cargo across all assignments
determined = 0
for i in range(6):
    cargos = set(assign[i] for assign in all_assignments)
    if len(cargos) == 1:
        determined += 1

# Now set constraints for each answer choice
opt_a_constr = BoolVal(determined == 2)
opt_b_constr = BoolVal(determined == 3)
opt_c_constr = BoolVal(determined == 4)
opt_d_constr = BoolVal(determined == 5)
opt_e_constr = BoolVal(determined == 6)

# Use the required skeleton
solver = Solver()
# No base constraints needed for the skeleton, just test each option
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