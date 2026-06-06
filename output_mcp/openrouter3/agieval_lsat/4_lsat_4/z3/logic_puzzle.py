from z3 import *

# Students and days
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
times = ["Morning", "Afternoon"]

# Create boolean variables: student gives report on day/time
# Using dictionary for easy access
report = {}
for s in students:
    for d in days:
        for t in times:
            report[(s, d, t)] = Bool(f"report_{s}_{d}_{t}")

solver = Solver()

# Constraint 1: Exactly 6 students give reports (2 per day × 3 days = 6 slots)
# But we need to ensure exactly 2 reports per day (one morning, one afternoon)
for d in days:
    # Exactly one report per time slot per day
    morning_reports = [report[(s, d, "Morning")] for s in students]
    afternoon_reports = [report[(s, d, "Afternoon")] for s in students]
    solver.add(Sum([If(r, 1, 0) for r in morning_reports]) == 1)
    solver.add(Sum([If(r, 1, 0) for r in afternoon_reports]) == 1)

# Constraint 2: Tuesday is the only day George can give a report
for d in days:
    if d != "Tuesday":
        for t in times:
            solver.add(Not(report[("George", d, t)]))

# Constraint 3: Neither Olivia nor Robert can give an afternoon report
for d in days:
    solver.add(Not(report[("Olivia", d, "Afternoon")]))
    solver.add(Not(report[("Robert", d, "Afternoon")]))

# Constraint 4: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday
# We need to model "next day" - for Monday Nina -> Tuesday Helen and Irving both give reports
# For Tuesday Nina -> Wednesday Helen and Irving both give reports
# For Wednesday Nina -> no constraint (unless clause)

# For each day Nina gives a report (except Wednesday), the next day must have both Helen and Irving
for i, d in enumerate(days):
    if d != "Wednesday":
        next_day = days[i+1]
        # If Nina gives any report on day d, then next day Helen and Irving must give reports
        # (in any time slot)
        nina_on_d = Or([report[("Nina", d, t)] for t in times])
        helen_on_next = Or([report[("Helen", next_day, t)] for t in times])
        irving_on_next = Or([report[("Irving", next_day, t)] for t in times])
        solver.add(Implies(nina_on_d, And(helen_on_next, irving_on_next)))

# Additional given: George, Nina, and Robert give reports and they do so on different days
# George gives report on Tuesday (only possible day)
solver.add(Or([report[("George", "Tuesday", t)] for t in times]))

# Nina gives a report (some day)
solver.add(Or([report[("Nina", d, t)] for d in days for t in times]))

# Robert gives a report (some day, but only morning since no afternoon)
solver.add(Or([report[("Robert", d, "Morning")] for d in days]))

# They give reports on different days from one another
# George is on Tuesday, so Nina and Robert cannot be on Tuesday
for t in times:
    solver.add(Not(report[("Nina", "Tuesday", t)]))
    solver.add(Not(report[("Robert", "Tuesday", t)]))

# Nina and Robert must be on different days
# We'll enforce this by ensuring they don't share any day
for d in days:
    nina_on_d = Or([report[("Nina", d, t)] for t in times])
    robert_on_d = Or([report[("Robert", d, t)] for t in times])
    solver.add(Not(And(nina_on_d, robert_on_d)))

# Additional constraint: Exactly 6 students give reports
# We have 8 students, but only 6 slots. We need to ensure exactly 6 students are selected.
# Let's create a variable for each student: does this student give any report?
student_gives = {}
for s in students:
    student_gives[s] = Or([report[(s, d, t)] for d in days for t in times])

# Exactly 6 students give reports
solver.add(Sum([If(student_gives[s], 1, 0) for s in students]) == 6)

# Now test each option
found_options = []

# Option A: Helen gives a report on Wednesday
opt_a = Or([report[("Helen", "Wednesday", t)] for t in times])
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Nina gives a report on Monday
opt_b = Or([report[("Nina", "Monday", t)] for t in times])
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Nina gives a report on Tuesday
opt_c = Or([report[("Nina", "Tuesday", t)] for t in times])
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Olivia gives a report on Monday
opt_d = Or([report[("Olivia", "Monday", t)] for t in times])
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Robert gives a report on Wednesday
opt_e = Or([report[("Robert", "Wednesday", "Morning")]])  # Robert can only give morning reports
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")