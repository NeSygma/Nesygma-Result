from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Medium: Oil=0, Watercolor=1
# Walls: 1,2,3,4
# Position: Upper=0, Lower=1

# For each wall (0-3) and position (0=upper, 1=lower), we have (student, medium)
student = [[Int(f"student_w{w}_p{p}") for p in range(2)] for w in range(4)]
medium = [[Int(f"medium_w{w}_p{p}") for p in range(2)] for w in range(4)]

# Domain constraints: student in {0,1,2,3}, medium in {0,1}
for w in range(4):
    for p in range(2):
        solver.add(student[w][p] >= 0, student[w][p] <= 3)
        solver.add(medium[w][p] >= 0, medium[w][p] <= 1)

# Each student has exactly one oil and one watercolor (2 paintings each, 8 total, 8 slots)
# Each student appears exactly twice
for s in range(4):
    solver.add(Sum([If(student[w][p] == s, 1, 0) for w in range(4) for p in range(2)]) == 2)

# Each student has exactly one oil and one watercolor
for s in range(4):
    solver.add(Sum([If(And(student[w][p] == s, medium[w][p] == 0), 1, 0) for w in range(4) for p in range(2)]) == 1)
    solver.add(Sum([If(And(student[w][p] == s, medium[w][p] == 1), 1, 0) for w in range(4) for p in range(2)]) == 1)

# Each wall has exactly 2 paintings (already by structure)

# Condition 1: No wall has only watercolors displayed on it.
# Each wall must have at least one oil
for w in range(4):
    solver.add(Or(medium[w][0] == 0, medium[w][1] == 0))

# Condition 2: No wall has the work of only one student displayed on it.
# The two students on each wall must be different
for w in range(4):
    solver.add(student[w][0] != student[w][1])

# Condition 3: No wall has both a painting by Franz (0) and a painting by Isaacs (3) displayed on it.
for w in range(4):
    solver.add(Not(Or(
        And(student[w][0] == 0, student[w][1] == 3),
        And(student[w][0] == 3, student[w][1] == 0)
    )))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# Franz's oil: student=0, medium=0. Find which wall it's on, then Greene's watercolor (student=1, medium=1) is upper on that wall.
for w in range(4):
    # If Franz's oil is on wall w (either position), then Greene's watercolor is upper on wall w
    franz_oil_on_w = Or(
        And(student[w][0] == 0, medium[w][0] == 0),
        And(student[w][1] == 0, medium[w][1] == 0)
    )
    greene_wc_upper_w = And(student[w][0] == 1, medium[w][0] == 1)
    solver.add(Implies(franz_oil_on_w, greene_wc_upper_w))

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
# Wall 4 = index 3, lower position = index 1
solver.add(student[3][1] == 3)  # Isaacs
solver.add(medium[3][1] == 0)   # Oil

# Now evaluate each answer choice
# Each choice specifies the lower position paintings for walls 1-4
# Lower position is position index 1

# (A) Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil
opt_a = And(
    student[0][1] == 0, medium[0][1] == 0,  # Franz's oil
    student[1][1] == 0, medium[1][1] == 1,  # Franz's watercolor
    student[2][1] == 1, medium[2][1] == 0,  # Greene's oil
    student[3][1] == 3, medium[3][1] == 0   # Isaacs's oil
)

# (B) Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil
opt_b = And(
    student[0][1] == 0, medium[0][1] == 0,  # Franz's oil
    student[1][1] == 2, medium[1][1] == 1,  # Hidalgo's watercolor
    student[2][1] == 3, medium[2][1] == 1,  # Isaacs's watercolor
    student[3][1] == 3, medium[3][1] == 0   # Isaacs's oil
)

# (C) Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil
opt_c = And(
    student[0][1] == 1, medium[0][1] == 0,  # Greene's oil
    student[1][1] == 0, medium[1][1] == 0,  # Franz's oil
    student[2][1] == 3, medium[2][1] == 0,  # Isaacs's oil
    student[3][1] == 2, medium[3][1] == 0   # Hidalgo's oil
)

# (D) Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil
opt_d = And(
    student[0][1] == 2, medium[0][1] == 0,  # Hidalgo's oil
    student[1][1] == 1, medium[1][1] == 0,  # Greene's oil
    student[2][1] == 1, medium[2][1] == 1,  # Greene's watercolor
    student[3][1] == 3, medium[3][1] == 0   # Isaacs's oil
)

# (E) Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil
opt_e = And(
    student[0][1] == 2, medium[0][1] == 1,  # Hidalgo's watercolor
    student[1][1] == 0, medium[1][1] == 0,  # Franz's oil
    student[2][1] == 1, medium[2][1] == 0,  # Greene's oil
    student[3][1] == 3, medium[3][1] == 0   # Isaacs's oil
)

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