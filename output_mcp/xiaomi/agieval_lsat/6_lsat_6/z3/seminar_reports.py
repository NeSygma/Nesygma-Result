from z3 import *

solver = Solver()

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
n_students = 8

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = ['Monday', 'Tuesday', 'Wednesday']
n_days = 3

# Slots: 0=morning, 1=afternoon
slots = ['morning', 'afternoon']

# reports[d][s] = student giving report on day d, slot s (-1 if no report, but exactly 6 reports means all slots filled)
reports = [[Int(f'reports_{d}_{s}') for s in range(2)] for d in range(3)]

# Each report is a student index 0-7
for d in range(3):
    for s in range(2):
        solver.add(reports[d][s] >= 0, reports[d][s] < n_students)

# Exactly 6 students give reports (2 per day, 3 days = 6 slots, all filled)
# All 6 reports must be from different students
all_reports = [reports[d][s] for d in range(3) for s in range(2)]
solver.add(Distinct(all_reports))

# George can only give a report on Tuesday (day 1)
for d in range(3):
    for s in range(2):
        if d != 1:  # Not Tuesday
            solver.add(reports[d][s] != 0)  # George = 0

# Olivia (6) and Robert (7) cannot give afternoon reports (slot 1)
for d in range(3):
    solver.add(reports[d][1] != 6)  # Olivia
    solver.add(reports[d][1] != 7)  # Robert

# If Nina (5) gives a report on day d, then on day d+1 (if exists and not Wednesday),
# Helen (1) and Irving (2) must both give reports
# "unless Nina's report is given on Wednesday" means the rule doesn't apply if Nina reports on Wednesday
for d in range(3):
    # Nina gives report on day d
    nina_on_day_d = Or([reports[d][s] == 5 for s in range(2)])
    # If Nina on day d and d < 2 (not Wednesday), then next day Helen and Irving must report
    if d < 2:  # Monday or Tuesday
        # Next day Helen reports
        helen_next = Or([reports[d+1][s] == 1 for s in range(2)])
        # Next day Irving reports
        irving_next = Or([reports[d+1][s] == 2 for s in range(2)])
        solver.add(Implies(nina_on_day_d, And(helen_next, irving_next)))

# Helen (1), Kyle (3), and Lenore (4) give the three morning reports
# Morning reports are reports[d][0] for d=0,1,2
morning_reports = [reports[d][0] for d in range(3)]
# These three students must be exactly the morning reporters
solver.add(Or([And(morning_reports[0] == 1, morning_reports[1] == 3, morning_reports[2] == 4),
              And(morning_reports[0] == 1, morning_reports[1] == 4, morning_reports[2] == 3),
              And(morning_reports[0] == 3, morning_reports[1] == 1, morning_reports[2] == 4),
              And(morning_reports[0] == 3, morning_reports[1] == 4, morning_reports[2] == 1),
              And(morning_reports[0] == 4, morning_reports[1] == 1, morning_reports[2] == 3),
              And(morning_reports[0] == 4, morning_reports[1] == 3, morning_reports[2] == 1)]))

# Now check each option
# (A) Helen gives a report on Monday
opt_a = Or(reports[0][0] == 1, reports[0][1] == 1)

# (B) Irving gives a report on Monday
opt_b = Or(reports[0][0] == 2, reports[0][1] == 2)

# (C) Irving gives a report on Wednesday
opt_c = Or(reports[2][0] == 2, reports[2][1] == 2)

# (D) Kyle gives a report on Tuesday
opt_d = Or(reports[1][0] == 3, reports[1][1] == 3)

# (E) Kyle gives a report on Wednesday
opt_e = Or(reports[2][0] == 3, reports[2][1] == 3)

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

# Also print a sample model for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample solution:")
    for d in range(3):
        for s in range(2):
            student_idx = m.evaluate(reports[d][s]).as_long()
            print(f"  {days[d]} {slots[s]}: {students[student_idx]}")
solver.pop()