from z3 import *

# Create solver
solver = Solver()

# Houses and positions
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
positions = list(range(1, 8))  # 1 to 7

# Create position variables for each house
pos = {h: Int(f'pos_{h}') for h in houses}

# All houses must have distinct positions
solver.add(Distinct([pos[h] for h in houses]))

# Each position must be between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1)
    solver.add(pos[h] <= 7)

# Rule 1: J must be in evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be in morning (positions 1 or 2)
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Rule 3: L must be after K and before M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Now test each option for "cannot be shown consecutively"
# We need to check if there exists ANY valid arrangement where they ARE consecutive
# If NO such arrangement exists, then they CANNOT be consecutive

# Option A: J, K cannot be consecutive
opt_a_constr = Or(pos['J'] == pos['K'] + 1, pos['K'] == pos['J'] + 1)

# Option B: J, M cannot be consecutive
opt_b_constr = Or(pos['J'] == pos['M'] + 1, pos['M'] == pos['J'] + 1)

# Option C: J, O cannot be consecutive
opt_c_constr = Or(pos['J'] == pos['O'] + 1, pos['O'] == pos['J'] + 1)

# Option D: J, P cannot be consecutive
opt_d_constr = Or(pos['J'] == pos['P'] + 1, pos['P'] == pos['J'] + 1)

# Option E: M, P cannot be consecutive
opt_e_constr = Or(pos['M'] == pos['P'] + 1, pos['P'] == pos['M'] + 1)

# Test each option: check if there exists a valid arrangement where they ARE consecutive
# If solver.check() == unsat, then they CANNOT be consecutive
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)  # Add constraint that they ARE consecutive
    result = solver.check()
    if result == unsat:  # If unsat, they CANNOT be consecutive
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")