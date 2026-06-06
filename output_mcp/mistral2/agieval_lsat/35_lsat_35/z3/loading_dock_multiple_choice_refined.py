from z3 import *

solver = Solver()

# Bays are numbered 1 to 6
bays = [Int(f'bay_{i}') for i in range(1, 7)]

# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
fuel, grain, livestock, machinery, produce, textiles = 0, 1, 2, 3, 4, 5

# Each bay holds a distinct cargo type
solver.add(Distinct(bays))

# Define variables for the bay numbers of each cargo type
bay_grain = Int('bay_grain')
bay_livestock = Int('bay_livestock')
bay_textiles = Int('bay_textiles')
bay_produce = Int('bay_produce')
bay_fuel = Int('bay_fuel')
bay_machinery = Int('bay_machinery')

# Each cargo type is assigned to exactly one bay
solver.add(Or([bay_grain == bay for bay in bays]))
solver.add(Or([bay_livestock == bay for bay in bays]))
solver.add(Or([bay_textiles == bay for bay in bays]))
solver.add(Or([bay_produce == bay for bay in bays]))
solver.add(Or([bay_fuel == bay for bay in bays]))
solver.add(Or([bay_machinery == bay for bay in bays]))

# All cargo types are in distinct bays
solver.add(Distinct([bay_grain, bay_livestock, bay_textiles, bay_produce, bay_fuel, bay_machinery]))

# Add the ordering constraints
solver.add(bay_grain > bay_livestock)
solver.add(bay_livestock > bay_textiles)
solver.add(bay_produce > bay_fuel)

# The bay holding textiles is next to the bay holding produce
solver.add(Or(bay_textiles == bay_produce - 1, bay_textiles == bay_produce + 1))

# The bay holding produce is next to the bay holding livestock
solver.add(Or(bay_produce == bay_livestock - 1, bay_produce == bay_livestock + 1))

# Now, let's evaluate the multiple choice options
# Option A: Bay 2 is holding fuel.
opt_a_constr = (bay_fuel == 2)

# Option B: Bay 4 is holding produce.
opt_b_constr = (bay_produce == 4)

# Option C: Bay 4 is holding textiles.
opt_c_constr = (bay_textiles == 4)

# Option D: Bay 5 is holding grain.
opt_d_constr = (bay_grain == 5)

# Option E: Bay 5 is holding machinery.
opt_e_constr = (bay_machinery == 5)

# Test each option
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