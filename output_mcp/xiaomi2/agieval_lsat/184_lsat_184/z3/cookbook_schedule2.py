from z3 import *

# Boolean variables: True = Fall, False = Spring
K, L, M, N, O, P = Bools('K L M N O P')
all_vars = [K, L, M, N, O, P]

# Base constraints (shared by all)
base = [
    M != P,               # 1. M and P cannot be in the same season
    K == N,               # 2. K and N must be in the same season
    Implies(K, O),        # 3. If K is fall, O must be fall
]

# Original constraint 4: If M is fall, N must be in spring
original_4 = Implies(M, Not(N))

# Answer choice constraints (each replaces constraint 4)
answer_constraints = {
    "A": Implies(L, Not(M)),           # If L is fall, M must be spring
    "B": Implies(N, P),                # If N is fall, P must be fall
    "C": Implies(Not(M), P),           # If M is spring, P must be fall
    "D": Implies(Not(N), Not(M)),      # If N is spring, M must be spring
    "E": Implies(Not(O), Not(N)),      # If O is spring, N must be spring
}

def enumerate_solutions(constraints):
    """Enumerate all satisfying assignments for given constraints."""
    s = Solver()
    s.add(constraints)
    solutions = set()
    while s.check() == sat:
        m = s.model()
        sol = tuple(is_true(m.eval(v, model_completion=True)) for v in all_vars)
        solutions.add(sol)
        # Block this solution
        s.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))
    return solutions

# Find all solutions under original constraints
original_solutions = enumerate_solutions(base + [original_4])

print(f"Original constraints yield {len(original_solutions)} valid schedules:")
for sol in sorted(original_solutions):
    labels = {True: 'F', False: 'S'}
    print(f"  K={labels[sol[0]]} L={labels[sol[1]]} M={labels[sol[2]]} N={labels[sol[3]]} O={labels[sol[4]]} P={labels[sol[5]]}")

print()

# Check each answer choice
found_options = []
for letter, constr in answer_constraints.items():
    candidate_solutions = enumerate_solutions(base + [constr])
    match = (candidate_solutions == original_solutions)
    print(f"Option {letter}: {len(candidate_solutions)} schedules, match={match}")
    if match:
        found_options.append(letter)

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")