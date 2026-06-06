from z3 import *

solver = Solver()

# Variables: each cargo type assigned to a bay number 1..6
fuel, grain, livestock, machinery, produce, textiles = Ints('fuel grain livestock machinery produce textiles')

# Each bay number is 1..6
cargos = [fuel, grain, livestock, machinery, produce, textiles]
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different
solver.add(Distinct(cargos))

# Constraints
# 1. grain > livestock
solver.add(grain > livestock)
# 2. livestock > textiles
solver.add(livestock > textiles)
# 3. produce > fuel
solver.add(produce > fuel)
# 4. textiles is next to produce
solver.add(Or(produce == textiles + 1, produce == textiles - 1))
# 5. ADDITIONAL: produce is next to livestock
solver.add(Or(produce == livestock + 1, produce == livestock - 1))

# Now evaluate each option
options = [
    ("A", fuel == 2, "Bay 2 is holding fuel"),
    ("B", produce == 4, "Bay 4 is holding produce"),
    ("C", textiles == 4, "Bay 4 is holding textiles"),
    ("D", grain == 5, "Bay 5 is holding grain"),
    ("E", machinery == 5, "Bay 5 is holding machinery"),
]

found_options = []
unsat_options = []

for letter, constr, desc in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    else:
        unsat_options.append(letter)
    solver.pop()

# The question asks "could be true EXCEPT" - the answer is the one that CANNOT be true
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) == 0:
    print("STATUS: unsat")
    print("Refine: All options can be true, no exception found")
else:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {unsat_options}")