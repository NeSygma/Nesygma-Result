from z3 import *

# Companies: 0=RealProp,1=Southco,2=Trustcorp
# Buildings indices and classes
buildings = [
    ('Garza', 1),   # 0
    ('Flores', 1),  # 1
    ('Yates', 3),   # 2
    ('Zimmer', 3),  # 3
    ('Lynch', 2),   # 4
    ('King', 2),    # 5
    ('Meyer', 2),   # 6
    ('Ortiz', 2)    # 7
]

n = len(buildings)
owner = [Int(f'owner_{i}') for i in range(n)]
solver = Solver()
# domain constraints
for o in owner:
    solver.add(o >= 0, o <= 2)
# At most one class 1 building per company (derived from trade rules)
for comp in range(3):
    solver.add(Sum([If(And(owner[i] == comp, buildings[i][1] == 1), 1, 0) for i in range(n)]) <= 1)

# Define option constraints
opt_a = And(owner[0] == 0, owner[1] == 0)  # RP owns Garza and Flores
opt_b = And(owner[1] == 1, owner[6] == 1)  # SC owns Flores and Meyer
opt_c = And(owner[0] == 1, owner[4] == 1)  # SC owns Garza and Lynch
opt_d = And(owner[1] == 2, owner[7] == 2)  # TC owns Flores and Ortiz
opt_e = And(owner[0] == 2, owner[6] == 2)  # TC owns Garza and Meyer

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")