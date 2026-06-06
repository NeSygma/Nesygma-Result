from z3 import *

solver = Solver()

# Countries and candidates
countries = ["Venezuela", "Yemen", "Zambia"]
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Assignments: country -> candidate
assignment = {c: Int(c) for c in countries}

# Each country is assigned a unique candidate
solver.add(Distinct(list(assignment.values())))

# Each candidate is assigned to at most one country (enforced by Distinct)

# Constraints:
# 1. Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
# This means exactly one of Kayne or Novetzke is assigned to a country.
kayne_assigned = Or([assignment[c] == "Kayne" for c in countries])
novetzke_assigned = Or([assignment[c] == "Novetzke" for c in countries])
solver.add(kayne_assigned != novetzke_assigned)

# 2. If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
jaramillo_assigned = Or([assignment[c] == "Jaramillo" for c in countries])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# 3. If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen.
ong_venezuela = (assignment["Venezuela"] == "Ong")
kayne_yemen = (assignment["Yemen"] == "Kayne")
solver.add(Not(And(ong_venezuela, kayne_yemen)))

# 4. If Landon is assigned to an ambassadorship, it is to Zambia.
landon_assigned = Or([assignment[c] == "Landon" for c in countries])
landon_zambia = (assignment["Zambia"] == "Landon")
solver.add(Implies(landon_assigned, landon_zambia))

# Base constraints for candidates: each assignment must be one of the candidates
for c in countries:
    solver.add(Or([assignment[c] == cand for cand in candidates]))

# Now evaluate each option to see which CANNOT be true
# We will check each option by adding its negation and seeing if the problem becomes unsat
# If adding the negation of an option makes the problem unsat, then the option MUST be true (so its negation cannot be true)
# If adding the negation of an option allows sat, then the option CAN be false (so its negation can be true)
# We are looking for the option that CANNOT be true, i.e., its negation is unsat

# Helper function to check if an option can be true
found_options = []

# Option A: Jaramillo is assigned as ambassador to Zambia.
# Negation: Jaramillo is NOT assigned to Zambia
solver.push()
solver.add(assignment["Zambia"] != "Jaramillo")
res_A = solver.check()
solver.pop()
if res_A == unsat:
    # The negation is unsat, so the original option MUST be true (so it CAN be true)
    found_options.append("A")

# Option B: Kayne is assigned as ambassador to Zambia.
# Negation: Kayne is NOT assigned to Zambia
solver.push()
solver.add(assignment["Zambia"] != "Kayne")
res_B = solver.check()
solver.pop()
if res_B == unsat:
    found_options.append("B")

# Option C: Novetzke is assigned as ambassador to Zambia.
# Negation: Novetzke is NOT assigned to Zambia
solver.push()
solver.add(assignment["Zambia"] != "Novetzke")
res_C = solver.check()
solver.pop()
if res_C == unsat:
    found_options.append("C")

# Option D: Landon is not assigned to an ambassadorship.
# Negation: Landon IS assigned to an ambassadorship
solver.push()
solver.add(Or([assignment[c] == "Landon" for c in countries]))
res_D = solver.check()
solver.pop()
if res_D == unsat:
    found_options.append("D")

# Option E: Ong is not assigned to an ambassadorship.
# Negation: Ong IS assigned to an ambassadorship
solver.push()
solver.add(Or([assignment[c] == "Ong" for c in countries]))
res_E = solver.check()
solver.pop()
if res_E == unsat:
    found_options.append("E")

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")