from z3 import *

# Students
students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
student_to_idx = {s: i for i, s in enumerate(students)}

# Days
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day_to_idx = {d: i for i, d in enumerate(Days)}

# Shifts
Shifts = [1, 2]

# Create a 2D array: schedule[student][day] = shift (1 or 2), or 0 if not working
schedule = [[Int(f"schedule_{s}_{d}") for d in Days] for s in students]

solver = Solver()

# Each student works exactly 2 shifts
for s in students:
    shifts_worked = [
        schedule[student_to_idx[s]][day_to_idx[d]]
        for d in Days
    ]
    # Each shift is either 0 (not working), 1, or 2
    for d in Days:
        solver.add(Or(
            schedule[student_to_idx[s]][day_to_idx[d]] == 0,
            schedule[student_to_idx[s]][day_to_idx[d]] == 1,
            schedule[student_to_idx[s]][day_to_idx[d]] == 2
        ))
    # Exactly two shifts are non-zero
    solver.add(Sum([If(schedule[student_to_idx[s]][day_to_idx[d]] != 0, 1, 0) for d in Days]) == 2)

# No student works both shifts of any day
for s in students:
    for d in Days:
        solver.add(Not(And(
            schedule[student_to_idx[s]][day_to_idx[d]] == 1,
            schedule[student_to_idx[s]][day_to_idx[d]] == 2
        )))

# Louise works the second shift on two consecutive days
louise_idx = student_to_idx["Louise"]
consecutive_days = [
    ("Monday", "Tuesday"),
    ("Tuesday", "Wednesday"),
    ("Wednesday", "Thursday"),
    ("Thursday", "Friday")
]
for d1, d2 in consecutive_days:
    solver.add(Or(
        And(
            schedule[louise_idx][day_to_idx[d1]] == 2,
            schedule[louise_idx][day_to_idx[d2]] == 2
        ),
        And(
            schedule[louise_idx][day_to_idx[d1]] != 2,
            schedule[louise_idx][day_to_idx[d2]] != 2
        )
    ))
# Louise must work the second shift on at least two days (not necessarily consecutive)
solver.add(Sum([
    If(schedule[louise_idx][day_to_idx[d]] == 2, 1, 0)
    for d in Days
]) >= 2)

# Grecia works the first shift on two non-consecutive days
grecia_idx = student_to_idx["Grecia"]
# Grecia must work first shift on at least two days
solver.add(Sum([
    If(schedule[grecia_idx][day_to_idx[d]] == 1, 1, 0)
    for d in Days
]) >= 2)

# Katya works on Tuesday and Friday (at least one shift each)
katya_idx = student_to_idx["Katya"]
solver.add(schedule[katya_idx][day_to_idx["Tuesday"]] != 0)
solver.add(schedule[katya_idx][day_to_idx["Friday"]] != 0)

# Hakeem and Joe work on the same day at least once
hakeem_idx = student_to_idx["Hakeem"]
joe_idx = student_to_idx["Joe"]
solver.add(Or([
    And(
        schedule[hakeem_idx][day_to_idx[d]] != 0,
        schedule[joe_idx][day_to_idx[d]] != 0
    )
    for d in Days
]))

# Grecia and Louise never work on the same day
grecia_idx = student_to_idx["Grecia"]
louise_idx = student_to_idx["Louise"]
for d in Days:
    solver.add(Not(And(
        schedule[grecia_idx][day_to_idx[d]] != 0,
        schedule[louise_idx][day_to_idx[d]] != 0
    )))

# Check if the problem is satisfiable
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    for s in students:
        print(f"Schedule for {s}:")
        for d in Days:
            shift = model[schedule[student_to_idx[s]][day_to_idx[d]]]
            if shift is not None and shift != 0:
                print(f"  {d}: shift {shift}")
else:
    print("STATUS: unsat")