from z3 import *

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]
num_students = len(students)
num_plays = len(plays)

review = [[Bool(f"review_{i}_{j}") for j in range(num_plays)] for i in range(num_students)]

solver = Solver()

# Constraint 1: Each student reviews at least one play
for i in range(num_students):
    solver.add(Sum(review[i]) >= 1)

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
kramer_sum = Sum(review[1])
lopez_sum = Sum(review[2])
megregian_sum = Sum(review[3])
solver.add(kramer_sum < megregian_sum)
solver.add(lopez_sum < megregian_sum)

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(num_plays):
    solver.add(Implies(review[0][j], Not(review[2][j])))
    solver.add(Implies(review[0][j], Not(review[3][j])))

# Constraint 4: Kramer and O'Neill both review Tamerlane (play index 1)
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Constraint 5: Exactly two students have identical review sets
eq = {}
for i in range(num_students):
    for j in range(i+1, num_students):
        eq[(i,j)] = Bool(f"eq_{i}_{j}")
        solver.add(eq[(i,j)] == And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        ))
solver.add(Sum([eq[(i,j)] for i in range(num_students) for j in range(i+1, num_students)]) == 1)

# Check satisfiability
if solver.check() == sat:
    m = solver.model()
    print("Found a model:")
    for i in range(num_students):
        reviews = [plays[j] for j in range(num_plays) if is_true(m[review[i][j]])]
        print(f"{students[i]}: {reviews}")
    print()
    # Compute sums
    sums = [sum(1 for j in range(num_plays) if is_true(m[review[i][j]])) for i in range(num_students)]
    for i in range(num_students):
        print(f"{students[i]} reviews {sums[i]} plays")
    print()
    # Check which options hold
    print("Option A (Jiang > Lopez):", sums[0] > sums[2])
    print("Option B (Megregian > Jiang):", sums[3] > sums[0])
    print("Option C (Megregian > O'Neill):", sums[3] > sums[4])
    print("Option D (O'Neill > Jiang):", sums[4] > sums[0])
    print("Option E (O'Neill > Kramer):", sums[4] > sums[1])
else:
    print("No model found")