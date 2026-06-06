from z3 import *

solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 0=first, 1=second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

# We need to assign students to shifts for each day
# schedule[day][shift] = student
schedule = [[Int(f'schedule_{d}_{s}') for s in range(2)] for d in range(5)]

# Each student works exactly two shifts
for student in range(5):
    solver.add(Sum([If(schedule[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# Each shift is worked by exactly one student
for d in range(5):
    for s in range(2):
        solver.add(schedule[d][s] >= 0, schedule[d][s] <= 4)

# No student works both shifts of any day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# On two consecutive days, Louise works the second shift
# Louise is student 4
# We need to find two consecutive days where Louise works second shift
consecutive_louise = []
for d in range(4):  # Monday-Thursday, check d and d+1
    consecutive_louise.append(And(schedule[d][1] == 4, schedule[d+1][1] == 4))
solver.add(Or(consecutive_louise))

# On two nonconsecutive days, Grecia works the first shift
# Grecia is student 0
# We need to find two days that are not consecutive where Grecia works first shift
nonconsecutive_grecia = []
for d1 in range(5):
    for d2 in range(d1+2, 5):  # d2 >= d1+2 ensures nonconsecutive
        nonconsecutive_grecia.append(And(schedule[d1][0] == 0, schedule[d2][0] == 0))
solver.add(Or(nonconsecutive_grecia))

# Katya works on Tuesday and Friday
# Katya is student 3
# Tuesday is day 1, Friday is day 4
# She works at least one shift on each of these days
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Hakeem and Joe work on the same day as each other at least once
# Hakeem is student 1, Joe is student 2
same_day = []
for d in range(5):
    # They could work different shifts on the same day
    same_day.append(Or(
        And(schedule[d][0] == 1, schedule[d][1] == 2),
        And(schedule[d][0] == 2, schedule[d][1] == 1),
        And(schedule[d][0] == 1, schedule[d][0] == 2),  # Same shift? Not possible since one shift per student
        And(schedule[d][1] == 1, schedule[d][1] == 2)   # Same shift? Not possible
    ))
solver.add(Or(same_day))

# Grecia and Louise never work on the same day as each other
for d in range(5):
    # They cannot both work on day d
    solver.add(Not(Or(
        And(schedule[d][0] == 0, schedule[d][1] == 4),
        And(schedule[d][0] == 4, schedule[d][1] == 0),
        And(schedule[d][0] == 0, schedule[d][0] == 4),  # Same shift? Not possible
        And(schedule[d][1] == 0, schedule[d][1] == 4)   # Same shift? Not possible
    )))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Student schedule found:")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
    
    for d in range(5):
        first_student = m.evaluate(schedule[d][0]).as_long()
        second_student = m.evaluate(schedule[d][1]).as_long()
        print(f"{days[d]}: First shift = {students[first_student]}, Second shift = {students[second_student]}")
    
    # Check which answer choice might correspond
    print("\nNow checking cookbook scheduling options...")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")