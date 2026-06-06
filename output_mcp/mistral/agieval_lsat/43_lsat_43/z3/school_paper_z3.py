from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Define the plays as bit indices for clarity
# Sunset = 0, Tamerlane = 1, Undulation = 2
plays = [0, 1, 2]

# Define the students
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]

# For each student, create a list of 3 Booleans indicating which plays they review
# reviews[student][play] = True means the student reviews that play
reviews = {s: [Bool(f"{s}_reviews_{p}") for p in plays] for s in students}

# Helper: Each student reviews at least one play
for s in students:
    solver.add(Or(reviews[s]))

# Constraint: Kramer and O'Neill both review Tamerlane (play 1)
solver.add(reviews["Kramer"][1] == True)
solver.add(reviews["O'Neill"][1] == True)

# Constraint: Kramer and Lopez each review fewer plays than Megregian
# Number of plays reviewed by a student = Sum of their review Booleans
num_plays = {s: Sum([If(reviews[s][p], 1, 0) for p in plays]) for s in students}

solver.add(num_plays["Kramer"] < num_plays["Megregian"])
solver.add(num_plays["Lopez"] < num_plays["Megregian"])

# Constraint: Neither Lopez nor Megregian reviews any play Jiang reviews
# For each play, if Jiang reviews it, then Lopez and Megregian do not
for p in plays:
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Lopez"][p])))
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Megregian"][p])))

# Constraint: Exactly two of the students review exactly the same play or plays as each other
# We need to find exactly one pair of students with identical review sets
# Approach: For every pair, check if their review sets are equal, and ensure exactly one such pair exists
pairs = [(s1, s2) for i, s1 in enumerate(students) for s2 in students[i+1:]]

# For each pair, create a condition that their review sets are equal
pair_equal = {pair: And([reviews[pair[0]][p] == reviews[pair[1]][p] for p in plays]) for pair in pairs}

# Exactly one pair must have equal review sets
solver.add(Sum([If(pair_equal[pair], 1, 0) for pair in pairs]) == 1)

# Now, evaluate each answer choice to see if it could be an accurate and complete list
# of the students who review ONLY Sunset (i.e., their review set is {Sunset})

# Helper: A student reviews ONLY Sunset if they review Sunset and do not review Tamerlane or Undulation
def only_sunset_constraint(student):
    return And(
        reviews[student][0],  # Reviews Sunset
        Not(reviews[student][1]),  # Does not review Tamerlane
        Not(reviews[student][2])   # Does not review Undulation
    )

# Answer choices as constraints
answer_choices = [
    ("A", only_sunset_constraint("Lopez")),
    ("B", only_sunset_constraint("O'Neill")),
    ("C", And(only_sunset_constraint("Jiang"), only_sunset_constraint("Lopez"))),
    ("D", And(only_sunset_constraint("Kramer"), only_sunset_constraint("O'Neill"))),
    ("E", And(only_sunset_constraint("Lopez"), only_sunset_constraint("Megregian")))
]

# Evaluate each answer choice
found_options = []
for letter, constr in answer_choices:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")