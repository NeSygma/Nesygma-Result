from z3 import *

solver = Solver()

# Bays 1 through 6, each holds a different cargo type
# We'll use Int variables for each cargo type, representing the bay number (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo is in a distinct bay 1-6
for c in cargos:
    solver.add(c >= 1, c <= 6)
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

# Now test each option: "CANNOT be the type of cargo held in bay 4"
# We test: is it possible for bay 4 to hold this cargo?
# If sat, it's possible (so it CAN be). If unsat, it's impossible (CANNOT be).

found_options = []

# Option A: grain in bay 4
opt_a = (grain == 4)
# Option B: livestock in bay 4
opt_b = (livestock == 4)
# Option C: machinery in bay 4
opt_c = (machinery == 4)
# Option D: produce in bay 4
opt_d = (produce == 4)
# Option E: textiles in bay 4
opt_e = (textiles == 4)

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