from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for assignments
# We have two ceremonies: Silva University (1) and Thorne University (2)
# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
# Assignment status: 0=not assigned, 1=Silva, 2=Thorne

Frost = Int('Frost')
Gonzalez = Int('Gonzalez')
Heideck = Int('Heideck')
Knutson = Int('Knutson')
Lai = Int('Lai')
Mays = Int('Mays')

# Base constraints
solver = Solver()

# Each ceremony must have at least two photographers
# Count the number of photographers assigned to Silva (1) and Thorne (2)
silva_assigned = Sum([If(Frost == 1, 1, 0), 
                      If(Gonzalez == 1, 1, 0), 
                      If(Heideck == 1, 1, 0), 
                      If(Knutson == 1, 1, 0), 
                      If(Lai == 1, 1, 0), 
                      If(Mays == 1, 1, 0)])
thorne_assigned = Sum([If(Frost == 2, 1, 0), 
                        If(Gonzalez == 2, 1, 0), 
                        If(Heideck == 2, 1, 0), 
                        If(Knutson == 2, 1, 0), 
                        If(Lai == 2, 1, 0), 
                        If(Mays == 2, 1, 0)])

solver.add(silva_assigned >= 2)
solver.add(thorne_assigned >= 2)

# No photographer can be assigned to both ceremonies
# This is enforced by the Int representation (only one value per photographer)

# Frost must be assigned together with Heideck to one of the graduation ceremonies
# This means if Frost is assigned (1 or 2), Heideck must be assigned to the same ceremony
solver.add(Implies(Frost != 0, Frost == Heideck))

# If Lai and Mays are both assigned, it must be to different ceremonies
# If Lai != 0 and Mays != 0, then Lai != Mays
solver.add(Implies(And(Lai != 0, Mays != 0), Lai != Mays))

# If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony
# Gonzalez == 1 implies Lai == 2
solver.add(Implies(Gonzalez == 1, Lai == 2))

# If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it
# Knutson != 2 implies Heideck == 2 and Mays == 2
solver.add(Implies(Knutson != 2, And(Heideck == 2, Mays == 2)))

# Additional constraint: Heideck is assigned to the same graduation ceremony as Lai
# Heideck == Lai
solver.add(Heideck == Lai)

# Now, evaluate the multiple choice options
found_options = []

# Option A: Frost is assigned to the Thorne University ceremony
# Frost == 2
solver.push()
solver.add(Frost == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Gonzalez is assigned to the Silva University ceremony
# Gonzalez == 1
solver.push()
solver.add(Gonzalez == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Gonzalez is assigned to neither graduation ceremony
# Gonzalez == 0
solver.push()
solver.add(Gonzalez == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Knutson is assigned to the Thorne University ceremony
# Knutson == 2
solver.push()
solver.add(Knutson == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Lai is assigned to the Thorne University ceremony
# Lai == 2
solver.push()
solver.add(Lai == 2)
if solver.check() == sat:
    found_options.append("E")
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