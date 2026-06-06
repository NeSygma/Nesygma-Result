from z3 import *

solver = Solver()

# Countries and candidates
countries = ["Venezuela", "Yemen", "Zambia"]
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Map candidates to indices for easier handling
candidate_to_idx = {candidate: idx for idx, candidate in enumerate(candidates)}

# Assignments: country -> candidate index (0 to 4)
# We use Int variables for each country's assignment
assignments = [Int(f"assign_{country}") for country in countries]

# Each country is assigned exactly one candidate
for i, country in enumerate(countries):
    solver.add(assignments[i] >= 0, assignments[i] < len(candidates))

# No candidate is assigned to more than one country
solver.add(Distinct(assignments))

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
# This means exactly one of Kayne or Novetzke is assigned to any of the three countries.
# Kayne is candidate_to_idx["Kayne"], Novetzke is candidate_to_idx["Novetzke"]
for i in range(len(countries)):
    for j in range(i + 1, len(countries)):
        # Ensure that Kayne and Novetzke are not both assigned
        solver.add(Not(And(
            assignments[i] == candidate_to_idx["Kayne"],
            assignments[j] == candidate_to_idx["Novetzke"]
        )))
        solver.add(Not(And(
            assignments[i] == candidate_to_idx["Novetzke"],
            assignments[j] == candidate_to_idx["Kayne"]
        )))

# At least one of Kayne or Novetzke must be assigned
solver.add(Or(
    Or([assignments[i] == candidate_to_idx["Kayne"] for i in range(len(countries))]),
    Or([assignments[i] == candidate_to_idx["Novetzke"] for i in range(len(countries))])
))

# Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
# Jaramillo is candidate_to_idx["Jaramillo"]
solver.add(Implies(
    Or([assignments[i] == candidate_to_idx["Jaramillo"] for i in range(len(countries))]),
    Or([assignments[i] == candidate_to_idx["Kayne"] for i in range(len(countries))])
))

# Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen.
# Ong is candidate_to_idx["Ong"], Venezuela is 0, Yemen is 1
solver.add(Implies(
    assignments[0] == candidate_to_idx["Ong"],
    assignments[1] != candidate_to_idx["Kayne"]
))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia.
# Landon is candidate_to_idx["Landon"], Zambia is 2
solver.add(Implies(
    Or([assignments[i] == candidate_to_idx["Landon"] for i in range(len(countries))]),
    assignments[2] == candidate_to_idx["Landon"]
))

# Base constraint: Ong is assigned to Venezuela (as per the question)
solver.add(assignments[0] == candidate_to_idx["Ong"])

# Now evaluate the multiple choice options
found_options = []

# Option A: Jaramillo and Landon
solver.push()
# Jaramillo and Landon are assigned to Yemen and Zambia (in any order)
solver.add(Or(
    And(assignments[1] == candidate_to_idx["Jaramillo"], assignments[2] == candidate_to_idx["Landon"]),
    And(assignments[1] == candidate_to_idx["Landon"], assignments[2] == candidate_to_idx["Jaramillo"])
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Jaramillo and Novetzke
solver.push()
# Jaramillo and Novetzke are assigned to Yemen and Zambia (in any order)
solver.add(Or(
    And(assignments[1] == candidate_to_idx["Jaramillo"], assignments[2] == candidate_to_idx["Novetzke"]),
    And(assignments[1] == candidate_to_idx["Novetzke"], assignments[2] == candidate_to_idx["Jaramillo"])
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Kayne and Landon
solver.push()
# Kayne and Landon are assigned to Yemen and Zambia (in any order)
solver.add(Or(
    And(assignments[1] == candidate_to_idx["Kayne"], assignments[2] == candidate_to_idx["Landon"]),
    And(assignments[1] == candidate_to_idx["Landon"], assignments[2] == candidate_to_idx["Kayne"])
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kayne and Novetzke
solver.push()
# Kayne and Novetzke are assigned to Yemen and Zambia (in any order)
solver.add(Or(
    And(assignments[1] == candidate_to_idx["Kayne"], assignments[2] == candidate_to_idx["Novetzke"]),
    And(assignments[1] == candidate_to_idx["Novetzke"], assignments[2] == candidate_to_idx["Kayne"])
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Landon and Novetzke
solver.push()
# Landon and Novetzke are assigned to Yemen and Zambia (in any order)
solver.add(Or(
    And(assignments[1] == candidate_to_idx["Landon"], assignments[2] == candidate_to_idx["Novetzke"]),
    And(assignments[1] == candidate_to_idx["Novetzke"], assignments[2] == candidate_to_idx["Landon"])
))
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