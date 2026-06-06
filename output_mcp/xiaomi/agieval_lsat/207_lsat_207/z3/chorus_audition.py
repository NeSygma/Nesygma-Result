from z3 import *

# Define singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']  # Kammer, Lugo, Trillo, Waite, Yoshida, Zinn

# Position variables: pos[s] = position (1-6) for singer s
pos = {s: Int(f'pos_{s}') for s in singers}

solver = Solver()

# All positions are between 1 and 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions are distinct
solver.add(Distinct([pos[s] for s in singers]))

# Recorded singers: Kammer (K) and Lugo (L)
# Not recorded: T, W, Y, Z

# Condition 1: The fourth audition cannot be recorded
# So position 4 cannot be K or L
solver.add(pos['K'] != 4)
solver.add(pos['L'] != 4)

# Condition 2: The fifth audition must be recorded
# So position 5 must be K or L
solver.add(Or(pos['K'] == 5, pos['L'] == 5))

# Condition 3: Waite's audition must take place earlier than the two recorded auditions
# W must be before both K and L
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])

# Condition 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(pos['K'] < pos['T'])

# Condition 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos['Z'] < pos['Y'])

# Now we need to find which substitution for condition 3 yields the same set of valid orderings.
# We'll check each option by replacing condition 3 with the option's constraint,
# and verifying that the solution sets are equivalent.

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
        # Zinn's audition is the only one that can take place earlier than Waite's
        # This means: Z < W, and for all other singers X (not Z), X > W
        pos['Z'] < pos['W'],
        pos['K'] > pos['W'],
        pos['L'] > pos['W'],
        pos['T'] > pos['W'],
        pos['Y'] > pos['W']
    ),
    "B": lambda: Or(
        # Waite's audition must take place either immediately before or immediately after Zinn's
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
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")