from z3 import *

# Base constraints
def create_solver_with_base():
    s = Solver()
    Robertson = Int('Robertson')
    Souza = Int('Souza')
    Togowa = Int('Togowa')
    Vaughn = Int('Vaughn')
    Xu = Int('Xu')
    Young = Int('Young')
    
    employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
    
    for e in employees:
        s.add(e >= 1, e <= 6)
    s.add(Distinct(employees))
    
    s.add(Young > Togowa)
    s.add(Xu > Souza)
    s.add(Robertson > Young)
    s.add(Robertson >= 1, Robertson <= 4)
    s.add(Robertson == 3)
    
    return s, Robertson, Souza, Togowa, Vaughn, Xu, Young

# Check each option: if negating it makes it UNSAT, then it MUST be true
options = {
    "A": lambda S, T, V, X, Y, R: (S == 4),  # Souza == 4
    "B": lambda S, T, V, X, Y, R: (T == 2),  # Togowa == 2
    "C": lambda S, T, V, X, Y, R: (V == 5),  # Vaughn == 5
    "D": lambda S, T, V, X, Y, R: (X == 6),  # Xu == 6
    "E": lambda S, T, V, X, Y, R: (Y == 2),  # Young == 2
}

must_be_true = []

for letter, opt_fn in options.items():
    s, Robertson, Souza, Togowa, Vaughn, Xu, Young = create_solver_with_base()
    # Try to find a model where the option is FALSE
    s.add(Not(opt_fn(Souza, Togowa, Vaughn, Xu, Young, Robertson)))
    result = s.check()
    if result == unsat:
        # Cannot be false, so it MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")