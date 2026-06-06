from z3 import *

# Define variables
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

# Verify all options
for label, opt_constr in [("A", IV == 2), ("B", IW == 2), ("C", IW == 1), ("D", SW == 2), ("E", SW == 1)]:
    solver.push()
    solver.add(opt_constr)
    res = solver.check()
    print(f"Option {label} is {res}")
    if res == sat:
        print(solver.model())
    solver.pop()