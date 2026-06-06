from z3 import *

# Students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1
# We'll assign each student a day (0,1,2) and a time (0,1)
# But exactly 6 students give reports, 2 per day (one morning, one afternoon)

# Let's model: for each student, we have a day slot (0..2) and time slot (0..1)
# If a student is not giving a report, we can set day=-1 or use a Bool variable.

# Better: Use Bool variables for each (student, day, time) combination.
# 8 students * 3 days * 2 times = 48 boolean variables.
# Exactly 6 are True, exactly 2 per day, exactly 1 morning and 1 afternoon per day.

# Variables: s[student][day][time]
s = {}
for st in students:
    s[st] = {}
    for d in range(3):
        s[st][d] = {}
        for t in range(2):
            s[st][d][t] = Bool(f"{st}_{d}_{t}")

solver = Solver()

# Exactly 6 students give reports total
solver.add(Sum([If(s[st][d][t], 1, 0) for st in students for d in range(3) for t in range(2)]) == 6)

# Each student gives at most one report
for st in students:
    solver.add(Sum([If(s[st][d][t], 1, 0) for d in range(3) for t in range(2)]) <= 1)

# Each day: exactly 2 reports, one morning, one afternoon
for d in range(3):
    solver.add(Sum([If(s[st][d][0], 1, 0) for st in students]) == 1)  # one morning
    solver.add(Sum([If(s[st][d][1], 1, 0) for st in students]) == 1)  # one afternoon

# Condition 1: Tuesday is the only day on which George can give a report.
# George can only give report on Tuesday (day 1)
solver.add(Sum([If(s["George"][d][t], 1, 0) for d in [0, 2] for t in range(2)]) == 0)
# George may or may not give a report (if he does, it's Tuesday)

# Condition 2: Neither Olivia nor Robert can give an afternoon report.
for st in ["Olivia", "Robert"]:
    for d in range(3):
        solver.add(s[st][d][1] == False)

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
# "unless Nina's report is given on Wednesday" means: if Nina gives a report on Wednesday, the condition doesn't apply.
# So: If Nina gives a report AND it's not on Wednesday, then on the next day Helen and Irving both give reports.
# Nina gives a report: Or over all slots
nina_gives = Or([s["Nina"][d][t] for d in range(3) for t in range(2)])
# Nina gives on Monday (day 0): then Tuesday (day 1) Helen and Irving both give
nina_monday = Or([s["Nina"][0][t] for t in range(2)])
# Nina gives on Tuesday (day 1): then Wednesday (day 2) Helen and Irving both give
nina_tuesday = Or([s["Nina"][1][t] for t in range(2)])

# If Nina gives on Monday, then on Tuesday Helen and Irving both give
solver.add(Implies(nina_monday, And(
    Or([s["Helen"][1][t] for t in range(2)]),
    Or([s["Irving"][1][t] for t in range(2)])
)))

# If Nina gives on Tuesday, then on Wednesday Helen and Irving both give
solver.add(Implies(nina_tuesday, And(
    Or([s["Helen"][2][t] for t in range(2)]),
    Or([s["Irving"][2][t] for t in range(2)])
)))

# If Nina gives on Wednesday, no constraint triggered (unless clause)

# Now define each option as a set of constraints

def make_option(assignments):
    """assignments is a list of (student, day_str, time_str) tuples"""
    day_map = {"Mon": 0, "Tues": 1, "Wed": 2}
    time_map = {"morning": 0, "afternoon": 1}
    constrs = []
    for st, d_str, t_str in assignments:
        d = day_map[d_str]
        t = time_map[t_str]
        constrs.append(s[st][d][t] == True)
    # Also ensure no other students give reports (exactly these 6)
    assigned_students = [a[0] for a in assignments]
    for st in students:
        if st not in assigned_students:
            constrs.append(And([s[st][d][t] == False for d in range(3) for t in range(2)]))
    return And(constrs)

# Option A: Mon. morning: Helen; Mon. afternoon: Robert; Tues. morning: Olivia; Tues. afternoon: Irving; Wed. morning: Lenore; Wed. afternoon: Kyle
opt_a = make_option([
    ("Helen", "Mon", "morning"),
    ("Robert", "Mon", "afternoon"),
    ("Olivia", "Tues", "morning"),
    ("Irving", "Tues", "afternoon"),
    ("Lenore", "Wed", "morning"),
    ("Kyle", "Wed", "afternoon")
])

# Option B: Mon. morning: Irving; Mon. afternoon: Olivia; Tues. morning: Helen; Tues. afternoon: Kyle; Wed. morning: Nina; Wed. afternoon: Lenore
opt_b = make_option([
    ("Irving", "Mon", "morning"),
    ("Olivia", "Mon", "afternoon"),
    ("Helen", "Tues", "morning"),
    ("Kyle", "Tues", "afternoon"),
    ("Nina", "Wed", "morning"),
    ("Lenore", "Wed", "afternoon")
])

# Option C: Mon. morning: Lenore; Mon. afternoon: Helen; Tues. morning: George; Tues. afternoon: Kyle; Wed. morning: Robert; Wed. afternoon: Irving
opt_c = make_option([
    ("Lenore", "Mon", "morning"),
    ("Helen", "Mon", "afternoon"),
    ("George", "Tues", "morning"),
    ("Kyle", "Tues", "afternoon"),
    ("Robert", "Wed", "morning"),
    ("Irving", "Wed", "afternoon")
])

# Option D: Mon. morning: Nina; Mon. afternoon: Helen; Tues. morning: Robert; Tues. afternoon: Irving; Wed. morning: Olivia; Wed. afternoon: Lenore
opt_d = make_option([
    ("Nina", "Mon", "morning"),
    ("Helen", "Mon", "afternoon"),
    ("Robert", "Tues", "morning"),
    ("Irving", "Tues", "afternoon"),
    ("Olivia", "Wed", "morning"),
    ("Lenore", "Wed", "afternoon")
])

# Option E: Mon. morning: Olivia; Mon. afternoon: Nina; Tues. morning: Irving; Tues. afternoon: Helen; Wed. morning: Kyle; Wed. afternoon: George
opt_e = make_option([
    ("Olivia", "Mon", "morning"),
    ("Nina", "Mon", "afternoon"),
    ("Irving", "Tues", "morning"),
    ("Helen", "Tues", "afternoon"),
    ("Kyle", "Wed", "morning"),
    ("George", "Wed", "afternoon")
])

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