from z3 import *

# Students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create Boolean variables: student_reviews_play[student][play]
student_reviews = {}
for student in students:
    student_reviews[student] = {}
    for play in plays:
        student_reviews[student][play] = Bool(f"{student}_{play}")

# Helper function to count plays reviewed by a student
def count_plays(student):
    return Sum([If(student_reviews[student][play], 1, 0) for play in plays])

# Create solver
solver = Solver()

# Constraint 1: Each student reviews at least one play
for student in students:
    solver.add(Or([student_reviews[student][play] for play in plays]))

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
kramer_count = count_plays("Kramer")
lopez_count = count_plays("Lopez")
megregian_count = count_plays("Megregian")
solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for play in plays:
    solver.add(Not(And(student_reviews["Lopez"][play], student_reviews["Jiang"][play])))
    solver.add(Not(And(student_reviews["Megregian"][play], student_reviews["Jiang"][play])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(student_reviews["Kramer"]["Tamerlane"])
solver.add(student_reviews["O'Neill"]["Tamerlane"])

# Constraint 5: Exactly two students review exactly the same set of plays
# We need to check all pairs of students
def same_set(s1, s2):
    return And([student_reviews[s1][play] == student_reviews[s2][play] for play in plays])

# Exactly one pair must have the same set
pair_constraints = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        pair_constraints.append(same_set(students[i], students[j]))

# Exactly one pair should be true
solver.add(Sum([If(pc, 1, 0) for pc in pair_constraints]) == 1)

# Now evaluate each answer choice
# Answer choices are about comparing number of plays reviewed
# We need to check which one MUST be true (true in all satisfying models)

# For each answer choice, we'll check if it's possible to be false
# If it's impossible to be false, then it must be true

# (A) Jiang reviews more plays than Lopez
opt_a = count_plays("Jiang") > count_plays("Lopez")

# (B) Megregian reviews more plays than Jiang
opt_b = count_plays("Megregian") > count_plays("Jiang")

# (C) Megregian reviews more plays than O'Neill
opt_c = count_plays("Megregian") > count_plays("O'Neill")

# (D) O'Neill reviews more plays than Jiang
opt_d = count_plays("O'Neill") > count_plays("Jiang")

# (E) O'Neill reviews more plays than Kramer
opt_e = count_plays("O'Neill") > count_plays("Kramer")

# Check which options must be true
# For each option, check if its negation is satisfiable
# If negation is unsatisfiable, then the option must be true

found_options = []

# Check option A
solver.push()
solver.add(Not(opt_a))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Check option B
solver.push()
solver.add(Not(opt_b))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Check option C
solver.push()
solver.add(Not(opt_c))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Check option D
solver.push()
solver.add(Not(opt_d))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Check option E
solver.push()
solver.add(Not(opt_e))
if solver.check() == unsat:
    found_options.append("E")
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