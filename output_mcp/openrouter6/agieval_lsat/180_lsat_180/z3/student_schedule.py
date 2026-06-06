from z3 import *

# Students: Grecia, Hakeem, Joe, Katya, Louise
students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']
student_index = {s: i for i, s in enumerate(students)}
G, H, J, K, L = 0, 1, 2, 3, 4

# Days: Monday to Friday (0..4)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
# Shifts: 0 = first, 1 = second

# schedule[day][shift] = student index
schedule = [[Int(f'schedule_{d}_{s}') for s in range(2)] for d in range(5)]

solver = Solver()

# Each shift must be one of the students (0..4)
for d in range(5):
    for s in range(2):
        solver.add(schedule[d][s] >= 0)
        solver.add(schedule[d][s] <= 4)

# Each student works exactly two shifts total
for stu in range(5):
    solver.add(Sum([If(schedule[d][s] == stu, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# Louise works second shift on two consecutive days
# We need at least one pair of consecutive days where Louise works second shift both days
# Let's define a boolean for each day if Louise works second shift
louise_second = [Bool(f'louise_second_{d}') for d in range(5)]
for d in range(5):
    solver.add(louise_second[d] == (schedule[d][1] == L))
# At least one consecutive pair
solver.add(Or([And(louise_second[d], louise_second[d+1]) for d in range(4)]))

# Grecia works first shift on two nonconsecutive days
# We need at least two days that are not consecutive where Grecia works first shift
grecia_first = [Bool(f'grecia_first_{d}') for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (schedule[d][0] == G))
# Count how many days Grecia works first shift
count_grecia_first = Sum([If(grecia_first[d], 1, 0) for d in range(5)])
solver.add(count_grecia_first >= 2)
# Ensure there exist two nonconsecutive days
# We can enforce that not all days where she works first are consecutive
# For simplicity, we can require that there exists at least one pair of nonconsecutive days
# We'll add a constraint that there exists d1, d2 such that |d1-d2| > 1 and both have Grecia first
# We'll do this by enumerating all pairs of nonconsecutive days
nonconsecutive_pairs = [(d1, d2) for d1 in range(5) for d2 in range(d1+2, 5)]
solver.add(Or([And(grecia_first[d1], grecia_first[d2]) for (d1, d2) in nonconsecutive_pairs]))

# Katya works on Tuesday and Friday
# Tuesday is day 1, Friday is day 4
# She must work at least one shift on each of those days
solver.add(Or([schedule[1][s] == K for s in range(2)]))
solver.add(Or([schedule[4][s] == K for s in range(2)]))
# Since she works exactly two shifts total, she must work exactly one shift on Tuesday and one on Friday
# We can enforce that she works exactly one shift on Tuesday and exactly one on Friday
solver.add(Sum([If(schedule[1][s] == K, 1, 0) for s in range(2)]) == 1)
solver.add(Sum([If(schedule[4][s] == K, 1, 0) for s in range(2)]) == 1)

# Hakeem and Joe work on the same day as each other at least once
# There exists a day where both Hakeem and Joe work (maybe different shifts)
hakeem_works = [Bool(f'hakeem_works_{d}') for d in range(5)]
joe_works = [Bool(f'joe_works_{d}') for d in range(5)]
for d in range(5):
    solver.add(hakeem_works[d] == Or([schedule[d][s] == H for s in range(2)]))
    solver.add(joe_works[d] == Or([schedule[d][s] == J for s in range(2)]))
solver.add(Or([And(hakeem_works[d], joe_works[d]) for d in range(5)]))

# Grecia and Louise never work on the same day as each other
for d in range(5):
    grecia_works = Or([schedule[d][s] == G for s in range(2)])
    louise_works = Or([schedule[d][s] == L for s in range(2)])
    solver.add(Not(And(grecia_works, louise_works)))

# Additional constraint: each shift is worked by exactly one student (already enforced by variable assignment)
# But we need to ensure that each shift is assigned to a student, which is already done.

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Schedule:")
    for d in range(5):
        day_name = days[d]
        first = m[schedule[d][0]].as_long()
        second = m[schedule[d][1]].as_long()
        print(f"{day_name}: First shift: {students[first]}, Second shift: {students[second]}")
    # Also print which students work which days
    print("\nStudent shifts:")
    for stu in range(5):
        shifts = []
        for d in range(5):
            for s in range(2):
                if m[schedule[d][s]].as_long() == stu:
                    shifts.append(f"{days[d]} {'first' if s==0 else 'second'}")
        print(f"{students[stu]}: {', '.join(shifts)}")
elif result == unsat:
    print("STATUS: unsat")
    print("No schedule satisfies all constraints")
else:
    print("STATUS: unknown")