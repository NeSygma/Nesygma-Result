from z3 import *

solver = Solver()

# Variables: cargo type assigned to each bay (1-6)
# We'll use Int variables for each cargo type, representing which bay they're in
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]
cargo_names = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

# Each cargo is in a bay 1-6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different bays
solver.add(Distinct(cargos))

# Base constraints from problem:
# 1. grain > livestock
solver.add(grain > livestock)

# 2. livestock > textiles
solver.add(livestock > textiles)

# 3. produce > fuel
solver.add(produce > fuel)

# 4. textiles is next to produce (|textiles - produce| == 1)
solver.add(Abs(textiles - produce) == 1)

# Additional constraint from the question:
# "If the bay holding produce is next to the bay holding livestock"
# This is given as a condition, so we add it
solver.add(Abs(produce - livestock) == 1)

# Now evaluate each option
found_options = []

# Option A: Bay 2 is holding fuel
opt_a_constr = (fuel == 2)

# Option B: Bay 4 is holding produce
opt_b_constr = (produce == 4)

# Option C: Bay 4 is holding textiles
opt_c_constr = (textiles == 4)

# Option D: Bay 5 is holding grain
opt_d_constr = (grain == 5)

# Option E: Bay 5 is holding machinery
opt_e_constr = (machinery == 5)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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