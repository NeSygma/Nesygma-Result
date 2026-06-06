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

found_options = []
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