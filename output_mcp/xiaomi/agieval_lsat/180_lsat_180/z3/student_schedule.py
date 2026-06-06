from z3 import *

solver = Solver()

# Five students: Grecia, Hakeem, Joe, Katya, Louise
# Five days: Monday through Friday
# Two shifts per day: first and second
# Each student works exactly two shifts
# No student works both shifts of any day

# Let's define variables for each shift assignment
# shift[day][shift] = student (0-4)
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

days = 5  # Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
shifts = 2  # first=0, second=1

# Create variables for each shift
shift_vars = [[Int(f'shift_{d}_{s}') for s in range(shifts)] for d in range(days)]

# Each shift must be assigned to exactly one student (0-4)
for d in range(days):
    for s in range(shifts):
        solver.add(shift_vars[d][s] >= 0, shift_vars[d][s] <= 4)

# Each student works exactly two shifts
for student in range(5):
    solver.add(Sum([If(shift_vars[d][s] == student, 1, 0) 
                   for d in range(days) for s in range(shifts)]) == 2)

# No student works both shifts of any day
for d in range(days):
    solver.add(shift_vars[d][0] != shift_vars[d][1])

# Constraint: On two consecutive days, Louise works the second shift
# Louise is student 4
# We need to find two consecutive days where Louise works second shift
consecutive_louise = []
for d in range(4):  # Monday-Thursday
    consecutive_louise.append(And(shift_vars[d][1] == 4, shift_vars[d+1][1] == 4))
solver.add(Or(consecutive_louise))

# Constraint: On two nonconsecutive days, Grecia works the first shift
# Grecia is student 0
# We need to find two nonconsecutive days where Grecia works first shift
nonconsecutive_grecia = []
for d1 in range(days):
    for d2 in range(d1+2, days):  # At least one day gap
        nonconsecutive_grecia.append(And(shift_vars[d1][0] == 0, shift_vars[d2][0] == 0))
solver.add(Or(nonconsecutive_grecia))

# Constraint: Katya works on Tuesday and Friday
# Katya is student 3
# Tuesday is day 1, Friday is day 4
# She must work at least one shift on each of these days
solver.add(Or(shift_vars[1][0] == 3, shift_vars[1][1] == 3))
solver.add(Or(shift_vars[4][0] == 3, shift_vars[4][1] == 3))

# Constraint: Hakeem and Joe work on the same day as each other at least once
# Hakeem is student 1, Joe is student 2
same_day = []
for d in range(days):
    # They could work different shifts on the same day
    same_day.append(Or(
        And(shift_vars[d][0] == 1, shift_vars[d][1] == 2),
        And(shift_vars[d][0] == 2, shift_vars[d][1] == 1)
    ))
solver.add(Or(same_day))

# Constraint: Grecia and Louise never work on the same day as each other
# Grecia is student 0, Louise is student 4
for d in range(days):
    # They cannot both work on the same day (any combination of shifts)
    solver.add(Not(Or(
        And(shift_vars[d][0] == 0, shift_vars[d][1] == 4),
        And(shift_vars[d][0] == 4, shift_vars[d][1] == 0),
        And(shift_vars[d][0] == 0, shift_vars[d][0] == 4),  # This is impossible anyway
        And(shift_vars[d][1] == 0, shift_vars[d][1] == 4)   # This is impossible anyway
    )))

# Now we need to check which answer choice is acceptable
# The answer choices are about cookbook scheduling, not student scheduling
# This suggests there might be a mapping or the problem is misstated

# Let's try to see if any solution exists
result = solver.check()

if result == sat:
    print("STATUS: sat")
    print("Student scheduling solution found:")
    m = solver.model()
    for d in range(days):
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][d]
        print(f"{day_name}:")
        for s in range(shifts):
            shift_name = ["First", "Second"][s]
            student_id = m.evaluate(shift_vars[d][s]).as_long()
            student_name = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"][student_id]
            print(f"  {shift_name} shift: {student_name}")
else:
    print("STATUS: unsat")
    print("No valid student schedule exists with given constraints")