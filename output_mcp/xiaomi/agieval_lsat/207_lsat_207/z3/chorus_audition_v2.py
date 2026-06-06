from z3 import *

# Define singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']  # Kammer, Lugo, Trillo, Waite, Yoshida, Zinn

# Position variables: pos[s] = position (1-6) for singer s
pos = {s: Int(f'pos_{s}') for s in singers}

# First, find all solutions with original constraints
original_solutions = []
temp_solver = Solver()
for s in singers:
    temp_solver.add(pos[s] >= 1, pos[s] <= 6)
temp_solver.add(Distinct([pos[s] for s in singers]))
temp_solver.add(pos['K'] != 4)
temp_solver.add(pos['L'] != 4)
temp_solver.add(Or(pos['K'] == 5, pos['L'] == 5))
temp_solver.add(pos['W'] < pos['K'])
temp_solver.add(pos['W'] < pos['L'])
temp_solver.add(pos['K'] < pos['T'])
temp_solver.add(pos['Z'] < pos['Y'])

while temp_solver.check() == sat:
    m = temp_solver.model()
    sol = tuple(m.evaluate(pos[s]).as_long() for s in singers)
    original_solutions.append(sol)
    temp_solver.add(Or([pos[s] != m[pos[s]] for s in singers]))

print(f"Original solutions count: {len(original_solutions)}")

# Now test each option
options = {
    "A": lambda: And(
        pos['Z'] < pos['W'],
        pos['K'] > pos['W'],
        pos['L'] > pos['W'],
        pos['T'] > pos['W'],
        pos['Y'] > pos['W']
    ),
    "B": lambda: Or(
        pos['W'] == pos['Z'] + 1,
        pos['Z'] == pos['W'] + 1
    ),
    "C": lambda: pos['W'] < pos['L'],
    "D": lambda: Or(pos['W'] == 1, pos['W'] == 2),
    "E": lambda: And(pos['K'] != 1, pos['L'] != 1)
}

found_options = []

for letter, constr_fn in options.items():
    # Build solver with base constraints (without condition 3) + option constraint
    s = Solver()
    for singer in singers:
        s.add(pos[singer] >= 1, pos[singer] <= 6)
    s.add(Distinct([pos[singer] for singer in singers]))
    s.add(pos['K'] != 4)
    s.add(pos['L'] != 4)
    s.add(Or(pos['K'] == 5, pos['L'] == 5))
    s.add(pos['K'] < pos['T'])
    s.add(pos['Z'] < pos['Y'])
    # Add the option constraint (replacing condition 3)
    s.add(constr_fn())
    
    # Find all solutions with this option
    option_solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.evaluate(pos[singer]).as_long() for singer in singers)
        option_solutions.append(sol)
        s.add(Or([pos[singer] != m[pos[singer]] for singer in singers]))
    
    # Check if solution sets are identical
    orig_set = set(original_solutions)
    opt_set = set(option_solutions)
    match = (orig_set == opt_set)
    
    print(f"Option {letter}: {len(option_solutions)} solutions, match={match}")
    
    if match:
        found_options.append(letter)

if len(found_options) == 1:
    print("\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("\nSTATUS: unsat")
    print("Refine: No options found")