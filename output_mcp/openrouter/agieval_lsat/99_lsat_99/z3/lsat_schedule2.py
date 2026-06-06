from z3 import *

solver = Solver()
# Days: 0=Mon,1=Tue,2=Wed
F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]
for w in witnesses:
    solver.add(And(w >= 0, w <= 2))
# Base constraints
solver.add(F != G)
solver.add(I == 2)
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
solver.add(H != 0)
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Option constraints
opt_a = And(F == 0, G != 0, H != 0, I != 0, J != 0)
opt_b = (F == I)  # F == 2
opt_c = And(G == 1, H == 1)
opt_d = And(G == 0, F != 0, H == 2, I == 2, J != 0,
            Sum([If(w == 2, 1, 0) for w in witnesses]) == 2)
opt_e = And(J == 1, Sum([If(w == 0, 1, 0) for w in witnesses]) == 2)
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

sat_opts = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        sat_opts.append(letter)
    solver.pop()

# Determine which option is impossible (i.e., not in sat_opts)
all_letters = [letter for letter, _ in options]
impossible = [l for l in all_letters if l not in sat_opts]
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
else:
    # fallback
    print("STATUS: unsat")
    print(f"Refine: impossible options {impossible}, sat options {sat_opts}")