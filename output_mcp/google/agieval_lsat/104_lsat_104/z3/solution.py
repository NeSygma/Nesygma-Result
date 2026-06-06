from z3 import *

# Define variables
# Targets: 1, 2, 3
# Clients: I, S, T
# Channels: W, V
# Variables: IW, IV, SW, SV, TW, TV

IW, IV = Int('IW'), Int('IV')
SW, SV = Int('SW'), Int('SV')
TW, TV = Int('TW'), Int('TV')

solver = Solver()

# Domain constraints
for v in [IW, IV, SW, SV, TW, TV]:
    solver.add(v >= 1, v <= 3)

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
solver.add(IV < SV)
solver.add(IV < TV)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
solver.add(SW < TW)

# Question condition: Truvest's website target is shorter than its voicemail target.
solver.add(TW < TV)

# Options
options = [
    ("A", IV == 2),
    ("B", IW == 2),
    ("C", IW == 1),
    ("D", SW == 2),
    ("E", SW == 1)
]

# Check which option MUST be true
# An option O must be true if (Constraints AND NOT O) is UNSAT
must_be_true = []
for label, opt_constr in options:
    solver.push()
    solver.add(Not(opt_constr))
    if solver.check() == unsat:
        must_be_true.append(label)
    solver.pop()

print(f"Options that must be true: {must_be_true}")