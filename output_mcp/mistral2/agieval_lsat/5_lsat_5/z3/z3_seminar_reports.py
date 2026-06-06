from z3 import *

solver = Solver()

# Entities and days
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Total reports: 6 out of 8 students
# Exactly 2 reports per day (Morning and Afternoon)
# Exactly 6 students give reports

# Decision variables: assignment of students to (day, slot)
# We represent this as a dictionary: assignment[day][slot] = student
# Use String instead of StrSort for compatibility
assignment = {
    day: {
        slot: Const(f"{day}_{slot}", StringSort())
        for slot in slots
    }
    for day in days
}

# Helper: all assigned students (flattened)
assigned_students = [assignment[day][slot] for day in days for slot in slots]

# Exactly 6 distinct students give reports
solver.add(Distinct(assigned_students))
for day in days:
    for slot in slots:
        # Each slot must be assigned a student from the list
        solver.add(Or([assignment[day][slot] == student for student in students]))

# Constraints from the problem statement

# 1. Tuesday is the only day on which George can give a report.
solver.add(Or(
    assignment["Tuesday"]["Morning"] == "George",
    assignment["Tuesday"]["Afternoon"] == "George"
))
solver.add(And(
    assignment["Monday"]["Morning"] != "George",
    assignment["Monday"]["Afternoon"] != "George",
    assignment["Wednesday"]["Morning"] != "George",
    assignment["Wednesday"]["Afternoon"] != "George"
))

# 2. Neither Olivia nor Robert can give an afternoon report.
for day in days:
    solver.add(assignment[day]["Afternoon"] != "Olivia")
    solver.add(assignment[day]["Afternoon"] != "Robert")

# 3. If Nina gives a report, then on the next day Helen and Irving must both give reports,
#    unless Nina's report is given on Wednesday.
# We need to handle the "next day" logic carefully.
# For each day except Wednesday, if Nina is assigned that day, then the next day must have both Helen and Irving.
for i, day in enumerate(days[:-1]):
    next_day = days[i+1]
    # If Nina is assigned on this day (either slot), then next day must have both Helen and Irving in some slots.
    solver.add(Implies(
        Or(
            assignment[day]["Morning"] == "Nina",
            assignment[day]["Afternoon"] == "Nina"
        ),
        And(
            Or(
                assignment[next_day]["Morning"] == "Helen",
                assignment[next_day]["Afternoon"] == "Helen"
            ),
            Or(
                assignment[next_day]["Morning"] == "Irving",
                assignment[next_day]["Afternoon"] == "Irving"
            )
        )
    ))

# Additional constraint: Nina's report on Wednesday does not require the next day (since there is none).
# This is already handled by the loop above (only days[:-1] are considered).

# Given conditions for the question:
# Kyle gives the afternoon report on Tuesday
solver.add(assignment["Tuesday"]["Afternoon"] == "Kyle")

# Helen gives the afternoon report on Wednesday
solver.add(assignment["Wednesday"]["Afternoon"] == "Helen")

# Now, evaluate the multiple choice options for the morning reports on Monday, Tuesday, and Wednesday.
# We will check each option to see if it is consistent with the constraints.

# Define the options as constraints on the morning assignments.
# Each option is a tuple: (Monday Morning, Tuesday Morning, Wednesday Morning)
options = {
    "A": ("Irving", "Lenore", "Nina"),
    "B": ("Lenore", "George", "Irving"),
    "C": ("Nina", "Irving", "Lenore"),
    "D": ("Robert", "George", "Irving"),
    "E": ("Robert", "Irving", "Lenore"),
}

found_options = []
for letter, (mon_morning, tue_morning, wed_morning) in options.items():
    solver.push()
    # Constrain the morning assignments for this option
    solver.add(assignment["Monday"]["Morning"] == mon_morning)
    solver.add(assignment["Tuesday"]["Morning"] == tue_morning)
    solver.add(assignment["Wednesday"]["Morning"] == wed_morning)
    
    # Check if this option is consistent
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