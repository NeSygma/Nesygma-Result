from z3 import *

# Photographers
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Create boolean variables for assignment to Silva and Thorne
silva = {p: Bool(f"silva_{p}") for p in photographers}
thorne = {p: Bool(f"thorne_{p}") for p in photographers}

solver = Solver()

# Constraint 1: No photographer is assigned to both ceremonies
for p in photographers:
    solver.add(Not(And(silva[p], thorne[p])))

# Constraint 2: Each ceremony has at least two photographers
solver.add(Sum([silva[p] for p in photographers]) >= 2)
solver.add(Sum([thorne[p] for p in photographers]) >= 2)

# Constraint 3: Frost must be assigned together with Heideck to one of the ceremonies
solver.add(Or(And(silva["Frost"], silva["Heideck"]), And(thorne["Frost"], thorne["Heideck"])))

# Constraint 4: If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Implies(And(silva["Lai"], silva["Mays"]), Not(thorne["Lai"]), Not(thorne["Mays"])))
solver.add(Implies(And(thorne["Lai"], thorne["Mays"]), Not(silva["Lai"]), Not(silva["Mays"])))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(silva["Gonzalez"], thorne["Lai"]))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(thorne["Knutson"]), And(thorne["Heideck"], thorne["Mays"])))

# Evaluate each option for Thorne University assignment
found_options = []

# Option A: Frost, Gonzalez, Heideck, Mays
solver.push()
# Set Thorne assignment to exactly these photographers
for p in photographers:
    if p in ["Frost", "Gonzalez", "Heideck", "Mays"]:
        solver.add(thorne[p] == True)
    else:
        solver.add(thorne[p] == False)

# Check if this assignment satisfies all constraints
if solver.check() == sat:
    found_options.append("A")
    print("Option A is SAT")
else:
    print("Option A is UNSAT")
solver.pop()

# Option B: Frost, Heideck, Knutson, Mays
solver.push()
# Set Thorne assignment to exactly these photographers
for p in photographers:
    if p in ["Frost", "Heideck", "Knutson", "Mays"]:
        solver.add(thorne[p] == True)
    else:
        solver.add(thorne[p] == False)

# Check if this assignment satisfies all constraints
if solver.check() == sat:
    found_options.append("B")
    print("Option B is SAT")
else:
    print("Option B is UNSAT")
solver.pop()

# Option C: Gonzalez, Knutson, Lai
solver.push()
# Set Thorne assignment to exactly these photographers
for p in photographers:
    if p in ["Gonzalez", "Knutson", "Lai"]:
        solver.add(thorne[p] == True)
    else:
        solver.add(thorne[p] == False)

# Check if this assignment satisfies all constraints
if solver.check() == sat:
    found_options.append("C")
    print("Option C is SAT")
else:
    print("Option C is UNSAT")
solver.pop()

# Option D: Gonzalez, Knutson, Mays
solver.push()
# Set Thorne assignment to exactly these photographers
for p in photographers:
    if p in ["Gonzalez", "Knutson", "Mays"]:
        solver.add(thorne[p] == True)
    else:
        solver.add(thorne[p] == False)

# Check if this assignment satisfies all constraints
if solver.check() == sat:
    found_options.append("D")
    print("Option D is SAT")
else:
    print("Option D is UNSAT")
solver.pop()

# Option E: Knutson, Mays
solver.push()
# Set Thorne assignment to exactly these photographers
for p in photographers:
    if p in ["Knutson", "Mays"]:
        solver.add(thorne[p] == True)
    else:
        solver.add(thorne[p] == False)

# Check if this assignment satisfies all constraints
if solver.check() == sat:
    found_options.append("E")
    print("Option E is SAT")
else:
    print("Option E is UNSAT")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")