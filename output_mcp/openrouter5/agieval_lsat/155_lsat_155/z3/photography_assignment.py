from z3 import *

# Six photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
# Two ceremonies: Silva University (S) and Thorne University (T)
# Each photographer can be assigned to S, T, or not assigned (N).
# We'll use Int variables: 0 = not assigned, 1 = Silva, 2 = Thorne

F, G, H, K, L, M = Ints('F G H K L M')
photographers = [F, G, H, K, L, M]
names = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

solver = Solver()

# Domain: 0 = not assigned, 1 = Silva, 2 = Thorne
for p in photographers:
    solver.add(Or(p == 0, p == 1, p == 2))

# At least two photographers at each ceremony
solver.add(Sum([If(p == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(p == 2, 1, 0) for p in photographers]) >= 2)

# No photographer can be assigned to both ceremonies (already enforced by domain)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony.
# They must be assigned to the same ceremony (both 1 or both 2), and neither is 0.
solver.add(F != 0)
solver.add(H != 0)
solver.add(F == H)

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies.
# "Both assigned" means L != 0 and M != 0. Then L != M.
solver.add(Implies(And(L != 0, M != 0), L != M))

# Constraint 3: If Gonzalez is assigned to Silva (1), then Lai must be assigned to Thorne (2).
solver.add(Implies(G == 1, L == 2))

# Constraint 4: If Knutson is not assigned to Thorne (not 2), then both Heideck and Mays must be assigned to it (2).
# K != 2 means K is either 0 or 1.
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Now define each option as a set of constraints
# Option A: Silva: Gonzalez, Lai | Thorne: Frost, Heideck, Mays
opt_a = And(
    G == 1, L == 1,  # Silva
    F == 2, H == 2, M == 2,  # Thorne
    K == 0  # Knutson not assigned
)

# Option B: Silva: Gonzalez, Mays | Thorne: Knutson, Lai
opt_b = And(
    G == 1, M == 1,  # Silva
    K == 2, L == 2,  # Thorne
    F == 0, H == 0  # Frost, Heideck not assigned
)

# Option C: Silva: Frost, Gonzalez, Heideck | Thorne: Knutson, Lai, Mays
opt_c = And(
    F == 1, G == 1, H == 1,  # Silva
    K == 2, L == 2, M == 2   # Thorne
)

# Option D: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Lai
opt_d = And(
    F == 1, H == 1, M == 1,  # Silva
    G == 2, L == 2,  # Thorne
    K == 0  # Knutson not assigned
)

# Option E: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Knutson, Lai
opt_e = And(
    F == 1, H == 1, M == 1,  # Silva
    G == 2, K == 2, L == 2   # Thorne
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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