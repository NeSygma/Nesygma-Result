from z3 import *

# Decision variables: 0 = not assigned, 1 = Silva, 2 = Thorne
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
vars = {name: Int(name) for name in photographers}
solver = Solver()

# Domain constraints
for v in vars.values():
    solver.add(Or(v == 0, v == 1, v == 2))

# At least two photographers at each ceremony
silva_count = Sum([If(v == 1, 1, 0) for v in vars.values()])
thorne_count = Sum([If(v == 2, 1, 0) for v in vars.values()])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Frost together with Heideck at same ceremony (non-zero)
F = vars['Frost']
H = vars['Heideck']
solver.add(F == H, F != 0)

# If Lai and Mays both assigned, they must be to different ceremonies
L = vars['Lai']
M = vars['Mays']
solver.add(Not(And(L != 0, M != 0, L == M)))

# If Gonzalez assigned to Silva, then Lai must be assigned to Thorne
G = vars['Gonzalez']
solver.add(Implies(G == 1, L == 2))

# Define option constraints
K = vars['Knutson']
# A: (K == 1) => not both H and M assigned to Silva
opt_a = Implies(K == 1, Not(And(H == 1, M == 1)))
# B: (K == 1) => L == 1
opt_b = Implies(K == 1, L == 1)
# C: (K != 2) => (F == 2 and M == 2)
opt_c = Implies(K != 2, And(F == 2, M == 2))
# D: (K != 2) => not (H and L same ceremony)
opt_d = Implies(K != 2, Not(And(H != 0, L != 0, H == L)))
# E: (Heideck !=2 and Mays !=2) => K ==2
opt_e = Implies(And(H != 2, M != 2), K == 2)

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