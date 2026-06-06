from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define cargo types as integers for clarity
fuel = 0
GRAIN = 1
LIVESTOCK = 2
MACHINERY = 3
PRODUCE = 4
TEXTILES = 5

# Create a solver
solver = Solver()

# Declare variables for cargo in each bay (1-6)
# bay[i] = cargo type in bay i (0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles)
bay = [Int(f'bay_{i+1}') for i in range(6)]

# Each bay must have a distinct cargo type
solver.add(Distinct(bay))

# Constraints from the problem statement
# 1. The bay holding grain has a higher number than the bay holding livestock
# 2. The bay holding livestock has a higher number than the bay holding textiles
# 3. The bay holding produce has a higher number than the bay holding fuel
# 4. The bay holding textiles is next to the bay holding produce

# To express "higher number", we need to find the bay indices for each cargo type
# Let's define variables for the bay indices of each cargo type
bay_of = {cargo: Int(f'bay_of_{cargo}') for cargo in [fuel, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]}

# Link bay indices to cargo assignments
for i in range(6):
    for cargo in [fuel, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]:
        solver.add(Implies(bay[i] == cargo, bay_of[cargo] == i+1))

# Constraint 1: Grain bay > Livestock bay
solver.add(bay_of[GRAIN] > bay_of[LIVESTOCK])

# Constraint 2: Livestock bay > Textiles bay
solver.add(bay_of[LIVESTOCK] > bay_of[TEXTILES])

# Constraint 3: Produce bay > Fuel bay
solver.add(bay_of[PRODUCE] > bay_of[fuel])

# Constraint 4: Textiles bay is next to Produce bay
solver.add(Or(
    bay_of[TEXTILES] == bay_of[PRODUCE] + 1,
    bay_of[TEXTILES] == bay_of[PRODUCE] - 1
))

# Base constraints are now set. Now evaluate each multiple-choice option.
# Each option specifies cargo for bays 1, 2, 3 (in order).
# We need to check if the option is consistent with the constraints.

# Define the options as constraints on bays 1, 2, 3
options = {
    "A": [fuel, MACHINERY, TEXTILES],
    "B": [GRAIN, MACHINERY, fuel],
    "C": [MACHINERY, LIVESTOCK, fuel],
    "D": [MACHINERY, TEXTILES, fuel],
    "E": [MACHINERY, TEXTILES, PRODUCE]
}

found_options = []

for letter, cargo_list in options.items():
    solver.push()
    # Constrain bays 1, 2, 3 to the cargo in the option
    for i in range(3):
        solver.add(bay[i] == cargo_list[i])
    
    # Check if the constraints are satisfiable
    if solver.check() == sat:
        found_options.append(letter)
    
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")