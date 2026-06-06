from z3 import *

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create boolean variables: student_reviews_play[student][play]
student_reviews = {}
for student in students:
    student_reviews[student] = {}
    for play in plays:
        student_reviews[student][play] = Bool(f"{student}_{play}")

# Create integer variables for number of plays each student reviews
num_plays = {student: Int(f"num_{student}") for student in students}

solver = Solver()

# Constraint 1: Each student reviews at least one play
for student in students:
    solver.add(Sum([If(student_reviews[student][play], 1, 0) for play in plays]) >= 1)

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
# First, compute the number of plays each student reviews
for student in students:
    solver.add(num_plays[student] == Sum([If(student_reviews[student][play], 1, 0) for play in plays]))

solver.add(num_plays["Kramer"] < num_plays["Megregian"])
solver.add(num_plays["Lopez"] < num_plays["Megregian"])

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for play in plays:
    solver.add(Or(
        Not(student_reviews["Lopez"][play]),
        Not(student_reviews["Jiang"][play])
    ))
    solver.add(Or(
        Not(student_reviews["Megregian"][play]),
        Not(student_reviews["Jiang"][play])
    ))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(student_reviews["Kramer"]["Tamerlane"])
solver.add(student_reviews["O'Neill"]["Tamerlane"])

# Constraint 5: Exactly two students review exactly the same set of plays
# We need to count how many pairs of students have identical play sets
same_set_pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        s1, s2 = students[i], students[j]
        # They have the same set if for all plays, they both review or both don't review
        same_set = And([student_reviews[s1][play] == student_reviews[s2][play] for play in plays])
        same_set_pairs.append(same_set)

# Exactly one pair should be true (exactly two students have same set)
solver.add(Sum([If(pair, 1, 0) for pair in same_set_pairs]) == 1)

# Now, let's define what it means for a student to review ONLY Sunset
def reviews_only_sunset(student):
    return And(
        student_reviews[student]["Sunset"],
        Not(student_reviews[student]["Tamerlane"]),
        Not(student_reviews[student]["Undulation"])
    )

# Now test each answer choice
options = {
    "A": ["Lopez"],
    "B": ["O'Neill"],
    "C": ["Jiang", "Lopez"],
    "D": ["Kramer", "O'Neill"],
    "E": ["Lopez", "Megregian"]
}

found_options = []
for letter, students_in_option in options.items():
    solver.push()
    
    # Add constraint: exactly these students review ONLY Sunset
    # First, students in the option must review ONLY Sunset
    for student in students_in_option:
        solver.add(reviews_only_sunset(student))
    
    # Second, students NOT in the option must NOT review ONLY Sunset
    for student in students:
        if student not in students_in_option:
            solver.add(Not(reviews_only_sunset(student)))
    
    # Check if this is satisfiable
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