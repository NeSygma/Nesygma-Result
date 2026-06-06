from z3 import *

# Students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Boolean variables: student_reviews_play[student][play]
student_reviews = {}
for s in students:
    student_reviews[s] = {}
    for p in plays:
        student_reviews[s][p] = Bool(f"{s}_{p}")

# Helper function to get list of plays reviewed by a student
def plays_reviewed(student):
    return [student_reviews[student][p] for p in plays]

# Helper function to count plays reviewed by a student
def count_plays(student):
    return Sum([If(student_reviews[student][p], 1, 0) for p in plays])

# Base constraints
solver = Solver()

# 1. Each student reviews at least one play
for s in students:
    solver.add(Sum([If(student_reviews[s][p], 1, 0) for p in plays]) >= 1)

# 2. Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays("Kramer") < count_plays("Megregian"))
solver.add(count_plays("Lopez") < count_plays("Megregian"))

# 3. Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Or(Not(student_reviews["Lopez"][p]), Not(student_reviews["Jiang"][p])))
    solver.add(Or(Not(student_reviews["Megregian"][p]), Not(student_reviews["Jiang"][p])))

# 4. Kramer and O'Neill both review Tamerlane
solver.add(student_reviews["Kramer"]["Tamerlane"])
solver.add(student_reviews["O'Neill"]["Tamerlane"])

# 5. Exactly two students review exactly the same set of plays
# We need to check all pairs of students
def same_set(s1, s2):
    # Returns True if s1 and s2 review exactly the same plays
    return And([student_reviews[s1][p] == student_reviews[s2][p] for p in plays])

# Exactly one pair has same set, and no other pair has same set
# We'll use a more direct approach: count how many pairs have same set
pair_same = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        pair_same.append(same_set(students[i], students[j]))

# Exactly one pair should be true
solver.add(Sum([If(p, 1, 0) for p in pair_same]) == 1)

# 6. Exactly three students review Undulation
solver.add(Sum([If(student_reviews[s]["Undulation"], 1, 0) for s in students]) == 3)

# Now test each option
# Option A: Megregian does not review Undulation
opt_a = Not(student_reviews["Megregian"]["Undulation"])

# Option B: O'Neill does not review Undulation
opt_b = Not(student_reviews["O'Neill"]["Undulation"])

# Option C: Jiang reviews Undulation
opt_c = student_reviews["Jiang"]["Undulation"]

# Option D: Lopez reviews Tamerlane
opt_d = student_reviews["Lopez"]["Tamerlane"]

# Option E: O'Neill reviews Sunset
opt_e = student_reviews["O'Neill"]["Sunset"]

# Test each option using the exact skeleton
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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