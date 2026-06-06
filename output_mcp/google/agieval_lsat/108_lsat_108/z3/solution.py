from z3 import *

# Clients
clients = ['I', 'S', 'T']
# Targets: W (website), V (voicemail)
# Domain: 1, 2, 3
targets = {c: {'W': Int(f'{c}_W'), 'V': Int(f'{c}_V')} for c in clients}

solver = Solver()

# Domain constraints
for c in clients:
    solver.add(targets[c]['W'] >= 1, targets[c]['W'] <= 3)
    solver.add(targets[c]['V'] >= 1, targets[c]['V'] <= 3)

# 1. None of the clients can have a website target that is longer than its voicemail target.
for c in clients:
    solver.add(targets[c]['W'] <= targets[c]['V'])

# 2. Image's voicemail target must be shorter than the other clients' voicemail targets.
solver.add(targets['I']['V'] < targets['S']['V'])
solver.add(targets['I']['V'] < targets['T']['V'])

# 3. Solide's website target must be shorter than Truvest's website target.
solver.add(targets['S']['W'] < targets['T']['W'])

# 4. If none of the clients has a website target of 2 days
for c in clients:
    solver.add(targets[c]['W'] != 2)

# Options
options = [
    ("A", targets['I']['W'] < targets['S']['W']),
    ("B", targets['S']['W'] < targets['I']['W']),
    ("C", targets['S']['V'] < targets['T']['V']),
    ("D", targets['T']['W'] < targets['I']['W']),
    ("E", targets['T']['V'] < targets['S']['V'])
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