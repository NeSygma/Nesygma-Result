from z3 import *

# Eight students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
# Exactly six give reports (two do not). We are told Kyle and Lenore do NOT give reports.
# So the six who give reports are: George, Helen, Irving, Nina, Olivia, Robert
# Days: Monday (0), Tuesday (1), Wednesday (2)
# Times: morning (0), afternoon (1)

students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
# Indices for the six reporting students
# George=0, Helen=1, Irving=2, Nina=5, Olivia=6, Robert=7

# We'll assign each student a day (0,1,2) and a time (0=morning, 1=afternoon)
# But we need exactly 2 reports per day, one morning one afternoon.

# Let's use variables: for each student, day and time slot.
# Since Kyle and Lenore don't give reports, we only model the other 6.

reporting = [0, 1, 2, 5, 6, 7]  # indices of George, Helen, Irving, Nina, Olivia, Robert

day = [Int(f"day_{s}") for s in range(8)]
time = [Int(f"time_{s}") for s in range(8)]

solver = Solver()

# Domain constraints for reporting students
for s in reporting:
    solver.add(day[s] >= 0, day[s] <= 2)  # Monday=0, Tuesday=1, Wednesday=2
    solver.add(time[s] >= 0, time[s] <= 1)  # morning=0, afternoon=1

# Kyle and Lenore don't give reports - we don't constrain them (they're irrelevant)

# Exactly two reports each day, one morning and one afternoon
# For each day d, exactly one reporting student has day=d and time=0 (morning)
# and exactly one has day=d and time=1 (afternoon)
for d in range(3):
    # morning
    solver.add(Sum([If(And(day[s] == d, time[s] == 0), 1, 0) for s in reporting]) == 1)
    # afternoon
    solver.add(Sum([If(And(day[s] == d, time[s] == 1), 1, 0) for s in reporting]) == 1)

# Condition 1: Tuesday is the only day on which George can give a report.
# George must give a report on Tuesday (day=1)
solver.add(day[0] == 1)  # George is index 0

# Condition 2: Neither Olivia nor Robert can give an afternoon report.
solver.add(time[6] == 0)  # Olivia morning only
solver.add(time[7] == 0)  # Robert morning only

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina is index 5, Helen is index 1, Irving is index 2
# If Nina gives report on Monday (day=0), then on Tuesday (day=1) Helen and Irving both give reports
# If Nina gives report on Tuesday (day=1), then on Wednesday (day=2) Helen and Irving both give reports
# If Nina gives report on Wednesday (day=2), no constraint (the "unless" case)

# Encode: For each possible day d for Nina, if d != 2, then Helen and Irving must both be on day d+1
for d in range(2):  # Monday and Tuesday
    solver.add(Implies(day[5] == d, And(day[1] == d+1, day[2] == d+1)))

# Now evaluate each option.
# Each option gives the morning reports on Monday, Tuesday, Wednesday respectively.
# So option A: morning Monday = Helen, morning Tuesday = George, morning Wednesday = Nina
# etc.

# We need to encode: for each option, the morning report on each day is as specified.
# That means: for day d, the student named in the option has time=0 and day=d.

def make_option_constr(monday_name, tuesday_name, wednesday_name):
    """Return a constraint that the morning reports are as given."""
    name_to_idx = {"George":0, "Helen":1, "Irving":2, "Kyle":3, "Lenore":4, "Nina":5, "Olivia":6, "Robert":7}
    m_idx = name_to_idx[monday_name]
    t_idx = name_to_idx[tuesday_name]
    w_idx = name_to_idx[wednesday_name]
    constr = And(
        day[m_idx] == 0, time[m_idx] == 0,
        day[t_idx] == 1, time[t_idx] == 0,
        day[w_idx] == 2, time[w_idx] == 0
    )
    return constr

options = [
    ("A", make_option_constr("Helen", "George", "Nina")),
    ("B", make_option_constr("Irving", "Robert", "Helen")),
    ("C", make_option_constr("Nina", "Helen", "Olivia")),
    ("D", make_option_constr("Olivia", "Robert", "Irving")),
    ("E", make_option_constr("Robert", "George", "Helen"))
]

found_options = []
for letter, constr in options:
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