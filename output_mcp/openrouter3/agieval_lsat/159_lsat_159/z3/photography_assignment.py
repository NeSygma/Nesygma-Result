from z3 import *

# Create solver
solver = Solver()

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Variables: assigned_to_silva[i] = True if photographer i is assigned to Silva
# assigned_to_thorne[i] = True if photographer i is assigned to Thorne
# Note: A photographer can be assigned to neither ceremony (not assigned)
assigned_to_silva = [Bool(f"s_{i}") for i in range(6)]
assigned_to_thorne = [Bool(f"t_{i}") for i in range(6)]

# Constraint: No photographer can be assigned to both ceremonies
for i in range(6):
    solver.add(Or(Not(assigned_to_silva[i]), Not(assigned_to_thorne[i])))

# Constraint: Exactly 4 photographers are assigned
total_assigned = Sum([If(Or(assigned_to_silva[i], assigned_to_thorne[i]), 1, 0) for i in range(6)])
solver.add(total_assigned == 4)

# Constraint: Each ceremony must have at least 2 photographers
silva_count = Sum([If(assigned_to_silva[i], 1, 0) for i in range(6)])
thorne_count = Sum([If(assigned_to_thorne[i], 1, 0) for i in range(6)])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
# This means: Frost and Heideck are both assigned to the same ceremony (either Silva or Thorne)
solver.add(Or(
    And(assigned_to_silva[0], assigned_to_silva[2]),  # Both to Silva
    And(assigned_to_thorne[0], assigned_to_thorne[2])  # Both to Thorne
))

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
# Lai is index 4, Mays is index 5
solver.add(Implies(
    And(Or(assigned_to_silva[4], assigned_to_thorne[4]), Or(assigned_to_silva[5], assigned_to_thorne[5])),
    Or(
        And(assigned_to_silva[4], assigned_to_thorne[5]),
        And(assigned_to_thorne[4], assigned_to_silva[5])
    )
))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
# Gonzalez is index 1, Lai is index 4
solver.add(Implies(
    assigned_to_silva[1],
    assigned_to_thorne[4]
))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
# Knutson is index 3, Heideck is index 2, Mays is index 5
solver.add(Implies(
    Not(assigned_to_thorne[3]),
    And(assigned_to_thorne[2], assigned_to_thorne[5])
))

# Now test each answer choice
# We need to find which photographer MUST be assigned to Silva University
# This means: in every valid solution with exactly 4 photographers assigned,
# this photographer is always assigned to Silva

# For each option, we'll check if there exists a valid solution where that photographer is NOT assigned to Silva
# If no such solution exists, then that photographer MUST be assigned to Silva

found_options = []

# Option A: Frost must be assigned to Silva
# Check if there's a valid solution where Frost is NOT assigned to Silva
solver.push()
solver.add(Not(assigned_to_silva[0]))  # Frost not assigned to Silva
if solver.check() == sat:
    # There exists a solution where Frost is not assigned to Silva
    # So Frost is NOT mandatory for Silva
    pass
else:
    # No solution where Frost is not assigned to Silva
    # So Frost MUST be assigned to Silva
    found_options.append("A")
solver.pop()

# Option B: Gonzalez must be assigned to Silva
solver.push()
solver.add(Not(assigned_to_silva[1]))  # Gonzalez not assigned to Silva
if solver.check() == sat:
    pass
else:
    found_options.append("B")
solver.pop()

# Option C: Knutson must be assigned to Silva
solver.push()
solver.add(Not(assigned_to_silva[3]))  # Knutson not assigned to Silva
if solver.check() == sat:
    pass
else:
    found_options.append("C")
solver.pop()

# Option D: Lai must be assigned to Silva
solver.push()
solver.add(Not(assigned_to_silva[4]))  # Lai not assigned to Silva
if solver.check() == sat:
    pass
else:
    found_options.append("D")
solver.pop()

# Option E: Mays must be assigned to Silva
solver.push()
solver.add(Not(assigned_to_silva[5]))  # Mays not assigned to Silva
if solver.check() == sat:
    pass
else:
    found_options.append("E")
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")