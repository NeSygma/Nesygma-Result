from z3 import *

# Base constraints
K = Bool('K')  # True for fall, False for spring
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

solver = Solver()

# M and P cannot be published in the same season as each other.
solver.add(M != P)

# K and N must be published in the same season as each other.
solver.add(K == N)

# If K is published in the fall, O must also be published in the fall.
# K fall means K == True. O fall means O == True.
solver.add(Implies(K, O))

# If M is published in the fall, N must be published in the spring.
# M fall means M == True. N spring means N == False.
solver.add(Implies(M, Not(N)))

# Check base satisfiability
print("Base constraints satisfiability:", solver.check())
if solver.check() == sat:
    print("Base model:", solver.model())
else:
    print("Base unsat")

# Now test each option
options = [
    ("A", And(K == True, L == False)),  # K fall, L spring
    ("B", And(O == True, P == False)),  # O fall, P spring
    ("C", And(P == True, L == False)),  # P fall, L spring
    ("D", And(K == False, L == False)), # Both K and L spring
    ("E", And(M == True, L == True))    # Both M and L fall
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        print(f"Option {letter} is satisfiable")
    else:
        print(f"Option {letter} is unsatisfiable")
    solver.pop()

print("Found options:", found_options)
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")