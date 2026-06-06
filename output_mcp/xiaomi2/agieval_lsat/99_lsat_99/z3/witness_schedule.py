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
    """Return list of base constraints from the problem."""
    cons = []
    # Each witness testifies on exactly one day (0, 1, or 2)
    for w in witnesses:
        cons.append(And(w >= 0, w <= 2))
    
    # 1. Franco does not testify on the same day as Garcia
    cons.append(F != G)
    
    # 2. Iturbe testifies on Wednesday
    cons.append(I == Wed)
    
    # 3. Exactly two witnesses testify on Tuesday
    cons.append(Sum([If(w == Tue, 1, 0) for w in witnesses]) == 2)
    
    # 4. Hong does not testify on Monday
    cons.append(H != Mon)
    
    # 5. At least one witness testifies on Monday
    cons.append(Sum([If(w == Mon, 1, 0) for w in witnesses]) >= 1)
    
    return cons

# Define option constraints
# (A) Franco is the only witness scheduled to testify on Monday.
opt_a = And(
    F == Mon,
    G != Mon,
    H != Mon,
    I != Mon,
    J != Mon
)

# (B) Franco is scheduled to testify on the same day as Iturbe.
opt_b = (F == Wed)  # Iturbe is on Wednesday

# (C) Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(G == Tue, H == Tue)

# (D) Garcia is the only witness on Monday AND Hong is one of two witnesses on Wednesday.
opt_d = And(
    G == Mon,
    F != Mon,
    H != Mon,
    I != Mon,  # I is on Wed, already guaranteed
    J != Mon,
    H == Wed,
    # Exactly two on Wednesday: Hong and Iturbe
    Sum([If(w == Wed, 1, 0) for w in witnesses]) == 2
)

# (E) Jackson is on Tuesday AND two witnesses testify on Monday.
opt_e = And(
    J == Tue,
    Sum([If(w == Mon, 1, 0) for w in witnesses]) == 2
)

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

base = base_constraints()

found_options = []
for letter, constr in options:
    solver = Solver()
    solver.add(base)
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT - ", end="")
        for i, w in enumerate(witnesses):
            day_val = m[w].as_long()
            day_name = ['Mon', 'Tue', 'Wed'][day_val]
            print(f"{names[i]}={day_name}", end=" ")
        print()
    else:
        print(f"Option {letter}: UNSAT (CANNOT be true)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")