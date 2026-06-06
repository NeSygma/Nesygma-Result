from z3 import *

# Declare variables for positions (1-6)
pos = {name: Int(f'pos_{name}') for name in ['K', 'L', 'T', 'W', 'Y', 'Z']}

# Base solver for enumerating all valid orderings
base_solver = Solver()

# All positions distinct and in 1..6
for name, p in pos.items():
    base_solver.add(p >= 1, p <= 6)
base_solver.add(Distinct(list(pos.values())))

# Constraint: Fourth audition cannot be recorded (i.e., position 4 is not K or L)
base_solver.add(pos['K'] != 4)
base_solver.add(pos['L'] != 4)

# Constraint: Fifth audition must be recorded (i.e., position 5 is K or L)
base_solver.add(Or(pos['K'] == 5, pos['L'] == 5))

# Constraint: Kammer earlier than Trillo
base_solver.add(pos['K'] < pos['T'])

# Constraint: Zinn earlier than Yoshida
base_solver.add(pos['Z'] < pos['Y'])

# Original constraint 3: Waite earlier than both recorded auditions (K and L)
original_constraint = And(pos['W'] < pos['K'], pos['W'] < pos['L'])

# Find all models that satisfy base constraints
solutions_base = []
while base_solver.check() == sat:
    m = base_solver.model()
    sol = {}
    for name in pos:
        # Get the value as an integer
        val = m.evaluate(pos[name], model_completion=True)
        # Convert from Z3 IntNumRef to Python int
        sol[name] = int(str(val))
    solutions_base.append(sol)
    # Blocking clause to find next solution
    base_solver.add(Or([pos[name] != sol[name] for name in pos]))

print(f"Total base solutions: {len(solutions_base)}")

# Filter solutions that satisfy original constraint
solutions_original = [sol for sol in solutions_base if sol['W'] < sol['K'] and sol['W'] < sol['L']]
print(f"Solutions with original constraint: {len(solutions_original)}")

# Define option constraints
opt_a = And(pos['Z'] < pos['W'],  # Zinn's audition is the only one that can take place earlier than Waite's.
            # "only one" means no other singer can be earlier than Waite except Zinn.
            # So for all other singers X (not Z, not W), pos[X] > pos[W]
            *[pos[X] > pos['W'] for X in ['K', 'L', 'T', 'Y']])

opt_b = Or(pos['W'] == pos['Z'] - 1, pos['W'] == pos['Z'] + 1)  # Waite immediately before or after Zinn

opt_c = pos['W'] < pos['L']  # Waite earlier than Lugo

opt_d = Or(pos['W'] == 1, pos['W'] == 2)  # Waite first or second

opt_e = And(pos['K'] != 1, pos['L'] != 1)  # First audition cannot be recorded (i.e., position 1 is not K and not L)

# For each option, find solutions that satisfy base + option
options = [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]
option_solutions = {}

for letter, opt_constr in options:
    solver = Solver()
    # Add base constraints
    for name, p in pos.items():
        solver.add(p >= 1, p <= 6)
    solver.add(Distinct(list(pos.values())))
    solver.add(pos['K'] != 4)
    solver.add(pos['L'] != 4)
    solver.add(Or(pos['K'] == 5, pos['L'] == 5))
    solver.add(pos['K'] < pos['T'])
    solver.add(pos['Z'] < pos['Y'])
    # Add option constraint
    solver.add(opt_constr)
    
    # Find all solutions
    sols = []
    while solver.check() == sat:
        m = solver.model()
        sol = {}
        for name in pos:
            val = m.evaluate(pos[name], model_completion=True)
            sol[name] = int(str(val))
        sols.append(sol)
        solver.add(Or([pos[name] != sol[name] for name in pos]))
    option_solutions[letter] = sols
    print(f"Option {letter} solutions: {len(sols)}")

# Compare sets: check if solutions_original equals option_solutions[letter] for each letter
found_options = []
for letter in ['A', 'B', 'C', 'D', 'E']:
    # Compare sets of solutions (as tuples of sorted items)
    set_orig = {tuple(sorted(sol.items())) for sol in solutions_original}
    set_opt = {tuple(sorted(sol.items())) for sol in option_solutions[letter]}
    if set_orig == set_opt:
        found_options.append(letter)

print(f"Found options with same effect: {found_options}")

# Output according to required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")