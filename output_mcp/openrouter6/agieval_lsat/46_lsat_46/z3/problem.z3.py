from z3 import *

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create boolean variables: reviews[s][p] = True if student s reviews play p
reviews = {}
for s in students:
    reviews[s] = {}
    for p in plays:
        reviews[s][p] = Bool(f"{s}_{p}")

# Count of plays reviewed by each student
count = {}
for s in students:
    count[s] = Sum([If(reviews[s][p], 1, 0) for p in plays])

solver = Solver()

# Constraint: each student reviews at least one play
for s in students:
    solver.add(count[s] >= 1)

# Constraint 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(count["Kramer"] < count["Megregian"])
solver.add(count["Lopez"] < count["Megregian"])

# Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Lopez"][p])))
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Megregian"][p])))

# Constraint 3: Kramer and O'Neill both review Tamerlane
solver.add(reviews["Kramer"]["Tamerlane"] == True)
solver.add(reviews["O'Neill"]["Tamerlane"] == True)

# Constraint 4: Exactly two students have identical review sets
# Enumerate all pairs
pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        s1 = students[i]
        s2 = students[j]
        identical = And([reviews[s1][p] == reviews[s2][p] for p in plays])
        pairs.append(identical)

# Exactly one pair must be identical
solver.add(Sum([If(identical, 1, 0) for identical in pairs]) == 1)

# Now test each option for Tamerlane reviewers
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
    # Set Tamerlane reviewers: for each student, reviews[s]["Tamerlane"] must be True if in list, else False
    for s in students:
        if s in reviewers:
            solver.add(reviews[s]["Tamerlane"] == True)
        else:
            solver.add(reviews[s]["Tamerlane"] == False)
    if solver.check() == sat:
        found_options.append(letter)
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