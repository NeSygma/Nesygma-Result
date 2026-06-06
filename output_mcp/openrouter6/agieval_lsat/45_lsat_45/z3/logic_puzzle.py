from z3 import *

# Students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create Boolean variables: reviewed[student][play]
reviewed = {}
for s in students:
    reviewed[s] = {}
    for p in plays:
        reviewed[s][p] = Bool(f"{s}_{p}")

solver = Solver()

# Constraint 1: Each student reviews at least one play
for s in students:
    solver.add(Or([reviewed[s][p] for p in plays]))

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
def count(student):
    return Sum([If(reviewed[student][p], 1, 0) for p in plays])

solver.add(count("Kramer") < count("Megregian"))
solver.add(count("Lopez") < count("Megregian"))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(reviewed["Jiang"][p], And(Not(reviewed["Lopez"][p]), Not(reviewed["Megregian"][p]))))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviewed["Kramer"]["Tamerlane"] == True)
solver.add(reviewed["O'Neill"]["Tamerlane"] == True)

# Constraint 5: Exactly two students have identical review sets
# Define same[i][j] for each unordered pair
pairs = []
same_vars = {}
for i in range(len(students)):
    for j in range(i+1, len(students)):
        s1 = students[i]
        s2 = students[j]
        same = Bool(f"same_{s1}_{s2}")
        same_vars[(s1, s2)] = same
        # same is true iff for all plays, reviewed[s1][p] == reviewed[s2][p]
        solver.add(same == And([reviewed[s1][p] == reviewed[s2][p] for p in plays]))
        pairs.append(same)

# Exactly one pair is identical
solver.add(Sum([If(same, 1, 0) for same in pairs]) == 1)

# Constraint 6: Exactly three students review Undulation
count_undulation = Sum([If(reviewed[s]["Undulation"], 1, 0) for s in students])
solver.add(count_undulation == 3)

# Now test each answer choice
options = [
    ("A", Not(reviewed["Megregian"]["Undulation"])),
    ("B", Not(reviewed["O'Neill"]["Undulation"])),
    ("C", reviewed["Jiang"]["Undulation"]),
    ("D", reviewed["Lopez"]["Tamerlane"]),
    ("E", reviewed["O'Neill"]["Sunset"])
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
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