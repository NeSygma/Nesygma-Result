from z3 import *

# Clients
clients = ['I', 'S', 'T']
# Targets: Website (W) and Voicemail (V)
# I_W, I_V, S_W, S_V, T_W, T_V
targets = {
    'I_W': Int('I_W'), 'I_V': Int('I_V'),
    'S_W': Int('S_W'), 'S_V': Int('S_V'),
    'T_W': Int('T_W'), 'T_V': Int('T_V')
}

solver = Solver()

# Domain: 1, 2, 3
for t in targets.values():
    solver.add(t >= 1, t <= 3)

# Constraints
# 1. None of the clients can have a website target that is longer than its voicemail target.
solver.add(targets['I_W'] <= targets['I_V'])
solver.add(targets['S_W'] <= targets['S_V'])
solver.add(targets['T_W'] <= targets['T_V'])

# 2. Image's voicemail target must be shorter than the other clients' voicemail targets.
solver.add(targets['I_V'] < targets['S_V'])
solver.add(targets['I_V'] < targets['T_V'])

# 3. Solide's website target must be shorter than Truvest's website target.
solver.add(targets['S_W'] < targets['T_W'])

# Given: Image's website target is 2 days
solver.add(targets['I_W'] == 2)

# Options to test
options = [
    ("A", targets['I_V'] == 2),
    ("B", targets['S_W'] == 2),
    ("C", targets['S_V'] == 2),
    ("D", targets['T_W'] == 2),
    ("E", targets['T_V'] == 2)
]

# We want to find which option MUST be 2.
# An option MUST be 2 if it is true in ALL valid models.
# Equivalently, it is NOT 2 if there exists a valid model where it is NOT 2.

found_options = []
for letter, constr in options:
    # Check if it's possible for the option to NOT be 2
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # If it's impossible for it to NOT be 2, then it MUST be 2.
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