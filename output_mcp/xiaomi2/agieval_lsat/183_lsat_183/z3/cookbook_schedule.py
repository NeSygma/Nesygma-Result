from z3 import *

solver = Solver()

# Variables: True = Fall, False = Spring
K, L, M, N, O, P = Bools('K L M N O P')
all_vars = [K, L, M, N, O, P]

# Base constraints
# 1. M and P cannot be published in the same season
solver.add(M != P)
# 2. K and N must be published in the same season
solver.add(K == N)
# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K, O))
# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M, Not(N)))

# Option constraints
opt_a = And(K, Not(L))          # (A) K fall, L spring
opt_b = And(O, Not(P))          # (B) O fall, P spring
opt_c = And(P, Not(L))          # (C) P fall, L spring
opt_d = And(Not(K), Not(L))     # (D) K spring, L spring
opt_e = And(M, L)               # (E) M fall, L fall

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        # Check if the solution is unique (fully determined)
        m = solver.model()
        solver.push()
        # Add blocking clause: at least one variable must differ
        solver.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))
        if solver.check() == unsat:
            # Only one solution exists — schedule is fully determined
            found_options.append(letter)
            print(f"Option {letter}: UNIQUE solution - fully determines schedule")
            print(f"  K={m.eval(K)}, L={m.eval(L)}, M={m.eval(M)}, N={m.eval(N)}, O={m.eval(O)}, P={m.eval(P)}")
        else:
            print(f"Option {letter}: Multiple solutions exist - does NOT fully determine schedule")
        solver.pop()
    else:
        print(f"Option {letter}: Not satisfiable with base constraints")
    solver.pop()

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