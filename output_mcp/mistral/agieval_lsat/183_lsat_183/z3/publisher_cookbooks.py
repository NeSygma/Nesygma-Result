from z3 import *

# Base constraints solver
solver = Solver()

# Variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

# Constraints
solver.add(Not(M == P))  # M and P cannot be in the same season
solver.add(K == N)       # K and N must be in the same season
solver.add(Implies(K, O))  # If K is in fall, O must be in fall
solver.add(Implies(M, Not(N)))  # If M is in fall, N must be in spring

# Option constraints
opt_a_constr = And(K, Not(L))
opt_b_constr = And(O, Not(P))
opt_c_constr = And(P, Not(L))
opt_d_constr = And(Not(K), Not(L))
opt_e_constr = And(M, Not(L))

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if the solution is unique by blocking the current model
        model = solver.model()
        # Create a blocking clause to exclude this model
        blocking = []
        for var in [K, L, M, N, O, P]:
            blocking.append(var != model[var])
        solver.add(Or(blocking))
        # Check again; if unsat, the solution is unique
        if solver.check() == unsat:
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