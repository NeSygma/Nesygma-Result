from z3 import *

# Boolean variables: True = Fall, False = Spring
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints (all except the one to be substituted)
base = [
    # M and P cannot be published in the same season
    Not(And(M, P)),   # not both Fall
    Not(And(Not(M), Not(P))),  # not both Spring => i.e., M != P
    # K and N must be in the same season
    K == N,
    # If K is in Fall, O must be in Fall
    Implies(K, O),
]

# The original constraint to be substituted:
# If M is Fall, N must be Spring
original = Implies(M, Not(N))

# We need to find which option, when combined with base constraints,
# produces the EXACT SAME set of valid schedules as base + original.

# First, enumerate all valid schedules under base + original
def enumerate_schedules(constraints):
    s = Solver()
    s.add(constraints)
    solutions = []
    vars_list = [K, L, M, N, O, P]
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(v, model_completion=True) for v in vars_list)
        solutions.append(sol)
        s.add(Or([v != m.eval(v, model_completion=True) for v in vars_list]))
    return set(solutions)

original_schedules = enumerate_schedules(base + [original])

# Now test each option
options = {
    "A": Implies(L, Not(M)),  # If L is Fall, M must be Spring
    "B": Implies(N, P),       # If N is Fall, P must be Fall
    "C": Implies(Not(M), P),  # If M is Spring, P must be Fall
    "D": Implies(Not(N), Not(M)),  # If N is Spring, M must be Spring
    "E": Implies(Not(O), Not(N)),  # If O is Spring, N must be Spring
}

found_options = []
for letter, constr in options.items():
    option_schedules = enumerate_schedules(base + [constr])
    if option_schedules == original_schedules:
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

# Debug info
print(f"\nOriginal schedules count: {len(original_schedules)}")
for letter, constr in options.items():
    option_schedules = enumerate_schedules(base + [constr])
    print(f"Option {letter}: count={len(option_schedules)}, match={option_schedules == original_schedules}")