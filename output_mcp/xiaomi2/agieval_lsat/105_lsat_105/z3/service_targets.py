from z3 import *

solver = Solver()

# Variables: client targets (website and voicemail)
# Clients: Image (I), Solide (S), Truvest (T)
I_w = Int('I_w')  # Image website
I_v = Int('I_v')  # Image voicemail
S_w = Int('S_w')  # Solide website
S_v = Int('S_v')  # Solide voicemail
T_w = Int('T_w')  # Truvest website
T_v = Int('T_v')  # Truvest voicemail

all_vars = [I_w, I_v, S_w, S_v, T_w, T_v]

# Domain: each target is 1, 2, or 3 days
for v in all_vars:
    solver.add(Or(v == 1, v == 2, v == 3))

# Constraint 1: Website target <= voicemail target for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Constraint 2: Image's voicemail target is shorter than other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Constraint 3: Solide's website target is shorter than Truvest's website target
solver.add(S_w < T_w)

# Given: Image's website target is 2 days
solver.add(I_w == 2)

# Now check each option: which MUST be 2?
# An option "must be 2" means: in ALL valid models, that variable equals 2.
# Equivalently: if we add the constraint that variable != 2, and get UNSAT, then it must be 2.

options = [
    ("A", I_v, "Image's voicemail target"),
    ("B", S_w, "Solide's website target"),
    ("C", S_v, "Solide's voicemail target"),
    ("D", T_w, "Truvest's website target"),
    ("E", T_v, "Truvest's voicemail target"),
]

must_be_2 = []
for letter, var, desc in options:
    s = Solver()
    # Add all base constraints
    for v in all_vars:
        s.add(Or(v == 1, v == 2, v == 3))
    s.add(I_w <= I_v)
    s.add(S_w <= S_v)
    s.add(T_w <= T_v)
    s.add(I_v < S_v)
    s.add(I_v < T_v)
    s.add(S_w < T_w)
    s.add(I_w == 2)
    # Try to make this variable NOT 2
    s.add(var != 2)
    if s.check() == unsat:
        must_be_2.append(letter)
        print(f"Option ({letter}) {desc}: MUST be 2 (unsat when != 2)")
    else:
        m = s.model()
        print(f"Option ({letter}) {desc}: NOT necessarily 2 (found model with {var}={m[var]})")

print()
if len(must_be_2) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_2[0]}")
elif len(must_be_2) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be 2: {must_be_2}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be 2")