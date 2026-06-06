from z3 import *

# Clients: 0=Image, 1=Solide, 2=Truvest
# Domain: 1, 2, or 3 days

# Variables: website and voicemail for each client
W = [Int(f'W_{i}') for i in range(3)]  # website targets
V = [Int(f'V_{i}') for i in range(3)]  # voicemail targets

solver = Solver()

# Domain constraints: 1, 2, or 3
for i in range(3):
    solver.add(Or(W[i] == 1, W[i] == 2, W[i] == 3))
    solver.add(Or(V[i] == 1, V[i] == 2, V[i] == 3))

# Condition 1: For each client, website <= voicemail
for i in range(3):
    solver.add(W[i] <= V[i])

# Condition 2: Image's voicemail < Solide's voicemail AND Image's voicemail < Truvest's voicemail
solver.add(V[0] < V[1])
solver.add(V[0] < V[2])

# Condition 3: Solide's website < Truvest's website
solver.add(W[1] < W[2])

# Additional condition from Q: Truvest's website < Truvest's voicemail
solver.add(W[2] < V[2])

# Now define each option's constraint
# (A) Image's voicemail target is 2 days.
opt_a = (V[0] == 2)
# (B) Image's website target is 2 days.
opt_b = (W[0] == 2)
# (C) Image's website target is 1 day.
opt_c = (W[0] == 1)
# (D) Solide's website target is 2 days.
opt_d = (W[1] == 2)
# (E) Solide's website target is 1 day.
opt_e = (W[1] == 1)

# Check satisfiability of each option
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