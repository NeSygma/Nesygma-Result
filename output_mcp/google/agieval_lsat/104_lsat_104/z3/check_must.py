from z3 import *

# Define variables
IW, IV = Int('IW'), Int('IV')
SW, SV = Int('SW'), Int('SV')
TW, TV = Int('TW'), Int('TV')

# Base constraints
def get_base_solver():
    s = Solver()
    for v in [IW, IV, SW, SV, TW, TV]:
        s.add(v >= 1, v <= 3)
    s.add(IW <= IV)
    s.add(SW <= SV)
    s.add(TW <= TV)
    s.add(IV < SV)
    s.add(IV < TV)
    s.add(SW < TW)
    s.add(TW < TV)
    return s

# Check which options MUST be true
# A "must be true" option is one that is true in ALL valid models.
# Equivalently, the negation of the option is UNSAT.

options = {
    "A": IV == 2,
    "B": IW == 2,
    "C": IW == 1,
    "D": SW == 2,
    "E": SW == 1
}

for label, constr in options.items():
    s = get_base_solver()
    s.add(Not(constr))
    if s.check() == unsat:
        print(f"Option {label} MUST be true.")
    else:
        print(f"Option {label} is NOT necessarily true.")
        # print(s.model()) # Optional: see a counterexample