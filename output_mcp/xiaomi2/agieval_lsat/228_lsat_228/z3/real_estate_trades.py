from z3 import *

solver = Solver()

# Buildings: (name, class)
# Owners: 0=RP, 1=SC, 2=TC
buildings = [
    ('Garza', 1),    # 0 - initially RP
    ('Yates', 3),    # 1 - initially RP
    ('Zimmer', 3),   # 2 - initially RP
    ('Flores', 1),   # 3 - initially SC
    ('Lynch', 2),    # 4 - initially SC
    ('King', 2),     # 5 - initially TC
    ('Meyer', 2),    # 6 - initially TC
    ('Ortiz', 2),    # 7 - initially TC
]

n = len(buildings)

# Final owner of each building
owner = [Int(f'owner_{i}') for i in range(n)]

# Each building has exactly one owner
for i in range(n):
    solver.add(Or(owner[i] == 0, owner[i] == 1, owner[i] == 2))

# RealProp owns only class 2 buildings
for i in range(n):
    if buildings[i][1] != 2:
        solver.add(owner[i] != 0)

# Value invariant: each trade preserves per-company value
# Trade type 1: 1 Cx <-> 1 Cx (same value)
# Trade type 2: 1 C1 <-> 2 C2 (4 = 2*2)
# Trade type 3: 1 C2 <-> 2 C3 (2 = 2*1)
# So C1=4, C2=2, C3=1. Each company starts at value 6, ends at value 6.
for company in range(3):
    total = Sum([If(owner[i] == company, 
                    4 if buildings[i][1] == 1 else (2 if buildings[i][1] == 2 else 1), 
                    0) 
                 for i in range(n)])
    solver.add(total == 6)

# Verify base constraints are satisfiable
if solver.check() == sat:
    m = solver.model()
    print("Base constraints satisfiable. Example model:")
    for i in range(n):
        own = m[owner[i]].as_long()
        own_name = ['RP', 'SC', 'TC'][own]
        print(f"  {buildings[i][0]} (C{buildings[i][1]}): {own_name}")
else:
    print("ERROR: Base constraints unsatisfiable")

# Answer choices
# (A) Trustcorp owns a class 1 building
opt_a = Or([And(owner[i] == 2, buildings[i][1] == 1) for i in range(n)])

# (B) Trustcorp owns the Meyer Building
opt_b = (owner[6] == 2)

# (C) Southco owns a class 2 building
opt_c = Or([And(owner[i] == 1, buildings[i][1] == 2) for i in range(n)])

# (D) Southco owns both class 3 buildings
opt_d = And(owner[1] == 1, owner[2] == 1)

# (E) Southco owns the Flores Tower
opt_e = (owner[3] == 1)

# Check which MUST be true (negation is unsat given base constraints)
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        found_options.append(letter)
        print(f"Option {letter}: MUST be true (negation unsat)")
    elif result == sat:
        m2 = solver.model()
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
    else:
        print(f"Option {letter}: unknown")
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