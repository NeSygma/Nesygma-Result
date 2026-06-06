from z3 import *

def get_solutions(base_constraints):
    solver = Solver()
    K, L, M, N, O, P = Bools('K L M N O P')
    vars_list = [K, L, M, N, O, P]
    
    for c in base_constraints:
        solver.add(c)
    
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        # Convert BoolRef to Python bool for each variable
        sol = tuple(m.eval(v) for v in vars_list)
        # Convert to Python bools for sorting and comparison
        sol_py = tuple(v for v in sol)  # still BoolRef? Actually m.eval returns BoolRef but we can use is_true
        sol_bool = tuple(is_true(m.eval(v)) for v in vars_list)
        solutions.add(sol_bool)
        # Block this solution using BoolRef values
        solver.add(Or([v != m.eval(v) for v in vars_list]))
    return solutions

K, L, M, N, O, P = Bools('K L M N O P')

base_constraints = [
    M != P,
    K == N,
    Implies(K, O)
]

orig_c4 = Implies(M, Not(N))

original_solutions = get_solutions(base_constraints + [orig_c4])
print(f"Original solutions count: {len(original_solutions)}")
for sol in sorted(original_solutions):
    print(sol)
print()

options = {
    "A": Implies(L, Not(M)),
    "B": Implies(N, P),
    "C": Implies(Not(M), P),
    "D": Implies(Not(N), Not(M)),
    "E": Implies(Not(O), Not(N))
}

for letter, opt_constraint in options.items():
    opt_solutions = get_solutions(base_constraints + [opt_constraint])
    print(f"Option {letter} solutions count: {len(opt_solutions)}")
    if opt_solutions == original_solutions:
        print(f"  -> MATCHES original!")
    else:
        print(f"  -> Does NOT match original")
        only_orig = original_solutions - opt_solutions
        only_opt = opt_solutions - original_solutions
        if only_orig:
            print(f"  Only in original: {only_orig}")
        if only_opt:
            print(f"  Only in option: {only_opt}")
    print()