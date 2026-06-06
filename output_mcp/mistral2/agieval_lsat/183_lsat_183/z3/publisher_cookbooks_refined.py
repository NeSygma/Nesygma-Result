from z3 import *

def is_unique_solution(solver, model_vars):
    # Save the current model
    current_model = solver.model()
    # Create a blocking clause to prevent this exact solution
    blocking_clause = Or([v != current_model[v] for v in model_vars])
    solver.add(blocking_clause)
    # Check if another solution exists
    result = solver.check()
    return result == unsat

solver = Solver()

# Declare symbolic variables for the seasons of each cookbook
# We use 0 for spring and 1 for fall
K, L, M, N, O, P = Ints('K L M N O P')
model_vars = [K, L, M, N, O, P]

solver.add(K >= 0, K <= 1)
solver.add(L >= 0, L <= 1)
solver.add(M >= 0, M <= 1)
solver.add(N >= 0, N <= 1)
solver.add(O >= 0, O <= 1)
solver.add(P >= 0, P <= 1)

# Constraints from the problem statement
# 1. M and P cannot be published in the same season
solver.add(M != P)

# 2. K and N must be published in the same season
solver.add(K == N)

# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K == 1, O == 1))

# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M == 1, N == 0))

found_options = []

# Option A: K is published in the fall and L is published in the spring
opt_a_constr = And(K == 1, L == 0)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    if is_unique_solution(solver, model_vars):
        found_options.append("A")
solver.pop()

# Option B: O is published in the fall and P is published in the spring
opt_b_constr = And(O == 1, P == 0)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    if is_unique_solution(solver, model_vars):
        found_options.append("B")
solver.pop()

# Option C: P is published in the fall and L is published in the spring
opt_c_constr = And(P == 1, L == 0)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    if is_unique_solution(solver, model_vars):
        found_options.append("C")
solver.pop()

# Option D: Both K and L are published in the spring
opt_d_constr = And(K == 0, L == 0)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    if is_unique_solution(solver, model_vars):
        found_options.append("D")
solver.pop()

# Option E: Both M and L are published in the fall
opt_e_constr = And(M == 1, L == 1)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    if is_unique_solution(solver, model_vars):
        found_options.append("E")
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