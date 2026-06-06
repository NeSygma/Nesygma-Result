from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each photographer's assignment
# 0 = unassigned, 1 = assigned to Silva, 2 = assigned to Thorne
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
assign = {p: Int(f"assign_{p}") for p in photographers}

# Base constraints
solver = Solver()

# Each photographer is either unassigned (0), assigned to Silva (1), or assigned to Thorne (2)
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# Exactly four photographers are assigned (i.e., not unassigned)
total_assigned = Sum([If(assign[p] != 0, 1, 0) for p in photographers])
solver.add(total_assigned == 4)

# At least two photographers are assigned to each ceremony
silva_assigned = Sum([If(assign[p] == 1, 1, 0) for p in photographers])
thorne_assigned = Sum([If(assign[p] == 2, 1, 0) for p in photographers])
solver.add(silva_assigned >= 2)
solver.add(thorne_assigned >= 2)

# Frost must be assigned together with Heideck to one of the ceremonies
solver.add(Implies(assign["Frost"] != 0, assign["Heideck"] == assign["Frost"]))
solver.add(Implies(assign["Heideck"] != 0, assign["Frost"] == assign["Heideck"]))

# If Lai and Mays are both assigned, they must be assigned to different ceremonies
solver.add(Not(And(assign["Lai"] != 0, assign["Mays"] != 0, assign["Lai"] == assign["Mays"])))

# If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
solver.add(Implies(assign["Gonzalez"] == 1, assign["Lai"] == 2))

# If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to Thorne University
solver.add(Implies(assign["Knutson"] != 2, And(assign["Heideck"] == 2, assign["Mays"] == 2)))

# Now, evaluate each answer choice to see if it MUST be assigned to Silva University
# We will check if the negation of the option (i.e., not assigned to Silva) leads to unsat

must_be_options = []

# Option A: Frost must be assigned to Silva
# Check if Frost is NOT assigned to Silva leads to unsat
solver.push()
solver.add(assign["Frost"] != 1)  # Frost is NOT assigned to Silva
if solver.check() == unsat:
    must_be_options.append("A")
solver.pop()

# Option B: Gonzalez must be assigned to Silva
# Check if Gonzalez is NOT assigned to Silva leads to unsat
solver.push()
solver.add(assign["Gonzalez"] != 1)  # Gonzalez is NOT assigned to Silva
if solver.check() == unsat:
    must_be_options.append("B")
solver.pop()

# Option C: Knutson must be assigned to Silva
# Check if Knutson is NOT assigned to Silva leads to unsat
solver.push()
solver.add(assign["Knutson"] != 1)  # Knutson is NOT assigned to Silva
if solver.check() == unsat:
    must_be_options.append("C")
solver.pop()

# Option D: Lai must be assigned to Silva
# Check if Lai is NOT assigned to Silva leads to unsat
solver.push()
solver.add(assign["Lai"] != 1)  # Lai is NOT assigned to Silva
if solver.check() == unsat:
    must_be_options.append("D")
solver.pop()

# Option E: Mays must be assigned to Silva
# Check if Mays is NOT assigned to Silva leads to unsat
solver.push()
solver.add(assign["Mays"] != 1)  # Mays is NOT assigned to Silva
if solver.check() == unsat:
    must_be_options.append("E")
solver.pop()

# Output the result
if len(must_be_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_options[0]}")
elif len(must_be_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be {must_be_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be")