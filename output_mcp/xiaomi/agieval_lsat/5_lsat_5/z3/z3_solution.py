from z3 import *

solver = Solver()

# Students: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
# Days: Monday=0, Tuesday=1, Wednesday=2
# Slots: Morning=0, Afternoon=1

students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
days = ['Monday', 'Tuesday', 'Wednesday']
slots = ['Morning', 'Afternoon']

# report[d][s] = student giving report on day d, slot s
report = [[Int(f'report_{d}_{s}') for s in range(2)] for d in range(3)]

# Each report is one of the 8 students (0-7)
for d in range(3):
    for s in range(2):
        solver.add(report[d][s] >= 0, report[d][s] <= 7)

# Exactly 6 students give reports (2 per day, 3 days = 6 reports total)
# All 6 reports must be from distinct students
all_reports = [report[d][s] for d in range(3) for s in range(2)]
solver.add(Distinct(all_reports))

# Condition 1: Tuesday is the only day George can give a report
# George (0) can only appear on Tuesday (day 1)
for d in range(3):
    for s in range(2):
        if d != 1:  # Not Tuesday
            solver.add(report[d][s] != 0)

# Condition 2: Neither Olivia (6) nor Robert (7) can give an afternoon report
for d in range(3):
    solver.add(report[d][1] != 6)  # Olivia can't be afternoon
    solver.add(report[d][1] != 7)  # Robert can't be afternoon

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
# Nina = 5, Helen = 1, Irving = 2
# If Nina reports on Monday (day 0), then Tuesday must have both Helen and Irving
# If Nina reports on Tuesday (day 1), then Wednesday must have both Helen and Irving
# If Nina reports on Wednesday (day 2), no constraint

# Nina on Monday -> Helen and Irving both on Tuesday
nina_on_monday = Or(report[0][0] == 5, report[0][1] == 5)
helen_on_tuesday = Or(report[1][0] == 1, report[1][1] == 1)
irving_on_tuesday = Or(report[1][0] == 2, report[1][1] == 2)
solver.add(Implies(nina_on_monday, And(helen_on_tuesday, irving_on_tuesday)))

# Nina on Tuesday -> Helen and Irving both on Wednesday
nina_on_tuesday = Or(report[1][0] == 5, report[1][1] == 5)
helen_on_wednesday = Or(report[2][0] == 1, report[2][1] == 1)
irving_on_wednesday = Or(report[2][0] == 2, report[2][1] == 2)
solver.add(Implies(nina_on_tuesday, And(helen_on_wednesday, irving_on_wednesday)))

# Given: Kyle gives the afternoon report on Tuesday
# Kyle = 3
solver.add(report[1][1] == 3)

# Given: Helen gives the afternoon report on Wednesday
# Helen = 1
solver.add(report[2][1] == 1)

# Now evaluate each option for morning reports (Monday morning, Tuesday morning, Wednesday morning)
# report[0][0], report[1][0], report[2][0]

# Option A: Irving(2), Lenore(4), Nina(5)
opt_a = And(report[0][0] == 2, report[1][0] == 4, report[2][0] == 5)

# Option B: Lenore(4), George(0), Irving(2)
opt_b = And(report[0][0] == 4, report[1][0] == 0, report[2][0] == 2)

# Option C: Nina(5), Irving(2), Lenore(4)
opt_c = And(report[0][0] == 5, report[1][0] == 2, report[2][0] == 4)

# Option D: Robert(7), George(0), Irving(2)
opt_d = And(report[0][0] == 7, report[1][0] == 0, report[2][0] == 2)

# Option E: Robert(7), Irving(2), Lenore(4)
opt_e = And(report[0][0] == 7, report[1][0] == 2, report[2][0] == 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for d in range(3):
            for s in range(2):
                stud = m[report[d][s]].as_long()
                print(f"  {days[d]} {slots[s]}: {students[stud]}")
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