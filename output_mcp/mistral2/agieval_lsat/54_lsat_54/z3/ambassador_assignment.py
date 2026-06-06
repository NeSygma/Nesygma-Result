from z3 import *

solver = Solver()

# Declare symbolic variables for the assignments
# Countries: Venezuela, Yemen, Zambia
# Ambassadors: Jaramillo, Kayne, Landon, Novetzke, Ong

# We will model the assignment as a function from countries to ambassadors
# Since each ambassador can only be assigned to one country, we will also ensure uniqueness

countries = ["Venezuela", "Yemen", "Zambia"]
ambassadors = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Create a dictionary to map each country to an ambassador
assignment = {c: Const(c, StringSort()) for c in countries}

# Ensure each ambassador is assigned to at most one country
# We will enforce this by ensuring that the assignments are unique
solver.add(Distinct(list(assignment.values())))

# Helper function to check if an ambassador is assigned to any country
def is_assigned(amb):
    return Or([assignment[c] == amb for c in countries])

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
solver.add(Or(is_assigned("Kayne"), is_assigned("Novetzke")))
solver.add(Not(And(is_assigned("Kayne"), is_assigned("Novetzke"))))

# Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne
solver.add(Implies(is_assigned("Jaramillo"), is_assigned("Kayne")))

# Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
solver.add(Implies(assignment["Venezuela"] == "Ong", assignment["Yemen"] != "Kayne"))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia
solver.add(Implies(is_assigned("Landon"), assignment["Zambia"] == "Landon"))

# Now, evaluate each option
found_options = []

# Option A: Venezuela: Jaramillo, Yemen: Ong, Zambia: Novetzke
solver.push()
solver.add(assignment["Venezuela"] == "Jaramillo")
solver.add(assignment["Yemen"] == "Ong")
solver.add(assignment["Zambia"] == "Novetzke")
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Venezuela: Kayne, Yemen: Jaramillo, Zambia: Landon
solver.push()
solver.add(assignment["Venezuela"] == "Kayne")
solver.add(assignment["Yemen"] == "Jaramillo")
solver.add(assignment["Zambia"] == "Landon")
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Venezuela: Landon, Yemen: Novetzke, Zambia: Ong
solver.push()
solver.add(assignment["Venezuela"] == "Landon")
solver.add(assignment["Yemen"] == "Novetzke")
solver.add(assignment["Zambia"] == "Ong")
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Venezuela: Novetzke, Yemen: Jaramillo, Zambia: Kayne
solver.push()
solver.add(assignment["Venezuela"] == "Novetzke")
solver.add(assignment["Yemen"] == "Jaramillo")
solver.add(assignment["Zambia"] == "Kayne")
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Venezuela: Ong, Yemen: Kayne, Zambia: Landon
solver.push()
solver.add(assignment["Venezuela"] == "Ong")
solver.add(assignment["Yemen"] == "Kayne")
solver.add(assignment["Zambia"] == "Landon")
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