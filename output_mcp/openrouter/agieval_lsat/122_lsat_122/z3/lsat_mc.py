from z3 import *

def all_models(solver, vars_list):
    models = []
    while solver.check() == sat:
        m = solver.model()
        tup = tuple(m.eval(v).as_long() for v in vars_list)
        models.append(tup)
        # block this model
        solver.add(Or([v != m.eval(v) for v in vars_list]))
    return set(models)

# Variables: slots for each band
U = Int('U')
V = Int('V')
W = Int('W')
X = Int('X')
Y = Int('Y')
Z = Int('Z')
vars_all = [U,V,W,X,Y,Z]

# Base constraints common to all
base = []
base.append(And(U >= 1, U <= 6))
base.append(And(V >= 1, V <= 6))
base.append(And(W >= 1, W <= 6))
base.append(And(X >= 1, X <= 6))
base.append(And(Y >= 1, Y <= 6))
base.append(And(Z >= 1, Z <= 6))
base.append(Distinct(vars_all))
# Vegemite earlier than Zircon
base.append(V < Z)
# Uneasy in last three slots
base.append(Or(U == 4, U == 5, U == 6))
# Yardsign in first three slots
base.append(Or(Y == 1, Y == 2, Y == 3))

# Original constraint: W < X and Z < X
orig = And(W < X, Z < X)

# Compute original models
solver_orig = Solver()
for c in base:
    solver_orig.add(c)
solver_orig.add(orig)
orig_models = all_models(solver_orig, vars_all)

# Define option constraints
opt_constraints = {}
# A: Only Uneasy can be later than Xpert -> V <= X, W <= X, Y <= X, Z <= X
opt_constraints['A'] = And(V <= X, W <= X, Y <= X, Z <= X)
# B: V < W < Z
opt_constraints['B'] = And(V < W, W < Z)
# C: V < X and W < X
opt_constraints['C'] = And(V < X, W < X)
# D: X is immediately before or after U
opt_constraints['D'] = Or(X == U - 1, X == U + 1)
# E: X in {5,6}
opt_constraints['E'] = Or(X == 5, X == 6)

found_options = []
for letter, constr in opt_constraints.items():
    s = Solver()
    for c in base:
        s.add(c)
    s.add(constr)
    models = all_models(s, vars_all)
    if models == orig_models:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")