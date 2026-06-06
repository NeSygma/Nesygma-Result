from z3 import *

# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
photographer_vars = {p: Int(p) for p in photographers}

# Ceremonies: 0 = Silva, 1 = Thorne (or we can use separate boolean variables)
# Let's use Int variables where 0 = not assigned, 1 = Silva, 2 = Thorne
# Actually, better to use separate boolean variables for clarity
assigned_to_silva = {p: Bool(f"{p}_silva") for p in photographers}
assigned_to_thorne = {p: Bool(f"{p}_thorne") for p in photographers}

solver = Solver()

# Constraint 1: At least 2 photographers per ceremony
silva_count = Sum([If(assigned_to_silva[p], 1, 0) for p in photographers])
thorne_count = Sum([If(assigned_to_thorne[p], 1, 0) for p in photographers])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 2: No photographer assigned to both ceremonies
for p in photographers:
    solver.add(Or(Not(assigned_to_silva[p]), Not(assigned_to_thorne[p])))

# Constraint 3: Frost must be assigned together with Heideck to one ceremony
# They must be assigned to the same ceremony (both Silva or both Thorne)
solver.add(Or(
    And(assigned_to_silva["Frost"], assigned_to_silva["Heideck"]),
    And(assigned_to_thorne["Frost"], assigned_to_thorne["Heideck"])
))

# Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
# If both are assigned (to any ceremony), they cannot be at the same ceremony
solver.add(Implies(
    Or(assigned_to_silva["Lai"], assigned_to_thorne["Lai"]),
    Implies(
        Or(assigned_to_silva["Mays"], assigned_to_thorne["Mays"]),
        Or(
            And(assigned_to_silva["Lai"], assigned_to_thorne["Mays"]),
            And(assigned_to_thorne["Lai"], assigned_to_silva["Mays"])
        )
    )
))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(
    assigned_to_silva["Gonzalez"],
    assigned_to_thorne["Lai"]
))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(
    Not(assigned_to_thorne["Knutson"]),
    And(assigned_to_thorne["Heideck"], assigned_to_thorne["Mays"])
))

# Additional constraint: Each photographer can be assigned to at most one ceremony
# (Already covered by constraint 2, but let's be explicit)
for p in photographers:
    solver.add(Or(
        Not(assigned_to_silva[p]),
        Not(assigned_to_thorne[p])
    ))

# Now, we need to evaluate the question:
# "If Heideck is assigned to the same graduation ceremony as Lai, then which one of the following must be true?"
# This means we need to check: Under the condition that Heideck and Lai are at the same ceremony,
# which of the answer choices is ALWAYS true?

# First, let's add the condition: Heideck and Lai are at the same ceremony
same_ceremony_condition = Or(
    And(assigned_to_silva["Heideck"], assigned_to_silva["Lai"]),
    And(assigned_to_thorne["Heideck"], assigned_to_thorne["Lai"])
)

# Now, for each answer choice, we need to check if it MUST be true under the condition.
# That is, we need to check if the implication (condition => choice) is valid.
# In Z3, we can check this by seeing if the negation is unsatisfiable.

# Answer choices:
# (A) Frost is assigned to the Thorne University ceremony.
# (B) Gonzalez is assigned to the Silva University ceremony.
# (C) Gonzalez is assigned to neither graduation ceremony.
# (D) Knutson is assigned to the Thorne University ceremony.
# (E) Lai is assigned to the Thorne University ceremony.

# We'll test each choice by checking if the condition implies the choice.
# If the implication is valid (i.e., the negation is unsat), then the choice must be true.

found_options = []

# Test choice A: Frost is assigned to Thorne
solver.push()
solver.add(same_ceremony_condition)
solver.add(Not(assigned_to_thorne["Frost"]))  # Negation of choice A
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Test choice B: Gonzalez is assigned to Silva
solver.push()
solver.add(same_ceremony_condition)
solver.add(Not(assigned_to_silva["Gonzalez"]))  # Negation of choice B
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Test choice C: Gonzalez is assigned to neither ceremony
solver.push()
solver.add(same_ceremony_condition)
solver.add(Or(assigned_to_silva["Gonzalez"], assigned_to_thorne["Gonzalez"]))  # Negation of choice C
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Test choice D: Knutson is assigned to Thorne
solver.push()
solver.add(same_ceremony_condition)
solver.add(Not(assigned_to_thorne["Knutson"]))  # Negation of choice D
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Test choice E: Lai is assigned to Thorne
solver.push()
solver.add(same_ceremony_condition)
solver.add(Not(assigned_to_thorne["Lai"]))  # Negation of choice E
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

# Now, according to the requirement, we need exactly one option to be valid
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")