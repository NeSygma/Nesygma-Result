from z3 import *

# Create solver
solver = Solver()

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create boolean variables: student_reviews_play[student][play]
# Using a dictionary of dictionaries for clarity
reviews = {}
for student in students:
    reviews[student] = {}
    for play in plays:
        reviews[student][play] = Bool(f"{student}_{play}")

# Constraint 1: Each student reviews one or more plays
for student in students:
    solver.add(Or([reviews[student][play] for play in plays]))

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
# Count plays reviewed by each student
kramer_count = Sum([If(reviews["Kramer"][play], 1, 0) for play in plays])
lopez_count = Sum([If(reviews["Lopez"][play], 1, 0) for play in plays])
megregian_count = Sum([If(reviews["Megregian"][play], 1, 0) for play in plays])

solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for play in plays:
    solver.add(Implies(reviews["Jiang"][play], Not(reviews["Lopez"][play])))
    solver.add(Implies(reviews["Jiang"][play], Not(reviews["Megregian"][play])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews["Kramer"]["Tamerlane"])
solver.add(reviews["O'Neill"]["Tamerlane"])

# Constraint 5: Exactly two of the students review exactly the same play or plays as each other
# This means there is exactly one pair of students with identical review sets
# We need to check all possible pairs and ensure exactly one pair matches

# Create a function to check if two students have identical review sets
def identical_reviews(s1, s2):
    return And([reviews[s1][play] == reviews[s2][play] for play in plays])

# Create variables for each possible pair
pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        pairs.append((students[i], students[j], identical_reviews(students[i], students[j])))

# Exactly one pair should have identical reviews
pair_vars = [Bool(f"pair_{s1}_{s2}") for s1, s2, _ in pairs]
for i, (s1, s2, ident) in enumerate(pairs):
    solver.add(Implies(ident, pair_vars[i]))
    solver.add(Implies(Not(ident), Not(pair_vars[i])))

solver.add(Sum(pair_vars) == 1)

# Now test each answer choice
# Answer choices are about who reviews Tamerlane
# We need to check which option could be an accurate and complete list

# Define the options as constraints on who reviews Tamerlane
options = [
    ("A", ["Jiang", "Kramer"]),
    ("B", ["Kramer", "O'Neill"]),
    ("C", ["Kramer", "Lopez", "O'Neill"]),
    ("D", ["Kramer", "Megregian", "O'Neill"]),
    ("E", ["Lopez", "Megregian", "O'Neill"])
]

found_options = []
for letter, reviewers in options:
    solver.push()
    # Add constraint: exactly these students review Tamerlane
    # First, ensure all listed students review Tamerlane
    for student in reviewers:
        solver.add(reviews[student]["Tamerlane"])
    # Second, ensure no other student reviews Tamerlane
    for student in students:
        if student not in reviewers:
            solver.add(Not(reviews[student]["Tamerlane"]))
    
    if solver.check() == sat:
        found_options.append(letter)
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