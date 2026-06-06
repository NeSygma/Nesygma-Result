from z3 import *

# We have 7 clues: R, S, T, U, W, X, Z
# 7 chapters: 1 through 7
# Each clue assigned to exactly one chapter

# Let's enumerate all valid solutions under original constraints
# Then for each option, enumerate solutions and compare

clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']

def get_all_solutions(constraints_with_mod=None, replace_constraint1_with=None):
    """Get all solutions. If replace_constraint1_with is given,
    replace the 'T != 1' constraint with the given constraint."""
    solver = Solver()
    
    # Decision variables: chapter number for each clue
    chap = {c: Int(f'chap_{c}') for c in clues}
    
    # Domain: each chapter is 1-7
    for c in clues:
        solver.add(chap[c] >= 1, chap[c] <= 7)
    
    # All different: each clue in a different chapter
    solver.add(Distinct([chap[c] for c in clues]))
    
    # Original constraint 1: T cannot be in chapter 1
    if replace_constraint1_with is None:
        solver.add(chap['T'] != 1)
    else:
        solver.add(replace_constraint1_with)
    
    # Constraint 2: T before W, exactly 2 chapters separating them
    solver.add(chap['T'] < chap['W'])
    solver.add(chap['W'] - chap['T'] == 3)
    
    # Constraint 3: S and Z not adjacent
    solver.add(Abs(chap['S'] - chap['Z']) != 1)
    
    # Constraint 4: W and X not adjacent
    solver.add(Abs(chap['W'] - chap['X']) != 1)
    
    # Constraint 5: U and X adjacent
    solver.add(Abs(chap['U'] - chap['X']) == 1)
    
    # Also add constraints from the modified set if any
    if constraints_with_mod:
        for constr in constraints_with_mod:
            solver.add(constr)
    
    # Enumerate all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(chap[c], model_completion=True).as_long() for c in clues)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([chap[c] != m.eval(chap[c], model_completion=True).as_long() for c in clues]))
    
    return set(solutions)

# Get baseline solutions (original constraints)
print("Computing baseline solutions with original constraint 'T != 1'...")
baseline = get_all_solutions()
print(f"Number of baseline solutions: {len(baseline)}")
for sol in sorted(baseline):
    print(f"  R={sol[0]} S={sol[1]} T={sol[2]} U={sol[3]} W={sol[4]} X={sol[5]} Z={sol[6]}")

print("\n" + "="*60 + "\n")

# Now test each option by replacing T != 1 with the option's constraint
options = {
    "A": chap['U'] != 2,  # U cannot be in chapter 2
    "B": chap['W'] != 4,  # W cannot be in chapter 4
    "C": chap['X'] != 6,  # X cannot be in chapter 6
    "D": chap['U'] < chap['T'],  # U before T
    "E": chap['X'] < chap['W'],  # X before W
}

# But wait - for options A, B, C, we replace the 'T != 1' constraint with the option.
# For D and E, these are additional constraints plus the original T != 1? 
# Let me re-read: "if substituted for the constraint that T cannot be mentioned in chapter 1"
# So ALL options are meant to substitute for constraint 1.

# But D and E are different kinds of constraints. Let me apply them as substitutes.

for letter, constr in options.items():
    print(f"Testing Option {letter}: replacing T != 1 with {constr}")
    
    # We need a fresh solver and fresh variables here
    sol_set = get_all_solutions(replace_constraint1_with=constr)
    print(f"  Number of solutions: {len(sol_set)}")
    
    if sol_set == baseline:
        print(f"  ✅ OPTION {letter} HAS THE SAME EFFECT!")
    else:
        # Show the differences
        only_in_baseline = baseline - sol_set
        only_in_option = sol_set - baseline
        if only_in_baseline:
            print(f"  In baseline but not option: {only_in_baseline}")
        if only_in_option:
            print(f"  In option but not baseline: {only_in_option}")
    print()