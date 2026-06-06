from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
Mon, Tue, Wed = 0, 1, 2

# Each witness assigned to a day
F = Int('F')  # Franco
G = Int('G')  # Garcia
H = Int('H')  # Hong
I = Int('I')  # Iturbe
J = Int('J')  # Jackson

witnesses = [F, G, H, I, J]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

def base_constraints():
    cons = []
    for w in witnesses:
        cons.append(And(w >= 0, w <= 2))
    cons.append(F != G)           # Franco != Garcia day
    cons.append(I == Wed)         # Iturbe on Wednesday
    cons.append(Sum([If(w == Tue, 1, 0) for w in witnesses]) == 2)  # Exactly 2 on Tuesday
    cons.append(H != Mon)         # Hong not on Monday
    cons.append(Sum([If(w == Mon, 1, 0) for w in witnesses]) >= 1)  # At least 1 on Monday
    return cons

# Option constraints
opt_a = And(F == Mon, G != Mon, H != Mon, I != Mon, J != Mon)
opt_b = (F == Wed)
opt_c = And(G == Tue, H == Tue)
opt_d = And(G == Mon, F != Mon, H != Mon, I != Mon, J != Mon, H == Wed,
            Sum([If(w == Wed, 1, 0) for w in witnesses]) == 2)
opt_e = And(J == Tue, Sum([If(w == Mon, 1, 0) for w in witnesses]) == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
base = base_constraints()

# Track which options CANNOT be true (UNSAT)
cannot_be_true = []
for letter, constr in options:
    solver = Solver()
    solver.add(base)
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter}: SAT (CAN be true)")
    else:
        cannot_be_true.append(letter)
        print(f"Option {letter}: UNSAT (CANNOT be true)")
    solver.pop()

print()
if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options CANNOT be true {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be true")