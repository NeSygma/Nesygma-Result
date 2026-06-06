from z3 import *

# Days: 0=Mon,1=Tue,2=Wed
F = Int('F')
G = Int('G')
H = Int('H')
I = Int('I')
J = Int('J')

solver = Solver()
# Domain constraints
for w in [F,G,H,I,J]:
    solver.add(w >= 0, w <= 2)
# Base constraints
solver.add(F != G)               # Franco not same day as Garcia
solver.add(I == 2)               # Iturbe Wednesday
# Exactly two witnesses on Tuesday (day 1)
solver.add(Sum([If(F == 1, 1, 0),
               If(G == 1, 1, 0),
               If(H == 1, 1, 0),
               If(I == 1, 1, 0),
               If(J == 1, 1, 0)]) == 2)
solver.add(H != 0)               # Hong not Monday
# At least one witness on Monday
solver.add(Sum([If(F == 0, 1, 0),
               If(G == 0, 1, 0),
               If(H == 0, 1, 0),
               If(I == 0, 1, 0),
               If(J == 0, 1, 0)]) >= 1)
# Jackson only witness on Monday
solver.add(J == 0)
for w in [F, G, H, I]:
    solver.add(w != 0)

# Option expressions
A_expr = (F == 2)          # Franco Wednesday
B_expr = (H == 1)          # Hong Tuesday
C_expr = (G == 1)          # Garcia Tuesday
D_expr = (F == H)          # Franco same day as Hong
E_expr = (G == H)          # Garcia same day as Hong
options = [("A", A_expr), ("B", B_expr), ("C", C_expr), ("D", D_expr), ("E", E_expr)]

forced_options = []
for letter, expr in options:
    solver.push()
    # Add negation of the option; if unsat, then option must be true
    solver.add(Not(expr))
    if solver.check() == unsat:
        forced_options.append(letter)
    solver.pop()

if len(forced_options) == 1:
    print("STATUS: sat")
    print(f"answer:{forced_options[0]}")
elif len(forced_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")