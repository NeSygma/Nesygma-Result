from z3 import *

# Students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
n = len(students)  # 8

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1
# day=3 means "no report"

day = [Int(f"day_{s}") for s in students]
time = [Int(f"time_{s}") for s in students]

solver = Solver()

# Domain constraints
for i in range(n):
    solver.add(Or([day[i] == d for d in [0, 1, 2, 3]]))  # 3 = no report
    solver.add(Or([time[i] == t for t in [0, 1]]))

# Exactly six students give reports (day != 3)
solver.add(Sum([If(day[i] != 3, 1, 0) for i in range(n)]) == 6)

# Exactly two reports each day (Monday, Tuesday, Wednesday)
for d in range(3):
    solver.add(Sum([If(day[i] == d, 1, 0) for i in range(n)]) == 2)

# Exactly one morning and one afternoon each day
for d in range(3):
    solver.add(Sum([If(And(day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    solver.add(Sum([If(And(day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Tuesday is the only day on which George can give a report.
# George = index 0
solver.add(Implies(day[0] != 3, day[0] == 1))
solver.add(day[0] != 0)
solver.add(day[0] != 2)

# Neither Olivia nor Robert can give an afternoon report.
# Olivia = index 6, Robert = index 7
solver.add(Implies(day[6] != 3, time[6] == 0))
solver.add(Implies(day[7] != 3, time[7] == 0))

# If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina = index 5, Helen = index 1, Irving = index 2
solver.add(Implies(And(day[5] != 3, day[5] != 2),
                   And(day[1] == day[5] + 1, day[2] == day[5] + 1)))

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")
if result == sat:
    m = solver.model()
    for i, s in enumerate(students):
        d = m[day[i]].as_long()
        t = m[time[i]].as_long()
        if d == 3:
            print(f"{s}: no report")
        else:
            days = ["Monday", "Tuesday", "Wednesday"]
            times = ["morning", "afternoon"]
            print(f"{s}: {days[d]} {times[t]}")
else:
    print("Base constraints are unsatisfiable!")
    # Let's try to debug - maybe the constraints are too strict
    # Let's relax and see what's happening
    solver2 = Solver()
    for i in range(n):
        solver2.add(Or([day[i] == d for d in [0, 1, 2, 3]]))
        solver2.add(Or([time[i] == t for t in [0, 1]]))
    solver2.add(Sum([If(day[i] != 3, 1, 0) for i in range(n)]) == 6)
    for d in range(3):
        solver2.add(Sum([If(day[i] == d, 1, 0) for i in range(n)]) == 2)
    for d in range(3):
        solver2.add(Sum([If(And(day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
        solver2.add(Sum([If(And(day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)
    print(f"Without extra constraints: {solver2.check()}")