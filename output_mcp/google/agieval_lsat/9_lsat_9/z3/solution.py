from z3 import *

# Define variables for the number of works selected
# fn: French novels, rn: Russian novels, fp: French plays, rp: Russian plays
fn = Int('fn')
rn = Int('rn')
fp = Int('fp')
rp = Int('rp')

solver = Solver()

# Constraints
# Total works: 9 (3 FN, 3 RN, 2 FP, 1 RP)
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Selection size: 5 or 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than four French works
solver.add(fn + fp <= 4)

# At least three but no more than four novels
novels = fn + rn
solver.add(novels >= 3, novels <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Question: If fn = 3, which of the following could be the remaining works?
solver.add(fn == 3)

# Define options as constraints on (rn, fp, rp)
options = [
    ("A", rn == 1, fp == 0, rp == 0),
    ("B", rn == 0, fp == 2, rp == 0),
    ("C", rn == 1, fp == 0, rp == 1),
    ("D", rn == 1, fp == 2, rp == 0),
    ("E", rn == 2, fp == 1, rp == 0)
]

found_options = []
for letter, c_rn, c_fp, c_rp in options:
    solver.push()
    solver.add(c_rn, c_fp, c_rp)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"Valid options: {found_options}")
if len(found_options) == 1:
    print(f"answer:{found_options[0]}")