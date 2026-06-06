from z3 import *

# Students and days
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
times = ["Morning", "Afternoon"]

# Create variables: reports[student][day][time] = Bool
reports = {}
for s in students:
    reports[s] = {}
    for d in days:
        reports[s][d] = {}
        for t in times:
            reports[s][d][t] = Bool(f"report_{s}_{d}_{t}")

solver = Solver()

# Constraint 1: Exactly 6 students give reports (2 per day × 3 days = 6 slots)
# Actually, we need exactly 2 reports per day (one morning, one afternoon)
for d in days:
    # Exactly one report per time slot per day
    morning_reports = [reports[s][d]["Morning"] for s in students]
    afternoon_reports = [reports[s][d]["Afternoon"] for s in students]
    solver.add(Sum([If(r, 1, 0) for r in morning_reports]) == 1)
    solver.add(Sum([If(r, 1, 0) for r in afternoon_reports]) == 1)

# Constraint 2: Tuesday is the only day George can give a report
for d in days:
    if d != "Tuesday":
        solver.add(Not(reports["George"][d]["Morning"]))
        solver.add(Not(reports["George"][d]["Afternoon"]))

# Constraint 3: Neither Olivia nor Robert can give an afternoon report
for d in days:
    solver.add(Not(reports["Olivia"][d]["Afternoon"]))
    solver.add(Not(reports["Robert"][d]["Afternoon"]))

# Constraint 4: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday
for d_idx, d in enumerate(days):
    if d_idx < 2:  # Not Wednesday
        next_day = days[d_idx + 1]
        # If Nina gives any report on day d, then both Helen and Irving must give reports on next_day
        nina_gives = Or(reports["Nina"][d]["Morning"], reports["Nina"][d]["Afternoon"])
        helen_gives_next = Or(reports["Helen"][next_day]["Morning"], reports["Helen"][next_day]["Afternoon"])
        irving_gives_next = Or(reports["Irving"][next_day]["Morning"], reports["Irving"][next_day]["Afternoon"])
        solver.add(Implies(nina_gives, And(helen_gives_next, irving_gives_next)))

# Additional condition: Helen, Kyle, and Lenore give the three morning reports
# This means exactly these three students give morning reports (one each day)
morning_students = ["Helen", "Kyle", "Lenore"]
all_morning_reports = []
for d in days:
    for s in students:
        all_morning_reports.append(reports[s][d]["Morning"])

# Exactly 3 morning reports total, and they must be from Helen, Kyle, Lenore
solver.add(Sum([If(r, 1, 0) for r in all_morning_reports]) == 3)

# Each of Helen, Kyle, Lenore gives exactly one morning report
for s in morning_students:
    morning_reports_s = [reports[s][d]["Morning"] for d in days]
    solver.add(Sum([If(r, 1, 0) for r in morning_reports_s]) == 1)

# No other student gives a morning report
for s in students:
    if s not in morning_students:
        for d in days:
            solver.add(Not(reports[s][d]["Morning"]))

# Additional constraint: Each student can give at most one report total
for s in students:
    all_reports_s = []
    for d in days:
        for t in times:
            all_reports_s.append(reports[s][d][t])
    solver.add(Sum([If(r, 1, 0) for r in all_reports_s]) <= 1)

# Now test each answer choice
found_options = []

# Option A: Helen gives a report on Monday
opt_a = Or(reports["Helen"]["Monday"]["Morning"], reports["Helen"]["Monday"]["Afternoon"])
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Irving gives a report on Monday
opt_b = Or(reports["Irving"]["Monday"]["Morning"], reports["Irving"]["Monday"]["Afternoon"])
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Irving gives a report on Wednesday
opt_c = Or(reports["Irving"]["Wednesday"]["Morning"], reports["Irving"]["Wednesday"]["Afternoon"])
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kyle gives a report on Tuesday
opt_d = Or(reports["Kyle"]["Tuesday"]["Morning"], reports["Kyle"]["Tuesday"]["Afternoon"])
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Kyle gives a report on Wednesday
opt_e = Or(reports["Kyle"]["Wednesday"]["Morning"], reports["Kyle"]["Wednesday"]["Afternoon"])
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Check which options are always true (must be true)
# We need to check which options are true in ALL satisfying models
# For "must be true", we need to check if the negation leads to unsat

must_be_true = []
for letter, opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(opt))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")