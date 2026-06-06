from z3 import *

# Encode the problem: 6 employees, 6 spaces (1-6)
R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Each option constraint as a Z3 expression
opt_A = (S == 4)
opt_B = (T == 2)
opt_C = (V == 5)
opt_D = (X == 6)
opt_E = (Y == 2)

# --- Approach 1: Check entailment (must-be-true) using NOT(option) ---
# If premises + NOT(option) is unsat, then option MUST be true.

print("=== Checking each option for entailment (must be true) ===")
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
    s = Solver()
    # Domain constraints
    for e in employees:
        s.add(e >= 1, e <= 6)
    s.add(Distinct(employees))
    # Order constraints
    s.add(Y > T)   # Young > Togowa
    s.add(X > S)   # Xu > Souza
    s.add(R > Y)   # Robertson > Young
    s.add(R >= 1, R <= 4)  # Robertson in 1-4
    # Additional condition
    s.add(R == 3)
    # Negate the option — if unsat, option is forced
    s.add(Not(constr))
    
    res = s.check()
    if res == unsat:
        found_options.append(letter)
        print(f"Option {letter} (Not({constr})) -> UNSAT, so {letter} MUST be true")
    else:
        print(f"Option {letter} (Not({constr})) -> {res}, so {letter} can be false")

print(f"\nOptions that MUST be true: {found_options}")

# --- Approach 2: Enumerate all solutions to verify ---
s2 = Solver()
for e in employees:
    s2.add(e >= 1, e <= 6)
s2.add(Distinct(employees))
s2.add(Y > T)
s2.add(X > S)
s2.add(R > Y)
s2.add(R >= 1, R <= 4)
s2.add(R == 3)

all_solutions = []
while s2.check() == sat:
    m = s2.model()
    sol = {str(e): m.eval(e).as_long() for e in employees}
    all_solutions.append(sol)
    # Block this exact assignment
    s2.add(Or([e != m.eval(e) for e in employees]))

print(f"\n=== Total solutions: {len(all_solutions)} ===")

# Check which option holds in ALL solutions
def check_option_in_all(constr):
    for sol in all_solutions:
        # Evaluate the Z3 constraint with the model values
        # We can just re-check by adding the constraint to a fresh solver
        pass
    return True

# For each option, re-check in all solutions
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
    count_true = 0
    for sol in all_solutions:
        s_check = Solver()
        for e in employees:
            s_check.add(e == sol[str(e)])
        s_check.add(constr)
        if s_check.check() == sat:
            count_true += 1
    print(f"Option {letter}: true in {count_true}/{len(all_solutions)} solutions")

# Determine answer
if len(found_options) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No options found")