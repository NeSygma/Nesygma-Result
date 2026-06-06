from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: Website (W), Voicemail (V)
# Values: 1, 2, 3

# Variables
IW, IV = Int('IW'), Int('IV')
SW, SV = Int('SW'), Int('SV')
TW, TV = Int('TW'), Int('TV')

solver = Solver()

# Domain constraints
for v in [IW, IV, SW, SV, TW, TV]:
    solver.add(v >= 1, v <= 3)

# Constraints
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)
solver.add(IV < SV)
solver.add(IV < TV)
solver.add(SW < TW)

# Condition: None of the clients has a voicemail target of 3 days
solver.add(IV != 3, SV != 3, TV != 3)

# Options
options = [
    ("A", IW == 1),
    ("B", SW == 2),
    ("C", SV == 2),
    ("D", TW == 2),
    ("E", TV == 2)
]

# We want to find which of these is NOT necessarily true.
# A statement is "must be true" if its negation is unsatisfiable.
# We are looking for the option that is NOT necessarily true,
# meaning there exists a valid model where the option is false.

results = []
for letter, constr in options:
    # Check if it's possible for the option to be false
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(constr))
    if s.check() == sat:
        results.append(letter)

print("STATUS: sat")
print(f"Options that are NOT necessarily true: {results}")