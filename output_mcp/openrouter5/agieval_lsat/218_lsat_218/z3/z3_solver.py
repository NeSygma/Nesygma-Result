from z3 import *

# We have 7 clues: R, S, T, U, W, X, Z
# Each assigned to a chapter 1-7, one per chapter.
# We'll model each clue's chapter as an integer variable.

clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
ch = {c: Int(f'ch_{c}') for c in clues}

solver = Solver()

# Domain: each chapter from 1 to 7
for c in clues:
    solver.add(ch[c] >= 1, ch[c] <= 7)

# All different chapters
solver.add(Distinct([ch[c] for c in clues]))

# Original constraints:
# 1. T cannot be mentioned in chapter 1.
solver.add(ch['T'] != 1)

# 2. T must be mentioned before W, and exactly two chapters separating T and W.
#    So ch['W'] - ch['T'] = 3 (since exactly two chapters between them, and T before W)
solver.add(ch['W'] - ch['T'] == 3)

# 3. S and Z cannot be adjacent.
solver.add(Abs(ch['S'] - ch['Z']) != 1)

# 4. W and X cannot be adjacent.
solver.add(Abs(ch['W'] - ch['X']) != 1)

# 5. U and X must be adjacent.
solver.add(Abs(ch['U'] - ch['X']) == 1)

# Now we need to find which option, when substituted for "T cannot be in chapter 1",
# has the same effect on determining the order.

# The approach: 
# - First, find all valid orders under the original constraints (including T != 1).
# - Then, for each option, replace T != 1 with that option's constraint, and see if the set of valid orders is the same.

# We'll enumerate all solutions for the original constraints.
# Decision variables: the chapter assignments.

def enumerate_solutions(s):
    """Enumerate all solutions and return list of models (as dicts)."""
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = {c: m.eval(ch[c], model_completion=True).as_long() for c in clues}
        solutions.append(sol)
        # Block this solution
        s.add(Or([ch[c] != sol[c] for c in clues]))
    return solutions

# Get original solutions
solver_orig = Solver()
for c in clues:
    solver_orig.add(ch[c] >= 1, ch[c] <= 7)
solver_orig.add(Distinct([ch[c] for c in clues]))
solver_orig.add(ch['T'] != 1)
solver_orig.add(ch['W'] - ch['T'] == 3)
solver_orig.add(Abs(ch['S'] - ch['Z']) != 1)
solver_orig.add(Abs(ch['W'] - ch['X']) != 1)
solver_orig.add(Abs(ch['U'] - ch['X']) == 1)

orig_solutions = enumerate_solutions(solver_orig)
print(f"Original solutions count: {len(orig_solutions)}")
for sol in orig_solutions:
    print(sol)

# Now test each option
options = {
    "A": ch['U'] != 2,
    "B": ch['W'] != 4,
    "C": ch['X'] != 6,
    "D": ch['U'] < ch['T'],
    "E": ch['X'] < ch['W']
}

found_options = []
for letter, constr in options.items():
    solver_test = Solver()
    for c in clues:
        solver_test.add(ch[c] >= 1, ch[c] <= 7)
    solver_test.add(Distinct([ch[c] for c in clues]))
    # Replace T != 1 with the new constraint
    solver_test.add(constr)
    # Keep the other original constraints
    solver_test.add(ch['W'] - ch['T'] == 3)
    solver_test.add(Abs(ch['S'] - ch['Z']) != 1)
    solver_test.add(Abs(ch['W'] - ch['X']) != 1)
    solver_test.add(Abs(ch['U'] - ch['X']) == 1)
    
    test_solutions = enumerate_solutions(solver_test)
    print(f"\nOption {letter} solutions count: {len(test_solutions)}")
    for sol in test_solutions:
        print(sol)
    
    # Check if the set of solutions is identical to original
    if set(tuple(sorted(sol.items())) for sol in test_solutions) == set(tuple(sorted(sol.items())) for sol in orig_solutions):
        found_options.append(letter)
        print(f"Option {letter} MATCHES original")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")