from z3 import *

# Scheduling problem: 5 students: Grecia, Hakeem, Joe, Katya, Louise
students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']
# 5 days: Monday, Tuesday, Wednesday, Thursday, Friday
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
# 2 shifts per day: first (0) and second (1)
shifts = [0, 1]

# Variables: for each day and shift, which student works?
# We'll use an integer variable for each shift, representing student index.
# Let's map student names to indices:
student_index = {s: i for i, s in enumerate(students)}
# Shift assignment: shift_assign[day][shift] = student index
shift_assign = [[Int(f'shift_{d}_{sh}') for sh in shifts] for d in days]

solver = Solver()

# Domain constraints: each shift assignment must be a student index (0..4)
for d in range(len(days)):
    for sh in shifts:
        solver.add(shift_assign[d][sh] >= 0)
        solver.add(shift_assign[d][sh] < len(students))

# Each student works exactly two shifts total.
# Count shifts per student.
for s in range(len(students)):
    solver.add(Sum([If(shift_assign[d][sh] == s, 1, 0) for d in range(len(days)) for sh in shifts]) == 2)

# No student works both shifts of any day.
for d in range(len(days)):
    solver.add(shift_assign[d][0] != shift_assign[d][1])

# Louise works the second shift on two consecutive days.
# Louise index is 4.
louise = 4
# Find two consecutive days where she works second shift.
# We'll create Boolean variables for each day indicating if Louise works second shift.
louise_second = [Bool(f'louise_second_{d}') for d in range(len(days))]
for d in range(len(days)):
    solver.add(louise_second[d] == (shift_assign[d][1] == louise))
# Exactly two consecutive days where louise_second is true.
# We'll enforce that there exists a pair of consecutive days where both are true, and no other day is true.
# But the constraint says "On two consecutive days, Louise works the second shift." It doesn't say exactly two days, but at least two consecutive days.
# We'll interpret as: there exists at least one pair of consecutive days where she works second shift.
# We'll also ensure she works second shift on exactly two days? The phrase "on two consecutive days" suggests she works second shift on two days that are consecutive.
# We'll create a constraint that there exists i such that louise_second[i] and louise_second[i+1] are true.
# And we'll also ensure that she works second shift on exactly two days? Not necessarily, but each student works exactly two shifts total, so she can work second shift on at most two days.
# Since she works exactly two shifts total, and she works second shift on two consecutive days, that means her two shifts are both second shifts on consecutive days.
# So we can enforce that she works second shift on exactly two days, and those days are consecutive.
# Let's enforce that she works second shift on exactly two days.
solver.add(Sum([If(louise_second[d], 1, 0) for d in range(len(days))]) == 2)
# And those two days are consecutive.
# We'll create a constraint that there exists i such that louise_second[i] and louise_second[i+1] are true, and all other days are false.
# We'll use an OR over i for consecutive pairs.
consecutive_pairs = []
for i in range(len(days)-1):
    consecutive_pairs.append(And(louise_second[i], louise_second[i+1]))
solver.add(Or(consecutive_pairs))

# On two nonconsecutive days, Grecia works the first shift.
grecia = 0
grecia_first = [Bool(f'grecia_first_{d}') for d in range(len(days))]
for d in range(len(days)):
    solver.add(grecia_first[d] == (shift_assign[d][0] == grecia))
# She works first shift on exactly two days, and those days are nonconsecutive.
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(len(days))]) == 2)
# Nonconsecutive: not consecutive.
# We'll enforce that there is no i such that grecia_first[i] and grecia_first[i+1] are both true.
for i in range(len(days)-1):
    solver.add(Not(And(grecia_first[i], grecia_first[i+1])))

# Katya works on Tuesday and Friday.
katya = 3
# Katya works on Tuesday (day index 1) and Friday (day index 4).
# She works exactly two shifts total, so she works one shift on Tuesday and one shift on Friday.
# We'll enforce that on Tuesday, she works either first or second shift.
solver.add(Or(shift_assign[1][0] == katya, shift_assign[1][1] == katya))
# Similarly for Friday.
solver.add(Or(shift_assign[4][0] == katya, shift_assign[4][1] == katya))
# And she works exactly two shifts total (already enforced by the per-student constraint).

# Hakeem and Joe work on the same day as each other at least once.
hakeem = 1
joe = 2
# For each day, check if both work on that day (either shift).
same_day = [Bool(f'same_day_{d}') for d in range(len(days))]
for d in range(len(days)):
    # Hakeem works on day d if he is assigned to either shift.
    hakeem_works = Or(shift_assign[d][0] == hakeem, shift_assign[d][1] == hakeem)
    joe_works = Or(shift_assign[d][0] == joe, shift_assign[d][1] == joe)
    solver.add(same_day[d] == And(hakeem_works, joe_works))
# At least one day where both work.
solver.add(Or(same_day))

# Grecia and Louise never work on the same day as each other.
# For each day, they cannot both work.
for d in range(len(days)):
    grecia_works = Or(shift_assign[d][0] == grecia, shift_assign[d][1] == grecia)
    louise_works = Or(shift_assign[d][0] == louise, shift_assign[d][1] == louise)
    solver.add(Not(And(grecia_works, louise_works)))

# Additional constraint: each shift is worked by exactly one student (already enforced by assignment variable).

# Check satisfiability.
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Schedule found:")
    for d in range(len(days)):
        for sh in shifts:
            student_idx = m.eval(shift_assign[d][sh])
            student_name = students[student_idx.as_long()]
            shift_name = "first" if sh == 0 else "second"
            print(f"{days[d]} {shift_name}: {student_name}")
elif result == unsat:
    print("STATUS: unsat")
    print("No schedule satisfies constraints.")
else:
    print("STATUS: unknown")