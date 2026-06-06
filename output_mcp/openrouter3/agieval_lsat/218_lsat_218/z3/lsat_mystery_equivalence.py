from z3 import *

def check_equivalence(candidate_name, candidate_constraint):
    """Check if candidate constraint is equivalent to T != 1 given other constraints."""
    # Original constraints (without T != 1)
    solver_orig = Solver()
    R, S, T, U, W, X, Z = Ints('R S T U W X Z')
    clues = [R, S, T, U, W, X, Z]
    for clue in clues:
        solver_orig.add(clue >= 1, clue <= 7)
    solver_orig.add(Distinct(clues))
    solver_orig.add(T < W)
    solver_orig.add(W == T + 3)
    solver_orig.add(Not(Or(S == Z + 1, Z == S + 1)))
    solver_orig.add(Not(Or(W == X + 1, X == W + 1)))
    solver_orig.add(Or(U == X + 1, X == U + 1))
    
    # Add original constraint T != 1
    solver_orig.add(T != 1)
    
    # Check if original implies candidate: (original + Not(candidate)) unsat?
    solver1 = Solver()
    solver1.add(solver_orig.assertions())
    solver1.add(Not(candidate_constraint))
    result1 = solver1.check()
    orig_implies_candidate = (result1 == unsat)
    
    # Check if candidate implies T != 1: (candidate + other constraints + T == 1) unsat?
    solver2 = Solver()
    # Add other constraints (without T != 1)
    for clue in clues:
        solver2.add(clue >= 1, clue <= 7)
    solver2.add(Distinct(clues))
    solver2.add(T < W)
    solver2.add(W == T + 3)
    solver2.add(Not(Or(S == Z + 1, Z == S + 1)))
    solver2.add(Not(Or(W == X + 1, X == W + 1)))
    solver2.add(Or(U == X + 1, X == U + 1))
    # Add candidate
    solver2.add(candidate_constraint)
    # Add T == 1
    solver2.add(T == 1)
    result2 = solver2.check()
    candidate_implies_Tnot1 = (result2 == unsat)
    
    return orig_implies_candidate and candidate_implies_Tnot1

# Define candidate constraints
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
candidates = [
    ("A", U != 2),  # U cannot be mentioned in chapter 2
    ("B", W != 4),  # W cannot be mentioned in chapter 4
    ("C", X != 6),  # X cannot be mentioned in chapter 6
    ("D", U < T),   # U must be mentioned in an earlier chapter than T
    ("E", X < W)    # X must be mentioned in an earlier chapter than W
]

print("Checking equivalence of each candidate with T != 1...")
found_equivalent = []
for name, constr in candidates:
    if check_equivalence(name, constr):
        found_equivalent.append(name)
        print(f"{name}: EQUIVALENT")
    else:
        print(f"{name}: NOT equivalent")

print(f"\nFound {len(found_equivalent)} equivalent candidates: {found_equivalent}")

if len(found_equivalent) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{found_equivalent[0]}")
else:
    print(f"\nSTATUS: unsat")
    if len(found_equivalent) > 1:
        print(f"Refine: Multiple options found {found_equivalent}")
    else:
        print("Refine: No options found")