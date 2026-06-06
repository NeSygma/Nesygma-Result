from z3 import *

def enumerate_solutions(solver, variables):
    """Enumerate all solutions for given solver, return set of tuples of variable values."""
    solutions = set()
    var_list = list(variables.values())
    names = list(variables.keys())
    while solver.check() == sat:
        m = solver.model()
        sol_tuple = tuple(m.eval(v, model_completion=True).as_long() for v in var_list)
        solutions.add(sol_tuple)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in var_list]))
    return solutions

# Create base variables
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = {'U': U, 'V': V, 'W': W, 'X': X, 'Y': Y, 'Z': Z}

domain_constraints = [And(v >= 1, v <= 6) for v in bands.values()]
all_distinct = [Distinct(list(bands.values()))]

# Original constraints
orig_constr_1 = V < Z  # V earlier than Z
orig_constr_2 = And(W < X, Z < X)  # W and Z earlier than X
orig_constr_3 = U >= 4  # U in last three slots (4,5,6)
orig_constr_4 = Y <= 3  # Y in first three slots (1,2,3)

# Build original solver and enumerate
solver_orig = Solver()
solver_orig.add(domain_constraints)
solver_orig.add(all_distinct)
solver_orig.add(orig_constr_1)
solver_orig.add(orig_constr_2)
solver_orig.add(orig_constr_3)
solver_orig.add(orig_constr_4)

print("Enumerating original solutions...")
orig_solutions = enumerate_solutions(solver_orig, bands)
print(f"Original solution count: {len(orig_solutions)}")
# Print all original solutions sorted
for sol in sorted(orig_solutions):
    print(f"  U={sol[0]} V={sol[1]} W={sol[2]} X={sol[3]} Y={sol[4]} Z={sol[5]}")

# Define options - corrected
options = {
    # A: Only Uneasy can perform in a later slot than Xpert.
    # Means: for any band B != U, B is NOT later than X => B < X
    # No constraint on U relative to X (but if X is not last, U must be the later one)
    'A': And(V < X, W < X, Y < X, Z < X),  # Only U can be later than X (all others earlier)
    
    # B: V < W < Z
    'B': And(V < W, W < Z),
    
    # C: V < X and W < X
    'C': And(V < X, W < X),
    
    # D: |X - U| = 1
    'D': Or(X == U - 1, X == U + 1),
    
    # E: X in slot 5 or 6
    'E': Or(X == 5, X == 6),
}

# For each option, build solver with base constraints (1,3,4) + option, enumerate solutions, compare
for letter, opt_constr in options.items():
    solver_opt = Solver()
    solver_opt.add(domain_constraints)
    solver_opt.add(all_distinct)
    solver_opt.add(orig_constr_1)  # Keep V < Z
    solver_opt.add(orig_constr_3)  # Keep U >= 4
    solver_opt.add(orig_constr_4)  # Keep Y <= 3
    solver_opt.add(opt_constr)     # Add this option's constraint (replacing constraint 2)
    
    opt_solutions = enumerate_solutions(solver_opt, bands)
    
    if opt_solutions == orig_solutions:
        print(f"\nOption {letter}: SAME effect as original. Solutions count: {len(opt_solutions)}")
    else:
        print(f"\nOption {letter}: DIFFERENT effect. Solutions count: {len(opt_solutions)}")
        only_orig = orig_solutions - opt_solutions
        only_opt = opt_solutions - orig_solutions
        if only_orig:
            print(f"  In original but not in option: {len(only_orig)} solutions")
        if only_opt:
            print(f"  In option but not in original: {len(only_opt)} solutions")

# Now determine which option is correct (same effect)
print("\n\nDetermining correct answer...")
found_options = []
for letter, opt_constr in options.items():
    solver_test = Solver()
    solver_test.add(domain_constraints)
    solver_test.add(all_distinct)
    solver_test.add(orig_constr_1)
    solver_test.add(orig_constr_3)
    solver_test.add(orig_constr_4)
    solver_test.add(opt_constr)
    
    test_solutions = enumerate_solutions(solver_test, bands)
    if test_solutions == orig_solutions:
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