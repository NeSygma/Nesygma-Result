from z3 import *

solver = Solver()

# Bays 1 through 6
# Each bay holds a different cargo type
# We'll use Int variables for each cargo type, representing the bay number they're in
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo is in a bay 1-6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different
solver.add(Distinct(cargos))

# Constraints:
# 1. grain > livestock
solver.add(grain > livestock)

# 2. livestock > textiles
solver.add(livestock > textiles)

# 3. produce > fuel
solver.add(produce > fuel)

# 4. textiles is next to produce (|textiles - produce| == 1)
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Additional condition: produce is next to livestock
solver.add(Or(produce == livestock + 1, produce == livestock - 1))

# Now evaluate each option
# Option A: Bay 2 is holding fuel
opt_a = (fuel == 2)

# Option B: Bay 4 is holding produce
opt_b = (produce == 4)

# Option C: Bay 4 is holding textiles
opt_c = (textiles == 4)

# Option D: Bay 5 is holding grain
opt_d = (grain == 5)

# Option E: Bay 5 is holding machinery
opt_e = (machinery == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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