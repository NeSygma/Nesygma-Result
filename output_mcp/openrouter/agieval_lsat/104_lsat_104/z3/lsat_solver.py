from z3 import *

# Define variables for each client and channel
clients = ['Image', 'Solide', 'Truvest']
channels = ['website', 'voicemail']
# Create dict of Int variables
vars = {}
for c in clients:
    for ch in channels:
        vars[(c, ch)] = Int(f"{c}_{ch}")

solver = Solver()
# Domain constraints: each target is 1,2,or3
for v in vars.values():
    solver.add(And(v >= 1, v <= 3))

# Constraint 1: website <= voicemail for each client
for c in clients:
    solver.add(vars[(c, 'website')] <= vars[(c, 'voicemail')])

# Constraint 2: Image voicemail < other clients' voicemail
solver.add(vars[('Image','voicemail')] < vars[('Solide','voicemail')])
solver.add(vars[('Image','voicemail')] < vars[('Truvest','voicemail')])

# Constraint 3: Solide website < Truvest website
solver.add(vars[('Solide','website')] < vars[('Truvest','website')])

# Additional premise: Truvest website < Truvest voicemail
solver.add(vars[('Truvest','website')] < vars[('Truvest','voicemail')])

# Define option constraints
opt_a = vars[('Image','voicemail')] == 2
opt_b = vars[('Image','website')] == 2
opt_c = vars[('Image','website')] == 1
opt_d = vars[('Solide','website')] == 2
opt_e = vars[('Solide','website')] == 1

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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