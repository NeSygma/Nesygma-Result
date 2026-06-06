from z3 import *

# Base constraints for the seminar schedule problem
solver = Solver()

# Students as Z3 integer constants
George = IntVal(0)
Helen = IntVal(1)
Irving = IntVal(2)
Kyle = IntVal(3)
Lenore = IntVal(4)
Nina = IntVal(5)
Olivia = IntVal(6)
Robert = IntVal(7)

# Days and slots
# Slots: Monday Morning, Monday Afternoon, Tuesday Morning, Tuesday Afternoon, Wednesday Morning, Wednesday Afternoon
slots = [
    ("Mon", "morning"),
    ("Mon", "afternoon"),
    ("Tue", "morning"),
    ("Tue", "afternoon"),
    ("Wed", "morning"),
    ("Wed", "afternoon")
]

# Decision variables: assignment of students to slots
# slot_vars[i] = student assigned to slot i
slot_vars = [Int(f"slot_{i}") for i in range(6)]

# Each slot must be assigned a student (0-7)
for i in range(6):
    solver.add(Or([slot_vars[i] == s for s in [George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert]]))

# Exactly 6 distinct students are selected (no repeats)
solver.add(Distinct(slot_vars))

# Constraint 1: George can only give a report on Tuesday
# Tuesday slots are index 2 (morning) and 3 (afternoon)
solver.add(Or([
    And(slot_vars[2] == George, slot_vars[3] != George),
    And(slot_vars[3] == George, slot_vars[2] != George),
    And(slot_vars[2] != George, slot_vars[3] != George)
]))

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
# Afternoon slots are index 1 (Mon), 3 (Tue), 5 (Wed)
for slot_idx in [1, 3, 5]:
    solver.add(Or(
        slot_vars[slot_idx] != Olivia,
        slot_vars[slot_idx] != Robert
    ))

# Constraint 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
# Helper function to get the next day's slots
slot_to_day = [
    ("Mon", "morning"),
    ("Mon", "afternoon"),
    ("Tue", "morning"),
    ("Tue", "afternoon"),
    ("Wed", "morning"),
    ("Wed", "afternoon")
]

def get_next_day_slots(day, slot_type):
    """Returns the indices of the next day's slots."""
    if day == "Mon":
        return [2, 3]  # Tuesday morning and afternoon
    elif day == "Tue":
        return [4, 5]  # Wednesday morning and afternoon
    else:
        return []  # Wednesday has no next day

# For each slot, if Nina is assigned there, enforce the constraint
for i in range(6):
    day, slot_type = slot_to_day[i]
    solver.add(Implies(
        slot_vars[i] == Nina,
        If(
            day == "Wed",
            True,  # No constraint if Nina is on Wednesday
            And(
                Or([slot_vars[j] == Helen for j in get_next_day_slots(day, slot_type)]),
                Or([slot_vars[j] == Irving for j in get_next_day_slots(day, slot_type)])
            )
        )
    ))

# Now evaluate the multiple-choice options
# We will check each option against the constraints

# Helper: Convert option schedule to constraints
# Each option is a list of tuples: (day, slot_type, student_name)

def option_constraints(option_schedule):
    """Returns a list of constraints for the given option schedule."""
    constraints = []
    student_map = {
        "George": George,
        "Helen": Helen,
        "Irving": Irving,
        "Kyle": Kyle,
        "Lenore": Lenore,
        "Nina": Nina,
        "Olivia": Olivia,
        "Robert": Robert
    }
    for (day, slot_type, student_name) in option_schedule:
        # Find the slot index
        slot_idx = None
        for i, (d, st) in enumerate(slot_to_day):
            if d == day and st == slot_type:
                slot_idx = i
                break
        if slot_idx is None:
            raise ValueError(f"Invalid slot: {day} {slot_type}")
        student_val = student_map[student_name]
        constraints.append(slot_vars[slot_idx] == student_val)
    return constraints

# Define the options as schedules
# Each option is a list of tuples: (day, slot_type, student_name)

option_A = [
    ("Mon", "morning", "Helen"),
    ("Mon", "afternoon", "Robert"),
    ("Tue", "morning", "Olivia"),
    ("Tue", "afternoon", "Irving"),
    ("Wed", "morning", "Lenore"),
    ("Wed", "afternoon", "Kyle")
]

option_B = [
    ("Mon", "morning", "Irving"),
    ("Mon", "afternoon", "Olivia"),
    ("Tue", "morning", "Helen"),
    ("Tue", "afternoon", "Kyle"),
    ("Wed", "morning", "Nina"),
    ("Wed", "afternoon", "Lenore")
]

option_C = [
    ("Mon", "morning", "Lenore"),
    ("Mon", "afternoon", "Helen"),
    ("Tue", "morning", "George"),
    ("Tue", "afternoon", "Kyle"),
    ("Wed", "morning", "Robert"),
    ("Wed", "afternoon", "Irving")
]

option_D = [
    ("Mon", "morning", "Nina"),
    ("Mon", "afternoon", "Helen"),
    ("Tue", "morning", "Robert"),
    ("Tue", "afternoon", "Irving"),
    ("Wed", "morning", "Olivia"),
    ("Wed", "afternoon", "Lenore")
]

option_E = [
    ("Mon", "morning", "Olivia"),
    ("Mon", "afternoon", "Nina"),
    ("Tue", "morning", "Irving"),
    ("Tue", "afternoon", "Helen"),
    ("Wed", "morning", "Kyle"),
    ("Wed", "afternoon", "George")
]

# Evaluate each option
found_options = []

for letter, option_schedule in [("A", option_A), ("B", option_B), ("C", option_C), ("D", option_D), ("E", option_E)]:
    solver.push()
    # Add the option's constraints
    for constr in option_constraints(option_schedule):
        solver.add(constr)
    # Check if the option satisfies all constraints
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")