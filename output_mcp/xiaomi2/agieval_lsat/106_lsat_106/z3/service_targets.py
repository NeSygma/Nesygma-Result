from z3 import *

solver = Solver()

# Variables: each client has a website target and a voicemail target
# Values are 1, 2, or 3 days
I_w = Int('I_w')  # Image website
I_v = Int('I_v')  # Image voicemail
S_w = Int('S_w')  # Solide website
S_v = Int('S_v')  # Solide voicemail
T_w = Int('T_w')  # Truvest website
T_v = Int('T_v')  # Truvest voicemail

all_vars = [I_w, I_v, S_w, S_v, T_w, T_v]

# Domain: each target is 1, 2, or 3
for v in all_vars:
    solver.add(And(v >= 1, v <= 3))

# Constraint 1: Website target <= voicemail target for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Constraint 2: Image's voicemail target is shorter than other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Constraint 3: Solide's website target is shorter than Truvest's website target
solver.add(S_w < T_w)

# Additional condition: Solide's voicemail target is shorter than Truvest's website target
solver.add(S_v < T_w)

# Now test each option: which target COULD be 2 days?
# "Could be" means: is there a satisfying assignment where that target equals 2?

options = [
    ("A", I_w == 2),  # Image's website target
    ("B", I_v == 2),  # Image's voicemail target
    ("C", S_w == 2),  # Solide's website target
    ("D", T_v == 2),  # Truvest's voicemail target
    ("E", T_w == 2),  # Truvest's website target
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: I_w={m[I_w]}, I_v={m[I_v]}, S_w={m[S_w]}, S_v={m[S_v]}, T_w={m[T_w]}, T_v={m[T_v]}")
    else:
        print(f"Option {letter} is UNSAT")
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