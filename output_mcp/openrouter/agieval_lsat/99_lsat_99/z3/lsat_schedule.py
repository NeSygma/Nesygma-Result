from z3 import *

# Create solver and variables
solver = Solver()
# Days: 0=Mon,1=Tue,2=Wed
F = Int('F')  # Franco
G = Int('G')  # Garcia
H = Int('H')  # Hong
I = Int('I')  # Iturbe
J = Int('J')  # Jackson
witnesses = [F, G, H, I, J]

# Domain constraints: each day is 0,1,2
for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Base constraints
# Franco does not testify on the same day that Garcia testifies.
solver.add(F != G)
# Iturbe testifies on Wednesday.
solver.add(I == 2)
# Exactly two witnesses testify on Tuesday.
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
# Hong does not testify on Monday.
solver.add(H != 0)
# At least one witness testifies on Monday.
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Option specific constraints
# A: Franco is the only witness scheduled to testify on Monday.
opt_a_constr = And(
    F == 0,
    G != 0,
    H != 0,
    I != 0,
    J != 0
)
# B: Franco is scheduled to testify on the same day as Iturbe.
opt_b_constr = (F == I)  # Since I == 2, this forces F == 2
# C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c_constr = And(G == 1, H == 1)
# D: Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d_constr = And(
    G == 0,
    F != 0,
    H == 2,
    I == 2,
    J != 0,
    # exactly two witnesses on Wednesday (Iturbe already Wednesday, plus Hong)
    Sum([If(w == 2, 1, 0) for w in witnesses]) == 2
)
# E: Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
opt_e_constr = And(
    J == 1,
    Sum([If(w == 0, 1, 0) for w in witnesses]) == 2
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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