from z3 import *

# Variables: chapter assignment for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]
clue_names = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']

def add_base_constraints(solver):
    """Add all constraints EXCEPT 'T cannot be in chapter 1'"""
    # Each clue assigned to a chapter 1-7
    for c in clues:
        solver.add(And(c >= 1, c <= 7))
    # All different chapters
    solver.add(Distinct(clues))
    
    # T before W with exactly 2 chapters between them: W = T + 3
    solver.add(W == T + 3)
    
    # S and Z not adjacent
    solver.add(Abs(S - Z) != 1)
    
    # W and X not adjacent
    solver.add(Abs(W - X) != 1)
    
    # U and X must be adjacent
    solver.add(Abs(U - X) == 1)

def get_all_solutions(base_constraints_fn, extra_constraint=None, max_solutions=500):
    """Enumerate all solutions given constraints"""
    s = Solver()
    base_constraints_fn(s)
    if extra_constraint is not None:
        s.add(extra_constraint)
    
    solutions = []
    decision_vars = clues
    
    while s.check() == sat:
        m = s.model()
        sol = tuple(int(str(m[v])) for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        s.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
        if len(solutions) >= max_solutions:
            break
    
    return set(solutions)

# Find all solutions with original constraint: T != 1
print("Finding solutions with T != 1...")
solutions_original = get_all_solutions(add_base_constraints, T != 1)
print(f"  Found {len(solutions_original)} solutions")

# Define replacement constraints for each option
options = {
    "A": U != 2,           # U cannot be in chapter 2
    "B": W != 4,           # W cannot be in chapter 4
    "C": X != 6,           # X cannot be in chapter 6
    "D": U < T,            # U must be mentioned earlier than T
    "E": X < W,            # X must be mentioned earlier than W
}

for letter, constraint in options.items():
    print(f"\nFinding solutions with option {letter}...")
    sols = get_all_solutions(add_base_constraints, constraint)
    print(f"  Found {len(sols)} solutions")
    matches = sols == solutions_original
    print(f"  Matches original set: {matches}")
    if matches:
        print(f"  *** OPTION {letter} IS THE CORRECT ANSWER ***")

# Now use the required skeleton for final output
solver = Solver()
add_base_constraints(solver)

# Base: all constraints except T!=1 are already added
# We need to test each option as a REPLACEMENT for T!=1

found_options = []
for letter, constr in [("A", U != 2), ("B", W != 4), ("C", X != 6), ("D", U < T), ("E", X < W)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")