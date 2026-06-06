from z3 import *

solver = Solver()

# Entities and domains
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Assignments: student -> (day, slot)
# We represent this as a function from (student, day, slot) to Bool
assignments = {}
for s in students:
    for d in days:
        for slot in slots:
            assignments[(s, d, slot)] = Bool(f"{s}_{d}_{slot}")

# Helper: Exactly one student per (day, slot)
for d in days:
    for slot in slots:
        # Exactly one student is assigned to this (day, slot)
        solver.add(sum([If(assignments[(s, d, slot)], 1, 0) for s in students]) == 1)

# Helper: Exactly two reports per day (one morning, one afternoon)
for d in days:
    solver.add(sum([If(assignments[(s, d, "Morning")], 1, 0) for s in students]) == 1)
    solver.add(sum([If(assignments[(s, d, "Afternoon")], 1, 0) for s in students]) == 1)

# Helper: Exactly six students give reports
solver.add(sum([If(Or([assignments[(s, d, slot)] for d in days for slot in slots]), 1, 0) for s in students]) == 6)

# Constraints from the problem statement

# 1. Tuesday is the only day on which George can give a report.
solver.add(Or([assignments[("George", "Tuesday", "Morning")], assignments[("George", "Tuesday", "Afternoon")]]))
solver.add(Not(Or([assignments[("George", "Monday", slot)] for slot in slots])))
solver.add(Not(Or([assignments[("George", "Wednesday", slot)] for slot in slots])))

# 2. Neither Olivia nor Robert can give an afternoon report.
for s in ["Olivia", "Robert"]:
    for d in days:
        solver.add(Not(assignments[(s, d, "Afternoon")]))

# 3. If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
# For each day except Wednesday, if Nina gives a report on that day, then Helen and Irving must give reports the next day.
for i, d in enumerate(days[:-1]):
    next_d = days[i+1]
    # If Nina gives a report on day d, then Helen and Irving must give reports on next_d
    solver.add(Implies(
        Or([assignments[("Nina", d, slot)] for slot in slots]),
        And(
            Or([assignments[("Helen", next_d, slot)] for slot in slots]),
            Or([assignments[("Irving", next_d, slot)] for slot in slots])
        )
    ))

# Additional constraint: Helen, Kyle, and Lenore give the three morning reports (one each on Monday, Tuesday, Wednesday)
# This means:
# - Exactly one of Helen, Kyle, Lenore gives a morning report on Monday
# - Exactly one of Helen, Kyle, Lenore gives a morning report on Tuesday
# - Exactly one of Helen, Kyle, Lenore gives a morning report on Wednesday
# And no other students give morning reports on these days.
for d in days:
    solver.add(sum([If(assignments[(s, d, "Morning")], 1, 0) for s in ["Helen", "Kyle", "Lenore"]]) == 1)
    # No other students give morning reports on day d
    for s in students:
        if s not in ["Helen", "Kyle", "Lenore"]:
            solver.add(Not(assignments[(s, d, "Morning")]))

# Now, evaluate the multiple choice options
found_options = []

# Option A: Helen gives a report on Monday
# This means Helen gives a report on Monday (either morning or afternoon)
solver.push()
solver.add(Or([assignments[("Helen", "Monday", slot)] for slot in slots]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Irving gives a report on Monday
solver.push()
solver.add(Or([assignments[("Irving", "Monday", slot)] for slot in slots]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Irving gives a report on Wednesday
solver.push()
solver.add(Or([assignments[("Irving", "Wednesday", slot)] for slot in slots]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kyle gives a report on Tuesday
solver.push()
solver.add(Or([assignments[("Kyle", "Tuesday", slot)] for slot in slots]))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Kyle gives a report on Wednesday
solver.push()
solver.add(Or([assignments[("Kyle", "Wednesday", slot)] for slot in slots]))
if solver.check() == sat:
    found_options.append("E")
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