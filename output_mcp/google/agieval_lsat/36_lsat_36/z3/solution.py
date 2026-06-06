from z3 import *

# Cargo types
cargo_types = ['F', 'G', 'L', 'M', 'P', 'T']
# Bay numbers
bays = [1, 2, 3, 4, 5, 6]

# pos[c] is the bay number for cargo c
pos = {c: Int(f'pos_{c}') for c in cargo_types}

solver = Solver()

# Each cargo in a different bay
solver.add(Distinct([pos[c] for c in cargo_types]))
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)

# Constraints
solver.add(pos['G'] > pos['L'])
solver.add(pos['L'] > pos['T'])
solver.add(pos['P'] > pos['F'])
solver.add(Or(pos['T'] == pos['P'] - 1, pos['T'] == pos['P'] + 1))

# Condition: Bay 4 is holding produce
solver.add(pos['P'] == 4)

# Find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {c: m[pos[c]].as_long() for c in cargo_types}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([pos[c] != m[pos[c]] for c in cargo_types]))

print(f"Total solutions: {len(solutions)}")

# For each bay, check if the cargo is determined
determined_bays = 0
for b in bays:
    # Find which cargo is in bay b for each solution
    cargo_in_b = []
    for sol in solutions:
        for c in cargo_types:
            if sol[c] == b:
                cargo_in_b.append(c)
    
    # If all solutions have the same cargo in bay b, it's determined
    if len(set(cargo_in_b)) == 1:
        determined_bays += 1
        print(f"Bay {b} is determined: {cargo_in_b[0]}")
    else:
        print(f"Bay {b} is NOT determined: {set(cargo_in_b)}")

print(f"Number of determined bays: {determined_bays}")

# Now map this to the answer choices
# (A)two (B)three (C)four (D)five (E)six
# We need to check which option matches determined_bays
# The question asks for exactly how many.
# Let's use the required skeleton.

opt_a_constr = (determined_bays == 2)
opt_b_constr = (determined_bays == 3)
opt_c_constr = (determined_bays == 4)
opt_d_constr = (determined_bays == 5)
opt_e_constr = (determined_bays == 6)

# Re-run the check using the required skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if constr:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")