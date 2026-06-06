from z3 import *

# Declare Bool variables for each student-play pair
# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset, Tamerlane, Undulation

# Bool variables for each student's reviews
# Format: student_play
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O_Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create a dictionary to hold all Bool variables
review_vars = {}
for s in students:
    for p in plays:
        review_vars[f"{s}_{p}"] = Bool(f"{s}_{p}")

solver = Solver()

# Helper function to get the set of plays reviewed by a student
def get_reviews(student):
    return [review_vars[f"{student}_{p}"] for p in plays]

# Helper function to count the number of plays reviewed by a student
def count_reviews(student):
    return Sum([If(review_vars[f"{student}_{p}"], 1, 0) for p in plays])

# 1. Each student reviews at least one play
for s in students:
    solver.add(Or(get_reviews(s)))

# 2. Each student reviews at most three plays (implicit, since only three plays exist)

# 3. Kramer and Lopez each review fewer plays than Megregian
solver.add(count_reviews("Kramer") < count_reviews("Megregian"))
solver.add(count_reviews("Lopez") < count_reviews("Megregian"))

# 4. Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    # If Jiang reviews p, then Lopez and Megregian do not review p
    solver.add(Implies(review_vars[f"Jiang_{p}"], Not(review_vars[f"Lopez_{p}"])))
    solver.add(Implies(review_vars[f"Jiang_{p}"], Not(review_vars[f"Megregian_{p}"])))

# 5. Kramer and O'Neill both review Tamerlane
solver.add(review_vars["Kramer_Tamerlane"])
solver.add(review_vars["O_Neill_Tamerlane"])

# 6. Exactly two students review the same set of plays
# We need to count the number of students with the same review set
# To do this, we can group students by their review sets and ensure exactly one group has size 2

# Create a list of review sets for all students
review_sets = [get_reviews(s) for s in students]

# For each pair of students, check if their review sets are equal
# We will use a list to store the equality conditions
pairwise_equal = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        # Check if all review variables are equal
        equal = And([review_sets[i][k] == review_sets[j][k] for k in range(len(plays))])
        pairwise_equal.append(equal)

# Exactly one pair of students must have equal review sets
solver.add(Sum([If(e, 1, 0) for e in pairwise_equal]) == 1)

# 7. Jiang does not review Tamerlane
solver.add(Not(review_vars["Jiang_Tamerlane"]))

# Now, evaluate the multiple-choice options
# We will check each option to see if it must be true

# Define the options as constraints
# (A) Jiang reviews Sunset
opt_a_constr = review_vars["Jiang_Sunset"]

# (B) Lopez reviews Undulation
opt_b_constr = review_vars["Lopez_Undulation"]

# (C) Megregian reviews Sunset
opt_c_constr = review_vars["Megregian_Sunset"]

# (D) Megregian reviews Tamerlane
opt_d_constr = review_vars["Megregian_Tamerlane"]

# (E) O'Neill reviews Undulation
opt_e_constr = review_vars["O_Neill_Undulation"]

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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