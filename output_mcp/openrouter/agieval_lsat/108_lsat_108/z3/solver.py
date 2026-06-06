from z3 import *

# Declare variables
clients = ['Image', 'Solide', 'Truvest']
# website and voicemail targets for each client
website = {c: Int(f'web_{c}') for c in clients}
voicemail = {c: Int(f'vm_{c}') for c in clients}

solver = Solver()

# Domain constraints: each target in {1,2,3}
for c in clients:
    solver.add(And(website[c] >= 1, website[c] <= 3))
    solver.add(And(voicemail[c] >= 1, voicemail[c] <= 3))

# Base constraints
# 1. website <= voicemail for each client
for c in clients:
    solver.add(website[c] <= voicemail[c])

# 2. Image's voicemail shorter than other clients' voicemail
solver.add(voicemail['Image'] < voicemail['Solide'])
solver.add(voicemail['Image'] < voicemail['Truvest'])

# 3. Solide's website shorter than Truvest's website
solver.add(website['Solide'] < website['Truvest'])

# Additional condition: none of the clients has a website target of 2 days
for c in clients:
    solver.add(website[c] != 2)

# Define option constraints
opt_a = website['Image'] < website['Solide']
opt_b = website['Solide'] < website['Image']
opt_c = voicemail['Solide'] < voicemail['Truvest']
opt_d = website['Truvest'] < website['Image']
opt_e = voicemail['Truvest'] < voicemail['Solide']

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