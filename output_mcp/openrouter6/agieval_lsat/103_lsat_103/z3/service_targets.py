from z3 import *

solver = Solver()

# Declare variables
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

# Base constraints
# Domain: website targets 1-3, voicemail targets 1-2 (no 3 days)
solver.add(I_w >= 1, I_w <= 3)
solver.add(I_v >= 1, I_v <= 2)
solver.add(S_w >= 1, S_w <= 3)
solver.add(S_v >= 1, S_v <= 2)
solver.add(T_w >= 1, T_w <= 3)
solver.add(T_v >= 1, T_v <= 2)

# Website <= Voicemail for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Image's voicemail shorter than others
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Solide's website shorter than Truvest's website
solver.add(S_w < T_w)

# Now evaluate options: we want to find which option is NOT necessarily true.
# That is, whose negation is satisfiable.
# We'll use the skeleton with constr being the negation of the option.

found_options = []
for letter, constr in [
    ("A", Not(I_w == 1)),   # Image's website target is NOT 1 day
    ("B", Not(S_w == 2)),   # Solide's website target is NOT 2 days
    ("C", Not(S_v == 2)),   # Solide's voicemail target is NOT 2 days
    ("D", Not(T_w == 2)),   # Truvest's website target is NOT 2 days
    ("E", Not(T_v == 2)),   # Truvest's voicemail target is NOT 2 days
]:
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