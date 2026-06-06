from z3 import *

# Mapping cargo types to integers
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
# indices: 0 fuel,1 grain,2 livestock,3 machinery,4 produce,5 textiles

# Declare variables for each bay (1..6)
bay = [Int(f'bay_{i}') for i in range(1, 7)]  # bay[0] corresponds to bay 1

solver = Solver()
# Each bay holds a cargo type in 0..5
for b in bay:
    solver.add(b >= 0, b <= 5)
# All different
solver.add(Distinct(bay))

# Constraints from problem
# grain > livestock
# livestock > textiles
# produce > fuel
# textiles adjacent to produce
# produce at bay 4

# Helper to get index of cargo type
fuel = cargo_types.index('fuel')
gr = cargo_types.index('grain')
liv = cargo_types.index('livestock')
mach = cargo_types.index('machinery')
prod = cargo_types.index('produce')
text = cargo_types.index('textiles')

# grain > livestock
# find bay positions: we need positions of each cargo type. Use Or constraints linking cargo to bay.
# We'll create position variables for each cargo type.
pos = [Int(f'pos_{c}') for c in cargo_types]  # pos_fuel etc, value 1..6
for i, p in enumerate(pos):
    solver.add(p >= 1, p <= 6)
# Link positions with bay assignments: for each bay i (1..6) and each cargo c, bay_i == c iff pos_c == i
# Use equivalence via two implications
for i in range(6):
    for c in range(6):
        solver.add(Implies(bay[i] == c, pos[c] == i+1))
        solver.add(Implies(pos[c] == i+1, bay[i] == c))

# Now add ordering constraints using pos variables
solver.add(pos[gr] > pos[liv])
solver.add(pos[liv] > pos[text])
solver.add(pos[prod] > pos[fuel])
# textiles adjacent to produce
solver.add(Or(pos[text] == pos[prod] + 1, pos[text] == pos[prod] - 1))
# produce at bay 4
solver.add(bay[3] == prod)  # index 3 is bay 4

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    assign = [m.eval(bay[i]).as_long() for i in range(6)]
    solutions.append(assign)
    # block this solution
    solver.add(Or([bay[i] != assign[i] for i in range(6)]))

# Determine for each bay the set of possible cargo types
possible = [set() for _ in range(6)]
for assign in solutions:
    for i in range(6):
        possible[i].add(assign[i])
# Count bays with exactly one possible cargo
determined_count = sum(1 for s in possible if len(s) == 1)
# Map count to integer constant
count_val = determined_count

# Now evaluate multiple choice options using the required skeleton
# Recreate base solver (without blocking constraints) for option checking
base_solver = Solver()
# Re-add all base constraints (same as above) but without enumeration blocking
# Re-declare variables anew to avoid interference
bay2 = [Int(f'bay2_{i}') for i in range(1, 7)]
pos2 = [Int(f'pos2_{c}') for c in cargo_types]
for b in bay2:
    base_solver.add(b >= 0, b <= 5)
base_solver.add(Distinct(bay2))
for i in range(6):
    for c in range(6):
        base_solver.add(Implies(bay2[i] == c, pos2[c] == i+1))
        base_solver.add(Implies(pos2[c] == i+1, bay2[i] == c))
base_solver.add(pos2[gr] > pos2[liv])
base_solver.add(pos2[liv] > pos2[text])
base_solver.add(pos2[prod] > pos2[fuel])
base_solver.add(Or(pos2[text] == pos2[prod] + 1, pos2[text] == pos2[prod] - 1))
base_solver.add(bay2[3] == prod)

found_options = []
options = [
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 5),
    ("E", 6)
]
for letter, k in options:
    base_solver.push()
    # constraint that the determined count equals k
    # Since count_val is a known Python integer, we use BoolVal
    base_solver.add(BoolVal(count_val == k))
    if base_solver.check() == sat:
        found_options.append(letter)
    base_solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")