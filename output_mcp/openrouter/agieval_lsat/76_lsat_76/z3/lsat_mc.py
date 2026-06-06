from z3 import *

# Define constants for business types
OPT = 0
PH = 1
REST = 2
SHOE = 3
TOY = 4
VET = 5

# Create position variables for spaces 1..7 (indices 0..6)
pos = [Int(f'p{i}') for i in range(7)]
solver = Solver()

# Domain constraints: each position must be one of the six types
for i in range(7):
    solver.add(And(pos[i] >= 0, pos[i] <= 5))

# Count constraints: exactly one optometrist, one pharmacy, two restaurants, one shoe store, one toy store, one veterinarian
solver.add(Sum([If(pos[i] == OPT, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == PH, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == REST, 1, 0) for i in range(7)]) == 2)
solver.add(Sum([If(pos[i] == SHOE, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == TOY, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == VET, 1, 0) for i in range(7)]) == 1)

# Constraint 1: Pharmacy at one end, a restaurant at the other end
solver.add(Or(And(pos[0] == PH, pos[6] == REST), And(pos[6] == PH, pos[0] == REST)))

# Constraint 2: Restaurants separated by at least two other businesses (distance >=3)
for i in range(7):
    for j in range(i+1, min(i+3, 7)):
        solver.add(Not(And(pos[i] == REST, pos[j] == REST)))

# Constraint 3: Pharmacy must be next to either the optometrist or the veterinarian
for i in range(7):
    # If pharmacy is at position i, then at least one neighbor is optometrist or veterinarian
    neighbor_opts = []
    if i > 0:
        neighbor_opts.append(Or(pos[i-1] == OPT, pos[i-1] == VET))
    if i < 6:
        neighbor_opts.append(Or(pos[i+1] == OPT, pos[i+1] == VET))
    if neighbor_opts:
        solver.add(Implies(pos[i] == PH, Or(neighbor_opts)))

# Constraint 4: Toy store cannot be next to the veterinarian
for i in range(6):
    solver.add(Not(And(pos[i] == TOY, pos[i+1] == VET)))
    solver.add(Not(And(pos[i] == VET, pos[i+1] == TOY)))

# Define option constraints
opt_a = And([pos[0] == PH,
              pos[1] == OPT,
              pos[2] == SHOE,
              pos[3] == REST,
              pos[4] == VET,
              pos[5] == TOY,
              pos[6] == REST])
opt_b = And([pos[0] == PH,
              pos[1] == VET,
              pos[2] == OPT,
              pos[3] == SHOE,
              pos[4] == REST,
              pos[5] == TOY,
              pos[6] == REST])
opt_c = And([pos[0] == REST,
              pos[1] == SHOE,
              pos[2] == VET,
              pos[3] == PH,
              pos[4] == OPT,
              pos[5] == TOY,
              pos[6] == REST])
opt_d = And([pos[0] == REST,
              pos[1] == TOY,
              pos[2] == OPT,
              pos[3] == REST,
              pos[4] == VET,
              pos[5] == SHOE,
              pos[6] == PH])
opt_e = And([pos[0] == REST,
              pos[1] == OPT,
              pos[2] == TOY,
              pos[3] == REST,
              pos[4] == SHOE,
              pos[5] == VET,
              pos[6] == PH])

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