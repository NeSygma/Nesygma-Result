from z3 import *

solver = Solver()
# Variables for each target (days)
IW = Int('IW')   # Image website
IVo = Int('IVo') # Image voicemail
SW = Int('SW')   # Solide website
SVo = Int('SVo') # Solide voicemail
TW = Int('TW')   # Truvest website
TVo = Int('TVo') # Truvest voicemail

vars = [IW, IVo, SW, SVo, TW, TVo]
# Domain constraints: each target is 1,2,or3
for v in vars:
    solver.add(And(v >= 1, v <= 3))

# Base constraints
solver.add(IW <= IVo)   # website <= voicemail for Image
solver.add(SW <= SVo)   # for Solide
solver.add(TW <= TVo)   # for Truvest
solver.add(IVo < SVo)   # Image voicemail shorter than others
solver.add(IVo < TVo)
solver.add(SW < TW)     # Solide website shorter than Truvest website
solver.add(IW == 2)     # given condition

# For each option, test if it must be 2 (i.e., target !=2 leads to unsat)
options = [
    ("A", IVo),
    ("B", SW),
    ("C", SVo),
    ("D", TW),
    ("E", TVo)
]
forced = []
for letter, var in options:
    solver.push()
    solver.add(var != 2)
    if solver.check() == unsat:
        forced.append(letter)
    solver.pop()

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
elif len(forced) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")