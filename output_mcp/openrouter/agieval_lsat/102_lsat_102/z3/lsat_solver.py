from z3 import *

# Base constraints
# Days: 0=Mon,1=Tue,2=Wed
F = Int('F')  # Franco
G = Int('G')  # Garcia
H = Int('H')  # Hong
I = Int('I')  # Iturbe
J = Int('J')  # Jackson
vars = [F, G, H, I, J]

solver = Solver()
# each witness on a day 0..2
for v in vars:
    solver.add(v >= 0, v <= 2)
# Franco does not testify on same day as Garcia
solver.add(F != G)
# Iturbe on Wednesday
solver.add(I == 2)
# Exactly two witnesses on Tuesday (day 1)
cntTue = Sum([If(v == 1, 1, 0) for v in vars])
solver.add(cntTue == 2)
# Hong not Monday
solver.add(H != 0)
# At least one witness on Monday
cntMon = Sum([If(v == 0, 1, 0) for v in vars])
solver.add(cntMon >= 1)
# Additional condition: Franco same day as Hong
solver.add(F == H)

# Options to test (must be true)
opt_A = (F == 2)                     # Franco Wednesday
opt_B = (G == 0)                     # Garcia Monday
opt_C = (G == 2)                     # Garcia Wednesday
opt_D = (H == 1)                     # Hong Tuesday
opt_E = And(I == 2, Sum([If(v == 2, 1, 0) for v in vars]) == 1)  # Iturbe only on Wed

options = [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]

found_options = []
for letter, expr in options:
    solver.push()
    # If adding the negation makes the problem unsat, then expr is forced.
    solver.add(Not(expr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")