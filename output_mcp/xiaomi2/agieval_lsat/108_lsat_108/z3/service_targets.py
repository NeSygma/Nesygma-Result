from z3 import *

solver = Solver()

# Clients: Image (0), Solide (1), Truvest (2)
# Channels: Website (W), Voicemail (V)
# Targets: 1, 2, or 3 days

W = [Int(f'W_{c}') for c in ['Image', 'Solide', 'Truvest']]
V = [Int(f'V_{c}') for c in ['Image', 'Solide', 'Truvest']]

# Domain: targets are 1, 2, or 3
for i in range(3):
    solver.add(And(W[i] >= 1, W[i] <= 3))
    solver.add(And(V[i] >= 1, V[i] <= 3))

# Constraint 1: Website target <= Voicemail target for each client
for i in range(3):
    solver.add(W[i] <= V[i])

# Constraint 2: Image's voicemail < Solide's voicemail AND Image's voicemail < Truvest's voicemail
solver.add(V[0] < V[1])
solver.add(V[0] < V[2])

# Constraint 3: Solide's website < Truvest's website
solver.add(W[1] < W[2])

# Additional constraint: None of the clients has a website target of 2 days
for i in range(3):
    solver.add(W[i] != 2)

# Now evaluate each answer choice
# (A) Image's website target is shorter than Solide's
opt_a = W[0] < W[1]
# (B) Solide's website target is shorter than Image's
opt_b = W[1] < W[0]
# (C) Solide's voicemail target is shorter than Truvest's
opt_c = V[1] < V[2]
# (D) Truvest's website target is shorter than Image's
opt_d = W[2] < W[0]
# (E) Truvest's voicemail target is shorter than Solide's
opt_e = V[2] < V[1]

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: W={[m[W[i]] for i in range(3)]}, V={[m[V[i]] for i in range(3)]}")
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