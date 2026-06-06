from z3 import *

# Declare Boolean variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
solver = Solver()
solver.add(Not(And(M, P)))  # M and P cannot be in the same season
solver.add(K == N)          # K and N must be in the same season
solver.add(Implies(K, O))   # If K is in fall, O must be in fall
solver.add(Implies(M, Not(N)))  # If M is in fall, N must be in spring (i.e., not fall)

# Enumerate all base solutions
base_solutions = []
s = Solver()
s.add(solver.assertions())
while s.check() == sat:
    m = s.model()
    sol = {
        'K': m[K],
        'L': m[L],
        'M': m[M],
        'N': m[N],
        'O': m[O],
        'P': m[P]
    }
    base_solutions.append(sol)
    # Block this model
    block = Or([v != m.eval(v) for v in [K, L, M, N, O, P]])
    s.add(block)

print(f"Total base solutions: {len(base_solutions)}")
for i, sol in enumerate(base_solutions):
    print(f"Solution {i+1}: K={sol['K']}, L={sol['L']}, M={sol['M']}, N={sol['N']}, O={sol['O']}, P={sol['P']}")

# Define options
options = [
    ("A", lambda sol: sol['K'] == True and sol['L'] == False),  # K fall, L spring
    ("B", lambda sol: sol['O'] == True and sol['P'] == False),  # O fall, P spring
    ("C", lambda sol: sol['P'] == True and sol['L'] == False),  # P fall, L spring
    ("D", lambda sol: sol['K'] == False and sol['L'] == False),  # Both K and L spring
    ("E", lambda sol: sol['M'] == True and sol['L'] == True)  # Both M and L fall
]

# Check which option is true in exactly one base solution
found_options = []
for letter, condition in options:
    count = sum(1 for sol in base_solutions if condition(sol))
    print(f"Option {letter}: true in {count} base solutions")
    if count == 1:
        found_options.append(letter)

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