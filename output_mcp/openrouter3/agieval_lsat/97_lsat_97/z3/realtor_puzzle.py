from z3 import *

# Create solver
solver = Solver()

# Declare variables for each house's position (1-7)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions must be distinct and between 1-7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# Constraint 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Constraint 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))

# Constraint 3: L must be shown after K and before M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Additional constraint: P is shown in the afternoon (positions 3, 4, or 5)
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# Now test each option
# Option A: J is shown seventh
opt_a = (pos['J'] == 7)

# Option B: K is shown third
opt_b = (pos['K'] == 3)

# Option C: N is shown first
opt_c = (pos['N'] == 1)

# Option D: M is shown in the afternoon (positions 3, 4, or 5)
opt_d = Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5)

# Option E: O is shown in the morning (positions 1 or 2)
opt_e = Or(pos['O'] == 1, pos['O'] == 2)

# Test each option using the required skeleton
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
    # Also print a sample model to verify
    solver.check()
    m = solver.model()
    print("\nSample model (positions):")
    for h in houses:
        print(f"{h}: {m[pos[h]]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")