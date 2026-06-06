from z3 import *

# Students indexed:
# 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
# Slots: 0=MonMorn, 1=MonAft, 2=TueMorn, 3=TueAft, 4=WedMorn, 5=WedAft

# slot_student[i] = which student gives report in slot i
slot_student = [Int(f'slot_{i}') for i in range(6)]

solver = Solver()

# Each slot gets a student from 0..7
for i in range(6):
    solver.add(slot_student[i] >= 0, slot_student[i] <= 7)

# All slot assignments are distinct (each student gives at most one report)
solver.add(Distinct(slot_student))

# Fixed assignments
solver.add(slot_student[3] == 3)  # Kyle gives Tuesday afternoon
solver.add(slot_student[5] == 1)  # Helen gives Wednesday afternoon

# Condition 1: George can only be on Tuesday (slots 2 or 3)
# So George cannot be in slots 0,1,4,5
solver.add(slot_student[0] != 0)
solver.add(slot_student[1] != 0)
solver.add(slot_student[4] != 0)
solver.add(slot_student[5] != 0)

# Condition 2: Neither Olivia nor Robert can give an afternoon report
# Afternoon slots: 1 (MonAft), 3 (TueAft), 5 (WedAft)
solver.add(And(slot_student[1] != 6, slot_student[1] != 7))  # MonAft not Olivia(6) or Robert(7)
solver.add(And(slot_student[3] != 6, slot_student[3] != 7))  # TueAft not Olivia or Robert
solver.add(And(slot_student[5] != 6, slot_student[5] != 7))  # WedAft not Olivia or Robert

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina index = 5
# For each possible slot s that Nina could be in:
# If s is Monday (0 or 1), then Helen and Irving must be on Tuesday (slots 2 or 3)
# If s is Tuesday (2 or 3), then Helen and Irving must be on Wednesday (slots 4 or 5)
# If s is Wednesday (4 or 5), no condition.

# We encode this as: For each slot s, if Nina is there, then the condition for that day applies.
# Use Implies for each slot.

# Helper: day(s) = s // 2
# Monday: 0,1 -> day 0
# Tuesday: 2,3 -> day 1
# Wednesday: 4,5 -> day 2

# Nina on Monday (day 0): next day is Tuesday (day 1), slots 2,3
# Helen must be in {2,3}, Irving must be in {2,3}
nina_on_monday_condition = And(
    Or(slot_student[2] == 1, slot_student[3] == 1),  # Helen on Tuesday
    Or(slot_student[2] == 2, slot_student[3] == 2)   # Irving on Tuesday
)

# Nina on Tuesday (day 1): next day is Wednesday (day 2), slots 4,5
# Helen already fixed to slot 5, so Helen is on Wednesday automatically.
# Irving must be in {4,5}
nina_on_tuesday_condition = Or(slot_student[4] == 2, slot_student[5] == 2)  # Irving on Wednesday
# (Helen is already on Wednesday at slot 5)

# Now add implications for slots 0,1 (Monday) and 2,3 (Tuesday)
# Slot 0 (MonMorn)
solver.add(Implies(slot_student[0] == 5, nina_on_monday_condition))
# Slot 1 (MonAft)
solver.add(Implies(slot_student[1] == 5, nina_on_monday_condition))
# Slot 2 (TueMorn)
solver.add(Implies(slot_student[2] == 5, nina_on_tuesday_condition))
# Slot 3 (TueAft) - but slot 3 is Kyle (3), so Nina cannot be in slot 3. But we add anyway for completeness.
solver.add(Implies(slot_student[3] == 5, nina_on_tuesday_condition))
# Slot 4 (WedMorn) - no condition
# Slot 5 (WedAft) - slot 5 is Helen (1), so Nina cannot be in slot 5 anyway.

# Now evaluate options

# Options: list of (letter, constraint_on_morning_slots)
# morning slots: 0=MonMorn, 2=TueMorn, 4=WedMorn

options = [
    ("A", [slot_student[0] == 2, slot_student[2] == 4, slot_student[4] == 5]),  # Irving, Lenore, Nina
    ("B", [slot_student[0] == 4, slot_student[2] == 0, slot_student[4] == 2]),  # Lenore, George, Irving
    ("C", [slot_student[0] == 5, slot_student[2] == 2, slot_student[4] == 4]),  # Nina, Irving, Lenore
    ("D", [slot_student[0] == 7, slot_student[2] == 0, slot_student[4] == 2]),  # Robert, George, Irving
    ("E", [slot_student[0] == 7, slot_student[2] == 2, slot_student[4] == 4]),  # Robert, Irving, Lenore
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