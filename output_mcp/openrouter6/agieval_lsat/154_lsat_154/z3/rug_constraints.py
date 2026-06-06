from z3 import *

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
rug = [Int(f'rug_{c}') for c in range(6)]

solver = Solver()

# Domain constraints: rug[c] in {0,1,2,3} where 3 means not used
for c in range(6):
    solver.add(rug[c] >= 0, rug[c] <= 3)

# Exactly five colors used
used_count = Sum([If(rug[c] != 3, 1, 0) for c in range(6)])
solver.add(used_count == 5)

# Each rug (0,1,2) must have at least one color
for r in range(3):
    count_r = Sum([If(rug[c] == r, 1, 0) for c in range(6)])
    solver.add(count_r >= 1)

# White rule: if white used, its rug has exactly three colors
white_used = rug[4] != 3
count_white_rug = Sum([If(rug[c] == rug[4], 1, 0) for c in range(6)])
solver.add(Implies(white_used, count_white_rug == 3))

# Olive rule: if olive used, peach must be used and in same rug
olive_used = rug[1] != 3
solver.add(Implies(olive_used, And(rug[2] != 3, rug[1] == rug[2])))

# Forest and turquoise not together
solver.add(Implies(And(rug[0] != 3, rug[3] != 3), rug[0] != rug[3]))

# Peach and turquoise not together
solver.add(Implies(And(rug[2] != 3, rug[3] != 3), rug[2] != rug[3]))

# Peach and yellow not together
solver.add(Implies(And(rug[2] != 3, rug[5] != 3), rug[2] != rug[5]))

# Solid yellow condition: yellow used and alone in its rug
solver.add(rug[5] != 3)  # yellow used
for c in range(6):
    if c != 5:
        solver.add(rug[c] != rug[5])

# Check base satisfiability
print("Checking base constraints...")
result_base = solver.check()
if result_base == sat:
    print("Base constraints are satisfiable.")
    m = solver.model()
    print("Example model:")
    for c in range(6):
        val = m[rug[c]]
        if val == 3:
            print(f"Color {c} not used")
        else:
            print(f"Color {c} assigned to rug {val}")
else:
    print("Base constraints are unsatisfiable. Something is wrong.")
    print("STATUS: unsat")
    exit()

# Now evaluate each answer choice
# Define option constraints
opt_a = Sum([If(rug[c] != 3 and Sum([If(rug[c] == r, 1, 0) for c in range(6)]) == 1, 1, 0) for r in range(3)]) == 1
# Actually, we need to count rugs with exactly one color.
# Let's compute for each rug r: is_solid[r] = (count_r[r] == 1)
# Then sum over r of is_solid[r] == 1.
# We'll compute count_r for each r.
counts = []
for r in range(3):
    count_r = Sum([If(rug[c] == r, 1, 0) for c in range(6)])
    counts.append(count_r)
is_solid = [counts[r] == 1 for r in range(3)]
opt_a = Sum([If(is_solid[r], 1, 0) for r in range(3)]) == 1

# Option B: One of the rugs is solid forest.
# That means there exists a rug r such that rug[0] == r and for all other colors c != 0, rug[c] != r.
# We can express as: Or([And(rug[0] == r, Sum([If(rug[c] == r, 1, 0) for c in range(6)]) == 1) for r in range(3)])
opt_b = Or([And(rug[0] == r, Sum([If(rug[c] == r, 1, 0) for c in range(6)]) == 1) for r in range(3)])

# Option C: Turquoise not used
opt_c = rug[3] == 3

# Option D: Forest and olive used together in a rug
opt_d = And(rug[0] != 3, rug[1] != 3, rug[0] == rug[1])

# Option E: Peach and white used together in a rug
opt_e = And(rug[2] != 3, rug[4] != 3, rug[2] == rug[4])

# Now test each option
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print("\nResults:")
print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")