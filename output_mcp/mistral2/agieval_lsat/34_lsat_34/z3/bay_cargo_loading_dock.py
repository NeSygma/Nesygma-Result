from z3 import *

solver = Solver()

# Declare variables for each bay (1 to 6) and their cargo
# We represent the cargo in each bay as an Int, where the value corresponds to the cargo type:
# 0: fuel, 1: grain, 2: livestock, 3: machinery, 4: produce, 5: textiles

# Bay numbers are 1 to 6
bays = [Int(f'bay_{i+1}') for i in range(6)]

# Each bay must hold a distinct cargo type
solver.add(Distinct(bays))

# Helper function to constrain cargo types
fuel, grain, livestock, machinery, produce, textiles = 0, 1, 2, 3, 4, 5

# Add constraints based on the problem statement

# 1. The bay holding grain has a higher number than the bay holding livestock.
# This means the index of grain is greater than the index of livestock
solver.add(Or([
    And(bays[i] == grain, bays[j] == livestock, i > j) 
    for i in range(6) for j in range(6) if i != j
]))

# 2. The bay holding livestock has a higher number than the bay holding textiles.
# This means the index of livestock is greater than the index of textiles
solver.add(Or([
    And(bays[i] == livestock, bays[j] == textiles, i > j) 
    for i in range(6) for j in range(6) if i != j
]))

# 3. The bay holding produce has a higher number than the bay holding fuel.
# This means the index of produce is greater than the index of fuel
solver.add(Or([
    And(bays[i] == produce, bays[j] == fuel, i > j) 
    for i in range(6) for j in range(6) if i != j
]))

# 4. The bay holding textiles is next to the bay holding produce.
# This means the index of textiles is adjacent to the index of produce
solver.add(Or([
    And(bays[i] == textiles, Or(
        (i > 0 and bays[i-1] == produce),
        (i < 5 and bays[i+1] == produce)
    ))
    for i in range(6)
]))

# Base constraints for cargo types (0 to 5)
for i in range(6):
    solver.add(bays[i] >= 0, bays[i] <= 5)

# Now evaluate each option to see which one must be false
# We will check each option by adding its negation and seeing if the problem is still satisfiable
# If the problem is unsatisfiable with the negation, then the option must be true (so the original option must be false)
# If the problem is satisfiable with the negation, then the option could be false

found_options = []

# Option A: The bay holding fuel is next to the bay holding machinery.
# Negation: The bay holding fuel is NOT next to the bay holding machinery.
opt_a_constr = Not(Or([
    And(bays[i] == fuel, Or(
        (i > 0 and bays[i-1] == machinery),
        (i < 5 and bays[i+1] == machinery)
    ))
    for i in range(6)
]))

# Option B: The bay holding grain is next to the bay holding machinery.
# Negation: The bay holding grain is NOT next to the bay holding machinery.
opt_b_constr = Not(Or([
    And(bays[i] == grain, Or(
        (i > 0 and bays[i-1] == machinery),
        (i < 5 and bays[i+1] == machinery)
    ))
    for i in range(6)
]))

# Option C: The bay holding livestock is next to the bay holding fuel.
# Negation: The bay holding livestock is NOT next to the bay holding fuel.
opt_c_constr = Not(Or([
    And(bays[i] == livestock, Or(
        (i > 0 and bays[i-1] == fuel),
        (i < 5 and bays[i+1] == fuel)
    ))
    for i in range(6)
]))

# Option D: The bay holding produce is next to the bay holding livestock.
# Negation: The bay holding produce is NOT next to the bay holding livestock.
opt_d_constr = Not(Or([
    And(bays[i] == produce, Or(
        (i > 0 and bays[i-1] == livestock),
        (i < 5 and bays[i+1] == livestock)
    ))
    for i in range(6)
]))

# Option E: The bay holding textiles is next to the bay holding fuel.
# Negation: The bay holding textiles is NOT next to the bay holding fuel.
opt_e_constr = Not(Or([
    And(bays[i] == textiles, Or(
        (i > 0 and bays[i-1] == fuel),
        (i < 5 and bays[i+1] == fuel)
    ))
    for i in range(6)
]))

# Now check each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        # The negation of the option is unsatisfiable, so the option must be true
        # Therefore, the original option must be false
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