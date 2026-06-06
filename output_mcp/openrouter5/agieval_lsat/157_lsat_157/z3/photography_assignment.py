from z3 import *

# Six photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
# Two ceremonies: Silva (S) and Thorne (T)
# Each photographer can be assigned to S, T, or not assigned (0).
# We'll use Int variables with domain {0, S, T} where S=1, T=2, 0=unassigned.

S = 1
T = 2
NONE = 0

Frost = Int('Frost')
Gonzalez = Int('Gonzalez')
Heideck = Int('Heideck')
Knutson = Int('Knutson')
Lai = Int('Lai')
Mays = Int('Mays')

photographers = [Frost, Gonzalez, Heideck, Knutson, Lai, Mays]

solver = Solver()

# Domain: each photographer is assigned to S, T, or not assigned
for p in photographers:
    solver.add(Or(p == S, p == T, p == NONE))

# At least two photographers at each ceremony
solver.add(Sum([If(p == S, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(p == T, 1, 0) for p in photographers]) >= 2)

# No photographer can be assigned to both ceremonies (already enforced by domain)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony.
# They must be assigned to the same ceremony (both S or both T), and neither is NONE.
solver.add(Frost != NONE)
solver.add(Heideck != NONE)
solver.add(Frost == Heideck)

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies.
# "Both assigned" means neither is NONE.
solver.add(Implies(And(Lai != NONE, Mays != NONE), Lai != Mays))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne.
solver.add(Implies(Gonzalez == S, Lai == T))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it.
solver.add(Implies(Knutson != T, And(Heideck == T, Mays == T)))

# Now evaluate each option.
# Each option gives a complete assignment for Silva University.
# We need to check if there exists a full assignment (including Thorne and unassigned)
# consistent with the option's Silva assignment.

# Option A: Frost, Gonzalez, Heideck, Knutson at Silva
opt_a = And(Frost == S, Gonzalez == S, Heideck == S, Knutson == S,
            Lai != S, Mays != S)  # Lai and Mays not at Silva (complete assignment)

# Option B: Frost, Gonzalez, Heideck at Silva
opt_b = And(Frost == S, Gonzalez == S, Heideck == S,
            Knutson != S, Lai != S, Mays != S)

# Option C: Gonzalez, Knutson at Silva
opt_c = And(Gonzalez == S, Knutson == S,
            Frost != S, Heideck != S, Lai != S, Mays != S)

# Option D: Heideck, Lai at Silva
opt_d = And(Heideck == S, Lai == S,
            Frost != S, Gonzalez != S, Knutson != S, Mays != S)

# Option E: Knutson, Mays at Silva
opt_e = And(Knutson == S, Mays == S,
            Frost != S, Gonzalez != S, Heideck != S, Lai != S)

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