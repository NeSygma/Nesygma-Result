from z3 import *

# Base constraints for the problem
solver = Solver()

# Days: Monday (0), Tuesday (1), Wednesday (2), Thursday (3), Friday (4)
days = range(5)
students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']
shifts = ['first', 'second']

# Decision variables: second_shift[day] = student working the second shift on that day
second_shift = [Int(f'second_shift_{day}') for day in days]

# Each student works exactly two shifts (total shifts = 5 days * 1 second shift = 5 shifts)
# Since each student works exactly two shifts in total (across both first and second shifts),
# and there are 5 students, the total shifts worked is 5 students * 2 shifts = 10 shifts.
# There are 5 first shifts and 5 second shifts, totaling 10 shifts.
# So, the second_shift variable assignments must ensure that each student appears exactly twice in the 10 shifts.

# Helper: first_shift[day] = student working the first shift on that day
first_shift = [Int(f'first_shift_{day}') for day in days]

# All students must be assigned to shifts
for day in days:
    solver.add(second_shift[day] >= 0, second_shift[day] < 5)
    solver.add(first_shift[day] >= 0, first_shift[day] < 5)

# No student works both shifts of any day
for day in days:
    solver.add(second_shift[day] != first_shift[day])

# On two consecutive days, Louise works the second shift
# Find two consecutive days where Louise is assigned to second_shift
consecutive_louise_days = []
for i in range(4):
    # Check if Louise (index 4) is assigned to second_shift on day i and i+1
    solver.push()
    solver.add(second_shift[i] == 4)
    solver.add(second_shift[i+1] == 4)
    if solver.check() == sat:
        consecutive_louise_days.append((i, i+1))
    solver.pop()

# We need at least one pair of consecutive days where Louise works the second shift
solver.add(Or([And(second_shift[i] == 4, second_shift[i+1] == 4) for i in range(4)]))

# On two nonconsecutive days, Grecia works the first shift
# Find two nonconsecutive days where Grecia is assigned to first_shift
nonconsecutive_grecia_days = []
for i in range(5):
    for j in range(i+2, 5):  # Ensure nonconsecutive
        solver.push()
        solver.add(first_shift[i] == 0)  # Grecia is index 0
        solver.add(first_shift[j] == 0)
        if solver.check() == sat:
            nonconsecutive_grecia_days.append((i, j))
        solver.pop()

# We need at least one pair of nonconsecutive days where Grecia works the first shift
solver.add(Or([And(first_shift[i] == 0, first_shift[j] == 0) for i in range(5) for j in range(i+2, 5)]))

# Katya works on Tuesday (day 1) and Friday (day 4)
# Katya must be assigned to either first or second shift on these days
solver.add(Or(first_shift[1] == 3, second_shift[1] == 3))  # Tuesday
solver.add(Or(first_shift[4] == 3, second_shift[4] == 3))  # Friday

# Hakeem and Joe work on the same day as each other at least once
# Find at least one day where both Hakeem (1) and Joe (2) are assigned to either first or second shift
solver.add(Or([
    And(Or(first_shift[day] == 1, second_shift[day] == 1), Or(first_shift[day] == 2, second_shift[day] == 2))
    for day in days
]))

# Grecia and Louise never work on the same day as each other
# For each day, Grecia and Louise cannot both be assigned to any shift
for day in days:
    solver.add(Not(And(Or(first_shift[day] == 0, second_shift[day] == 0), 
                       Or(first_shift[day] == 4, second_shift[day] == 4))))

# Each student works exactly two shifts in total (across all days and both shifts)
# We need to ensure that each student appears exactly twice in the combined list of first_shift and second_shift
for student_idx in range(5):
    solver.add(Sum([If(first_shift[day] == student_idx, 1, 0) for day in days]) + 
               Sum([If(second_shift[day] == student_idx, 1, 0) for day in days]) == 2)

# Now, evaluate the multiple choice options
# Map students to indices: Grecia=0, Hakeem=1, Joe=2, Katya=3, Louise=4

# Option A: Hakeem, Louise, Louise, Hakeem, Katya
# Indices: Hakeem=1, Louise=4, Katya=3
opt_a_constr = And(
    second_shift[0] == 1,
    second_shift[1] == 4,
    second_shift[2] == 4,
    second_shift[3] == 1,
    second_shift[4] == 3
)

# Option B: Joe, Hakeem, Grecia, Louise, Louise
# Indices: Joe=2, Hakeem=1, Grecia=0, Louise=4
opt_b_constr = And(
    second_shift[0] == 2,
    second_shift[1] == 1,
    second_shift[2] == 0,
    second_shift[3] == 4,
    second_shift[4] == 4
)

# Option C: Joe, Katya, Hakeem, Louise, Katya
# Indices: Joe=2, Katya=3, Hakeem=1, Louise=4
opt_c_constr = And(
    second_shift[0] == 2,
    second_shift[1] == 3,
    second_shift[2] == 1,
    second_shift[3] == 4,
    second_shift[4] == 3
)

# Option D: Louise, Katya, Joe, Louise, Katya
# Indices: Louise=4, Katya=3, Joe=2
opt_d_constr = And(
    second_shift[0] == 4,
    second_shift[1] == 3,
    second_shift[2] == 2,
    second_shift[3] == 4,
    second_shift[4] == 3
)

# Option E: Louise, Louise, Hakeem, Joe, Joe
# Indices: Louise=4, Hakeem=1, Joe=2
opt_e_constr = And(
    second_shift[0] == 4,
    second_shift[1] == 4,
    second_shift[2] == 1,
    second_shift[3] == 2,
    second_shift[4] == 2
)

# Test each option
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