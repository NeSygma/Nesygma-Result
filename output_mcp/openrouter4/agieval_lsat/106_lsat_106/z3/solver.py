from z3 import *

solver = Solver()

# Variables: targets in days (1=1day, 2=2days, 3=3days)
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

# Domains: all must be 1, 2, or 3
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: website target <= voicemail target for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail < other clients' voicemail
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website < Truvest's website
solver.add(S_w < T_w)

# Additional: Solide's voicemail < Truvest's website
solver.add(S_v < T_w)

# Now test each option: could each target be 2 days?
options = [
    ("A", I_w == 2),
    ("B", I_v == 2),
    ("C", S_w == 2),
    ("D", T_v == 2),
    ("E", T_w == 2)
]

found_options = []
for letter, constr in options:
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