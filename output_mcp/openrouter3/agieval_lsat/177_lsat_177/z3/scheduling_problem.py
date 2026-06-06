from z3 import *

# Student indices
G, H, J, K, L = 0, 1, 2, 3, 4
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=First, 1=Second

# work[day][shift] = student who works that shift on that day
work = [[Int(f"work_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Domain constraints: each work variable is between 0 and 4
for d in range(5):
    for s in range(2):
        solver.add(work[d][s] >= 0)
        solver.add(work[d][s] <= 4)

# Each shift has exactly one student (already enforced by domain + uniqueness)
# But we need to ensure no two shifts have same student on same day
for d in range(5):
    solver.add(work[d][0] != work[d][1])

# Each student works exactly 2 shifts total
student_shifts = [Sum([If(work[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) for student in range(5)]
for student in range(5):
    solver.add(student_shifts[student] == 2)

# Louise works second shift on two consecutive days
# Louise is student 4
louise_second_days = [If(work[d][1] == L, 1, 0) for d in range(5)]
# Exactly two days where Louise works second shift
solver.add(Sum(louise_second_days) == 2)
# And they must be consecutive
consecutive_pairs = [(d, d+1) for d in range(4)]
solver.add(Or([And(work[d][1] == L, work[d+1][1] == L) for d in range(4)]))

# Grecia works first shift on two nonconsecutive days
grecia_first_days = [If(work[d][0] == G, 1, 0) for d in range(5)]
solver.add(Sum(grecia_first_days) == 2)
# Nonconsecutive: not on adjacent days
for d in range(4):
    solver.add(Not(And(work[d][0] == G, work[d+1][0] == G)))

# Katya works on Tuesday and Friday (at least one shift each day)
solver.add(Or(work[1][0] == K, work[1][1] == K))  # Tuesday
solver.add(Or(work[4][0] == K, work[4][1] == K))  # Friday

# Hakeem and Joe work on the same day at least once
same_day = []
for d in range(5):
    same_day.append(Or(
        And(work[d][0] == H, work[d][1] == J),
        And(work[d][0] == J, work[d][1] == H),
        And(work[d][0] == H, work[d][0] == J),  # This can't happen due to no same day both shifts
        And(work[d][1] == H, work[d][1] == J)   # This can't happen either
    ))
solver.add(Or(same_day))

# Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(Or(
        And(work[d][0] == G, work[d][1] == L),
        And(work[d][0] == L, work[d][1] == G),
        And(work[d][0] == G, work[d][0] == L),  # Can't happen
        And(work[d][1] == G, work[d][1] == L)   # Can't happen
    )))

# Additional constraint: Hakeem works on Wednesday (given in question)
# Hakeem works at least one shift on Wednesday (day 2)
solver.add(Or(work[2][0] == H, work[2][1] == H))

# Now test each answer choice
# Answer choices are pairs of days that Joe must work on
# We need to check which pair is forced by the constraints

# Define the options as constraints that Joe works on those days
# Note: "Joe must work at the gallery on which one of the following pairs of days?"
# This means Joe works at least one shift on each day in the pair

options = [
    ("A", [0, 2]),  # Monday and Wednesday
    ("B", [0, 3]),  # Monday and Thursday
    ("C", [1, 2]),  # Tuesday and Wednesday
    ("D", [1, 3]),  # Tuesday and Thursday
    ("E", [2, 3])   # Wednesday and Thursday
]

found_options = []
for letter, days in options:
    solver.push()
    # Add constraint that Joe works on each day in the pair
    for day in days:
        solver.add(Or(work[day][0] == J, work[day][1] == J))
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