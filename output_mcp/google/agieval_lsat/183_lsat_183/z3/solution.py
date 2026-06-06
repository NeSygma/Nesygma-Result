from z3 import *

# Variables: 1 for Fall, 0 for Spring
K, L, M, N, O, P = Ints('K L M N O P')
vars = [K, L, M, N, O, P]

def get_base_constraints():
    return [
        And(v >= 0, v <= 1) for v in vars
    ] + [
        M != P,
        K == N,
        Implies(K == 1, O == 1),
        Implies(M == 1, N == 0)
    ]

def is_fully_determined(option_constraints):
    solver = Solver()
    solver.add(get_base_constraints())
    solver.add(option_constraints)
    
    if solver.check() == unsat:
        return False
    
    # Found at least one model
    m1 = solver.model()
    
    # Check if there's another model
    solver.push()
    # Add constraint to exclude the first model
    solver.add(Or([v != m1[v] for v in vars]))
    
    if solver.check() == sat:
        # Found a second model, so not fully determined
        solver.pop()
        return False
    else:
        solver.pop()
        return True

# Options
# (A) K is published in the fall and L is published in the spring.
# (B) O is published in the fall and P is published in the spring.
# (C) P is published in the fall and L is published in the spring.
# (D) Both K and L are published in the spring.
# (E) Both M and L are published in the fall.

options = [
    ("A", And(K == 1, L == 0)),
    ("B", And(O == 1, P == 0)),
    ("C", And(P == 1, L == 0)),
    ("D", And(K == 0, L == 0)),
    ("E", And(M == 1, L == 1))
]

found_options = []
for letter, constr in options:
    if is_fully_determined(constr):
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