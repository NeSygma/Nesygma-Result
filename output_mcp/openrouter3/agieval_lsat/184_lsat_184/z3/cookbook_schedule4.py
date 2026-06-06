from z3 import *

# Define seasons: 0 = Fall, 1 = Spring
K, L, M, N, O, P = Ints('K L M N O P')

# Base constraints (without original condition)
base_constraints = [
    M != P,  # M and P cannot be in the same season
    K == N,  # K and N must be in the same season
    Implies(K == 0, O == 0)  # If K is fall, O is fall
]

# Original condition
original_cond = Implies(M == 0, N == 1)

# Options
options = {
    "A": Implies(L == 0, M == 1),  # If L is fall, M is spring
    "B": Implies(N == 0, P == 0),  # If N is fall, P is fall
    "C": Implies(M == 1, P == 0),  # If M is spring, P is fall
    "D": Implies(N == 1, M == 1),  # If N is spring, M is spring
    "E": Implies(O == 1, N == 1)   # If O is spring, N is spring
}

found_options = []

for letter, opt in options.items():
    # Check if original implies option given base constraints
    s1 = Solver()
    s1.add(base_constraints)
    s1.add(original_cond)
    s1.add(Not(opt))
    res1 = s1.check()
    
    # Check if option implies original given base constraints
    s2 = Solver()
    s2.add(base_constraints)
    s2.add(opt)
    s2.add(Not(original_cond))
    res2 = s2.check()
    
    # If both are unsat, they're equivalent
    if res1 == unsat and res2 == unsat:
        found_options.append(letter)
        print(f"Option {letter} is equivalent to original condition")
    else:
        print(f"Option {letter}: res1={res1}, res2={res2}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")