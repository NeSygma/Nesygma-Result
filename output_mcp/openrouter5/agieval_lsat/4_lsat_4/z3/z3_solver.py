from z3 import *

# Eight students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
# Days: Monday (0), Tuesday (1), Wednesday (2)
# Times: morning (0), afternoon (1)
# Exactly 6 reports, 2 per day (one morning, one afternoon)

# We'll model each student's assignment: day and time slot
# Use Int variables for day (0=Mon,1=Tue,2=Wed) and time (0=AM,1=PM)
# A student not giving a report gets a special sentinel: day=3, time=0 (or we can use a Bool for whether they report)

students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
n = len(students)

# For each student: (reports, day, time)
# reports[i] = True if student i gives a report
reports = [Bool(f"reports_{i}") for i in range(n)]
day = [Int(f"day_{i}") for i in range(n)]
time = [Int(f"time_{i}") for i in range(n)]  # 0=AM, 1=PM

solver = Solver()

# Domain constraints
for i in range(n):
    # If reports, day in {0,1,2} and time in {0,1}
    solver.add(Implies(reports[i], And(day[i] >= 0, day[i] <= 2)))
    solver.add(Implies(reports[i], And(time[i] >= 0, time[i] <= 1)))
    # If not reports, set day=3, time=0 as sentinel (doesn't matter)
    solver.add(Implies(Not(reports[i]), day[i] == 3))
    solver.add(Implies(Not(reports[i]), time[i] == 0))

# Exactly six students give reports
solver.add(Sum([If(reports[i], 1, 0) for i in range(n)]) == 6)

# Exactly two reports each day, one morning and one afternoon
for d in range(3):
    # Exactly 2 reports on day d
    solver.add(Sum([If(And(reports[i], day[i] == d), 1, 0) for i in range(n)]) == 2)
    # Exactly 1 morning report on day d
    solver.add(Sum([If(And(reports[i], day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    # Exactly 1 afternoon report on day d
    solver.add(Sum([If(And(reports[i], day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Condition: Tuesday is the only day on which George can give a report.
# George is index 0
# If George reports, he must be on Tuesday (day=1)
solver.add(Implies(reports[0], day[0] == 1))
# George cannot report on Monday or Wednesday
solver.add(Implies(reports[0], day[0] != 0))
solver.add(Implies(reports[0], day[0] != 2))
# Actually, "Tuesday is the only day on which George can give a report" means
# if George gives a report, it must be Tuesday. And he cannot give a report on other days.
# But also: if George doesn't report, that's fine.

# Condition: Neither Olivia nor Robert can give an afternoon report.
# Olivia is index 6, Robert is index 7
solver.add(Implies(reports[6], time[6] != 1))  # Olivia not afternoon
solver.add(Implies(reports[7], time[7] != 1))  # Robert not afternoon

# Condition: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina is index 5, Helen is index 1, Irving is index 2
# If Nina reports and Nina's day is not Wednesday (day != 2), then:
# On the next day (day+1), Helen and Irving both give reports.
solver.add(Implies(And(reports[5], day[5] != 2),
                   And(reports[1], reports[2],
                       day[1] == day[5] + 1,
                       day[2] == day[5] + 1)))
# If Nina reports on Wednesday, the condition doesn't apply (the "unless" clause)

# Additional constraint from the condition: if Nina reports on Tuesday (day=1),
# then on Wednesday (day=2) Helen and Irving must both report.
# If Nina reports on Monday (day=0), then on Tuesday (day=1) Helen and Irving must both report.

# Given condition: George, Nina, and Robert give reports and they do so on different days from one another.
# George (0), Nina (5), Robert (7) all report
solver.add(reports[0])
solver.add(reports[5])
solver.add(reports[7])

# They are on different days
solver.add(Distinct(day[0], day[5], day[7]))

# Now evaluate each option
# (A) Helen gives a report on Wednesday.
opt_a = And(reports[1], day[1] == 2)

# (B) Nina gives a report on Monday.
opt_b = And(reports[5], day[5] == 0)

# (C) Nina gives a report on Tuesday.
opt_c = And(reports[5], day[5] == 1)

# (D) Olivia gives a report on Monday.
opt_d = And(reports[6], day[6] == 0)

# (E) Robert gives a report on Wednesday.
opt_e = And(reports[7], day[7] == 2)

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