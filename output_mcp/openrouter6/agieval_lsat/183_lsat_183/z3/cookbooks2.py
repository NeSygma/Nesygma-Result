from z3 import *

# Base constraints
K = Bool('K')  # True for fall, False for spring
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

variables = [K, L, M, N, O, P]

base_solver = Solver()
base_solver.add(M != P)
base_solver.add(K == N)
base_solver.add(Implies(K, O))
base_solver.add(Implies(M, Not(N)))

print("Base constraints satisfiability:", base_solver.check())
if base_solver.check() == sat:
    print("Base model:", base_solver.model())
else:
    print("Base unsat")

# Options
options = [
    ("A", And(K == True, L == False)),  # K fall, L spring
    ("B", And(O == True, P == False)),  # O fall, P spring
    ("C", And(P == True, L == False)),  # P fall, L spring
    ("D", And(K == False, L == False)), # Both K and L spring
    ("E", And(M == True, L == True))    # Both M and L fall
]

found_options = []
for letter, constr in options:
    solver = Solver()
    # Add base constraints
    solver.add(M != P)
    solver.add(K == N)
    solver.add(Implies(K, O))
    solver.add(Implies(M, Not(N)))
    # Add option condition
    solver.add(constr)
    
    # Check satisfiability
    if solver.check() != sat:
        print(f"Option {letter} is unsatisfiable")
        continue
    
    # Get first model
    m1 = solver.model()
    print(f"Option {letter} first model: {m1}")
    
    # Add blocking clause to exclude this exact model
    blocking = Or([v != m1.eval(v, model_completion=True) for v in variables])
    solver.add(blocking)
    
    # Check if there is a second model
    if solver.check() == sat:
        print(f"Option {letter} has at least two models -> not fully determined")
    else:
        print(f"Option {letter} has exactly one model -> fully determined")
        found_options.append(letter)

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