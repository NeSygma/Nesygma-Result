from z3 import *

# Days: 0=Mon,1=Tue,2=Wed
Mon, Tue, Wed = 0, 1, 2

# Witness variables
F = Int('F')  # Franco
G = Int('G')  # Garcia
H = Int('H')  # Hong
I = Int('I')  # Iturbe
J = Int('J')  # Jackson

solver = Solver()
# Domain constraints
for var in [F, G, H, I, J]:
    solver.add(var >= Mon, var <= Wed)

# Base constraints
solver.add(F != G)               # Franco not same day as Garcia
solver.add(I == Wed)             # Iturbe on Wednesday
# Exactly two witnesses on Tuesday
solver.add(Sum([If(F == Tue, 1, 0),
                If(G == Tue, 1, 0),
                If(H == Tue, 1, 0),
                If(I == Tue, 1, 0),
                If(J == Tue, 1, 0)]) == 2)
solver.add(H != Mon)             # Hong not Monday
# At least one witness on Monday
solver.add(Sum([If(F == Mon, 1, 0),
                If(G == Mon, 1, 0),
                If(H == Mon, 1, 0),
                If(I == Mon, 1, 0),
                If(J == Mon, 1, 0)]) >= 1)

# Option constraints
opt_a = And(F == Mon, G == Wed, H == Tue, I == Tue, J == Wed)
opt_b = And(F == Mon, G == Wed, H == Mon, I == Tue, J == Tue)
opt_c = And(F == Tue, G == Mon, H == Wed, I == Tue, J == Wed)
opt_d = And(F == Tue, G == Mon, H == Tue, I == Wed, J == Mon)
opt_e = And(F == Wed, G == Mon, H == Tue, I == Wed, J == Mon)

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