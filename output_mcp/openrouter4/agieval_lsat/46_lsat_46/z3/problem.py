from z3 import *

solver = Solver()

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Using indices: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Plays: 0=Sunset, 1=Tamerlane, 2=Undulation

student_names = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]

# Binary variables: review[i][p] = 1 if student i reviews play p
review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

# Each student reviews at least one play
for i in range(5):
    solver.add(Or([review[i][p] for p in range(3)]))

# Count how many plays each student reviews
count = [Sum([If(review[i][p], 1, 0) for p in range(3)]) for i in range(5)]

# Kramer (1) and Lopez (2) each review fewer plays than Megregian (3)
solver.add(count[1] < count[3])
solver.add(count[2] < count[3])

# Neither Lopez (2) nor Megregian (3) reviews any play Jiang (0) reviews
# For each play: if Jiang reviews it, then Lopez doesn't and Megregian doesn't
for p in range(3):
    solver.add(Implies(review[0][p], Not(review[2][p])))
    solver.add(Implies(review[0][p], Not(review[3][p])))

# Kramer (1) and O'Neill (4) both review Tamerlane (p=1)
solver.add(review[1][1])
solver.add(review[4][1])

# Exactly two students review exactly the same set of plays.
# Count how many pairs of students have identical review sets.
identical_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        same = And([review[i][p] == review[j][p] for p in range(3)])
        identical_pairs.append(same)

# Exactly 1 pair of students share the same review set
solver.add(Sum([If(identical_pairs[k], 1, 0) for k in range(len(identical_pairs))]) == 1)

print("Base constraints added. Checking satisfiability...")

# Now check each option for who reviews Tamerlane
options = {
    "A": [0, 1],      # Jiang, Kramer
    "B": [1, 4],      # Kramer, O'Neill
    "C": [1, 2, 4],   # Kramer, Lopez, O'Neill
    "D": [1, 3, 4],   # Kramer, Megregian, O'Neill
    "E": [2, 3, 4]    # Lopez, Megregian, O'Neill
}

found_options = []

for letter, student_indices in options.items():
    solver.push()
    # The students listed review Tamerlane
    for i in student_indices:
        solver.add(review[i][1])
    # The students NOT listed do NOT review Tamerlane
    for i in range(5):
        if i not in student_indices:
            solver.add(Not(review[i][1]))
    
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        m = solver.model()
        # Print the model for verification
        for i in range(5):
            plays_reviewed = []
            for p in range(3):
                if is_true(m[review[i][p]]):
                    plays_reviewed.append(["S", "T", "U"][p])
            print("  " + student_names[i] + ": " + str(plays_reviewed))
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print("answer:" + found_options[0])
elif len(found_options) > 1:
    print("STATUS: unsat")
    print("Refine: Multiple options found " + str(found_options))
else:
    print("STATUS: unsat")
    print("Refine: No options found")