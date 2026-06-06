from z3 import *

# Boolean variables: True = Fall, False = Spring
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

# Base constraints from the problem
solver = Solver()

# M and P cannot be published in the same season
solver.add(Not(M == P))  # M != P

# K and N must be published in the same season
solver.add(K == N)

# If K is published in the fall, O must also be published in the fall
solver.add(Implies(K, O))

# If M is published in the fall, N must be published in the spring
solver.add(Implies(M, Not(N)))

# Now test each option to see which one fully determines the schedule
# "Fully determined" means exactly one model exists

found_options = []

# Option A: K is published in the fall and L is published in the spring
opt_a = And(K, Not(L))

# Option B: O is published in the fall and P is published in the spring
opt_b = And(O, Not(P))

# Option C: P is published in the fall and L is published in the spring
opt_c = And(P, Not(L))

# Option D: Both K and L are published in the spring
opt_d = And(Not(K), Not(L))

# Option E: Both M and L are published in the fall
opt_e = And(M, L)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        # Check if the schedule is fully determined (unique model)
        m = solver.model()
        # Try to find another model that differs
        block = Or([v != m.eval(v, model_completion=True) for v in [K, L, M, N, O, P]])
        solver.add(block)
        result2 = solver.check()
        if result2 == unsat:
            # Only one model exists - fully determined
            found_options.append(letter)
        # else: multiple models, not fully determined
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