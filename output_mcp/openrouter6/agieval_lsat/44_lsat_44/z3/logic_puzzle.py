from z3 import *

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]
num_students = len(students)
num_plays = len(plays)

# Create Boolean variables: review[i][j] = True if student i reviews play j
review = [[Bool(f"review_{i}_{j}") for j in range(num_plays)] for i in range(num_students)]

solver = Solver()

# Constraint 1: Each student reviews at least one play
for i in range(num_students):
    solver.add(Sum(review[i]) >= 1)

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
kramer_sum = Sum(review[1])  # index 1: Kramer
lopez_sum = Sum(review[2])   # index 2: Lopez
megregian_sum = Sum(review[3])  # index 3: Megregian
solver.add(kramer_sum < megregian_sum)
solver.add(lopez_sum < megregian_sum)

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(num_plays):
    solver.add(Implies(review[0][j], Not(review[2][j])))  # Jiang -> not Lopez
    solver.add(Implies(review[0][j], Not(review[3][j])))  # Jiang -> not Megregian

# Constraint 4: Kramer and O'Neill both review Tamerlane (play index 1)
solver.add(review[1][1] == True)  # Kramer
solver.add(review[4][1] == True)  # O'Neill

# Constraint 5: Exactly two students have identical review sets
# Create equality variables for each pair
eq = {}
for i in range(num_students):
    for j in range(i+1, num_students):
        eq[(i,j)] = Bool(f"eq_{i}_{j}")
        # eq[(i,j)] is true iff all three plays are equal
        solver.add(eq[(i,j)] == And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        ))

# Sum of eq variables must be exactly 1
solver.add(Sum([eq[(i,j)] for i in range(num_students) for j in range(i+1, num_students)]) == 1)

# Now evaluate each answer choice
# Options:
# (A) Jiang reviews more plays than Lopez: sum(review[0]) > sum(review[2])
# (B) Megregian reviews more plays than Jiang: sum(review[3]) > sum(review[0])
# (C) Megregian reviews more plays than O'Neill: sum(review[3]) > sum(review[4])
# (D) O'Neill reviews more plays than Jiang: sum(review[4]) > sum(review[0])
# (E) O'Neill reviews more plays than Kramer: sum(review[4]) > sum(review[1])

found_options = []

# Option A
solver.push()
solver.add(Sum(review[0]) > Sum(review[2]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B
solver.push()
solver.add(Sum(review[3]) > Sum(review[0]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C
solver.push()
solver.add(Sum(review[3]) > Sum(review[4]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D
solver.push()
solver.add(Sum(review[4]) > Sum(review[0]))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E
solver.push()
solver.add(Sum(review[4]) > Sum(review[1]))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")