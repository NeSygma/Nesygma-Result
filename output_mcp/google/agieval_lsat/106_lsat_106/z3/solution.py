from z3 import *

# Define variables
# Targets: 1, 2, 3
# Clients: Image (I), Solide (S), Truvest (T)
# Channels: Website (W), Voicemail (V)

IW, IV = Int('IW'), Int('IV')
SW, SV = Int('SW'), Int('SV')
TW, TV = Int('TW'), Int('TV')

solver = Solver()

# Domain constraints
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(var >= 1, var <= 3)

# General constraints
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)
solver.add(IV < SV)
solver.add(IV < TV)
solver.add(SW < TW)

# Conditional constraint
solver.add(SV < TW)

# Options to test
options = [
    ("A", IW == 2),
    ("B", IV == 2),
    ("C", SW == 2),
    ("D", TV == 2),
    ("E", TW == 2)
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