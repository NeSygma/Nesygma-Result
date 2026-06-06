from z3 import *

# Variables: chapter assignment for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

def add_base_constraints(solver):
    """Add all constraints EXCEPT 'T cannot be in chapter 1'"""
    for c in clues:
        solver.add(And(c >= 1, c <= 7))
    solver.add(Distinct(clues))
    # T before W with exactly 2 chapters between: W = T + 3
    solver.add(W == T + 3)
    # S and Z not adjacent
    solver.add(Abs(S - Z) != 1)
    # W and X not adjacent
    solver.add(Abs(W - X) != 1)
    # U and X must be adjacent
    solver.add(Abs(U - X) == 1)

def get_all_solutions(extra_constraint=None, max_solutions=500):
    s = Solver()
    add_base_constraints(s)
    if extra_constraint is not None:
        s.add(extra_constraint)
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple(int(str(m[v])) for v in clues)
        solutions.append(sol)
        s.add(Or([v != m.eval(v, model_completion=True) for v in clues]))
        if len(solutions) >= max_solutions:
            break
    return set(solutions)

# Find solutions with original constraint T != 1
solutions_original = get_all_solutions(T != 1)

# Test each option as replacement for T != 1
options = {
    "A": U != 2,
    "B": W != 4,
    "C": X != 6,
    "D": U < T,
    "E": X < W,
}

found_options = []
for letter, constr in options.items():
    sols = get_all_solutions(constr)
    if sols == solutions_original:
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