from z3 import *

# Variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

solver = Solver()

# Original base constraints (excluding C4 which we're testing to replace)
# C1: M and P cannot be in the same season
solver.add(M != P)
# C2: K and N must be in the same season
solver.add(K == N)
# C3: If K is in fall, O must be in fall
solver.add(Implies(K, O))
# C4 (original): If M is in fall, N must be in spring
# solver.add(Implies(M, Not(N)))  # We're replacing this

# Now test each option as a substitute for C4
# We need to check which option (when added to C1-C3) produces the SAME set of allowed schedules
# as the original C1-C4.

# First compute original solutions
orig_solver = Solver()
orig_solver.add(M != P)
orig_solver.add(K == N)
orig_solver.add(Implies(K, O))
orig_solver.add(Implies(M, Not(N)))

orig_solutions = set()
while orig_solver.check() == sat:
    m = orig_solver.model()
    sol = tuple(is_true(m.eval(v)) for v in [K, L, M, N, O, P])
    orig_solutions.add(sol)
    orig_solver.add(Or([v != m.eval(v) for v in [K, L, M, N, O, P]]))

print(f"Original solutions ({len(orig_solutions)}):")
for s in sorted(orig_solutions):
    print(f"  K={s[0]}, L={s[1]}, M={s[2]}, N={s[3]}, O={s[4]}, P={s[5]}")
print()

# Define options as constraints
# Option A: If L is in fall, M must be in spring  => Implies(L, Not(M))
# Option B: If N is in fall, P must be in fall    => Implies(N, P)
# Option C: If M is in spring, P must be in fall  => Implies(Not(M), P)
# Option D: If N is in spring, M must be in spring => Implies(Not(N), Not(M))
# Option E: If O is in spring, N must be in spring => Implies(Not(O), Not(N))

options = {
    "A": Implies(L, Not(M)),
    "B": Implies(N, P),
    "C": Implies(Not(M), P),
    "D": Implies(Not(N), Not(M)),
    "E": Implies(Not(O), Not(N))
}

found_options = []

for letter, opt_constr in options.items():
    # Build solver with C1, C2, C3, and this option
    s = Solver()
    s.add(M != P)
    s.add(K == N)
    s.add(Implies(K, O))
    s.add(opt_constr)
    
    opt_solutions = set()
    while s.check() == sat:
        m = s.model()
        sol = tuple(is_true(m.eval(v)) for v in [K, L, M, N, O, P])
        opt_solutions.add(sol)
        s.add(Or([v != m.eval(v) for v in [K, L, M, N, O, P]]))
    
    print(f"Option {letter} solutions ({len(opt_solutions)}):")
    for sol in sorted(opt_solutions):
        print(f"  K={sol[0]}, L={sol[1]}, M={sol[2]}, N={sol[3]}, O={sol[4]}, P={sol[5]}")
    
    if opt_solutions == orig_solutions:
        print(f"  -> MATCHES original!")
        found_options.append(letter)
    else:
        print(f"  -> Does NOT match original")
    print()

print(f"Found options that match: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")