from z3 import *

# Students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_to_int = {s: i for i, s in enumerate(students)}
int_to_student = {i: s for s, i in student_to_int.items()}

# Days and slots
days = ["Mon", "Tue", "Wed"]
slots = ["morning", "afternoon"]

# Create variables: schedule[day][slot] = student index
schedule = {}
for day in days:
    for slot in slots:
        schedule[(day, slot)] = Int(f"{day}_{slot}")

solver = Solver()

# Base constraints:
# 1. Each slot gets a student (0-7)
for day in days:
    for slot in slots:
        solver.add(schedule[(day, slot)] >= 0)
        solver.add(schedule[(day, slot)] < len(students))

# 2. Exactly 6 students give reports (2 per day, 3 days = 6 slots)
# We'll ensure all 6 slots have distinct students (no student gives two reports)
all_slots = [schedule[(day, slot)] for day in days for slot in slots]
solver.add(Distinct(all_slots))

# 3. Exactly 2 students don't give reports (implied by distinct 6 out of 8)

# Constraint 1: Tuesday is the only day George can give a report
george = student_to_int["George"]
for day in days:
    for slot in slots:
        if day != "Tue":
            solver.add(schedule[(day, slot)] != george)

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
olivia = student_to_int["Olivia"]
robert = student_to_int["Robert"]
for day in days:
    solver.add(schedule[(day, "afternoon")] != olivia)
    solver.add(schedule[(day, "afternoon")] != robert)

# Constraint 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday.
nina = student_to_int["Nina"]
helen = student_to_int["Helen"]
irving = student_to_int["Irving"]

# We need to model "next day" - for Monday, next is Tuesday; for Tuesday, next is Wednesday
# For Wednesday, no next day (condition doesn't apply)

# For each day, if Nina gives a report that day (and it's not Wednesday), then next day both Helen and Irving give reports
for day_idx, day in enumerate(days):
    if day == "Wed":
        continue  # No constraint for Wednesday
    
    next_day = days[day_idx + 1]
    
    # Check if Nina gives a report on this day
    nina_on_day = Or([schedule[(day, slot)] == nina for slot in slots])
    
    # If Nina gives a report on this day (and it's not Wednesday), then next day both Helen and Irving give reports
    # We need to ensure that on next day, both Helen and Irving are scheduled (in some slot)
    helen_on_next = Or([schedule[(next_day, slot)] == helen for slot in slots])
    irving_on_next = Or([schedule[(next_day, slot)] == irving for slot in slots])
    
    # Implication: If Nina gives a report on this day (and it's not Wednesday), then next day both Helen and Irving give reports
    solver.add(Implies(nina_on_day, And(helen_on_next, irving_on_next)))

# Now test each option
# For each option, we'll add constraints that match the schedule and check if it's consistent

# Define the options as lists of (day, slot, student) tuples
options = {
    "A": [
        ("Mon", "morning", "Helen"),
        ("Mon", "afternoon", "Robert"),
        ("Tue", "morning", "Olivia"),
        ("Tue", "afternoon", "Irving"),
        ("Wed", "morning", "Lenore"),
        ("Wed", "afternoon", "Kyle")
    ],
    "B": [
        ("Mon", "morning", "Irving"),
        ("Mon", "afternoon", "Olivia"),
        ("Tue", "morning", "Helen"),
        ("Tue", "afternoon", "Kyle"),
        ("Wed", "morning", "Nina"),
        ("Wed", "afternoon", "Lenore")
    ],
    "C": [
        ("Mon", "morning", "Lenore"),
        ("Mon", "afternoon", "Helen"),
        ("Tue", "morning", "George"),
        ("Tue", "afternoon", "Kyle"),
        ("Wed", "morning", "Robert"),
        ("Wed", "afternoon", "Irving")
    ],
    "D": [
        ("Mon", "morning", "Nina"),
        ("Mon", "afternoon", "Helen"),
        ("Tue", "morning", "Robert"),
        ("Tue", "afternoon", "Irving"),
        ("Wed", "morning", "Olivia"),
        ("Wed", "afternoon", "Lenore")
    ],
    "E": [
        ("Mon", "morning", "Olivia"),
        ("Mon", "afternoon", "Nina"),
        ("Tue", "morning", "Irving"),
        ("Tue", "afternoon", "Helen"),
        ("Wed", "morning", "Kyle"),
        ("Wed", "afternoon", "George")
    ]
}

found_options = []
for letter, assignments in options.items():
    solver.push()
    # Add constraints for this option
    for day, slot, student in assignments:
        solver.add(schedule[(day, slot)] == student_to_int[student])
    
    # Check if this option satisfies all constraints
    if solver.check() == sat:
        found_options.append(letter)
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