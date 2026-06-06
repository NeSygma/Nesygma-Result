from z3 import *

solver = Solver()

# Students: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
N = 8

# Time slots: Mon_morning=0, Mon_afternoon=1, Tue_morning=2, Tue_afternoon=3, Wed_morning=4, Wed_afternoon=5
slot_names = ["Mon_morning", "Mon_afternoon", "Tue_morning", "Tue_afternoon", "Wed_morning", "Wed_afternoon"]
slots = [Int(f'slot_{i}') for i in range(6)]

# Each slot assigned a student 0-7
for s in slots:
    solver.add(s >= 0, s < N)

# Exactly 6 distinct students (2 don't report) - all 6 slots must be different
solver.add(Distinct(slots))

# Given constraints:
# Kyle gives afternoon report on Tuesday (slot 3)
solver.add(slots[3] == 3)  # Kyle

# Helen gives afternoon report on Wednesday (slot 5)
solver.add(slots[5] == 1)  # Helen

# Condition 1: Tuesday is the only day George can give a report
# George can only be in slot 2 (Tue_morning) or slot 3 (Tue_afternoon), or not report
# So George cannot be in slots 0,1,4,5
solver.add(slots[0] != 0)  # George not Mon morning
solver.add(slots[1] != 0)  # George not Mon afternoon
solver.add(slots[4] != 0)  # George not Wed morning
solver.add(slots[5] != 0)  # George not Wed afternoon (already ensured by Helen)

# Condition 2: Neither Olivia nor Robert can give an afternoon report
# Afternoon slots: 1 (Mon), 3 (Tue), 5 (Wed)
# Olivia=6, Robert=7
for afternoon_slot in [1, 3, 5]:
    solver.add(slots[afternoon_slot] != 6)  # Olivia
    solver.add(slots[afternoon_slot] != 7)  # Robert

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina=5, Helen=1, Irving=2

# If Nina on Monday (slot 0): Tuesday must have both Helen and Irving
# Tuesday slots are 2 and 3. slot[3]=Kyle already. So Helen or Irving must be slot[2].
# But we need BOTH Helen and Irving on Tuesday. slot[3]=Kyle, so only slot[2] is available.
# That means we can't have both Helen and Irving on Tuesday if Kyle is already there.
# So Nina CANNOT be on Monday.

# If Nina on Tuesday (slot 2 or 3): Wednesday must have both Helen and Irving
# Wednesday slots are 4 and 5. slot[5]=Helen. So Irving must be slot[4].
# solver.add(Implies(slots[2] == 5, And(Or(slots[4] == 2, slots[5] == 2), Or(slots[4] == 1, slots[5] == 1))))
# Actually let me be more precise.

# Nina on Monday → both Helen and Irving on Tuesday
# Tuesday has slots 2 and 3. slot[3]=Kyle. So we need Helen AND Irving in {slot[2], slot[3]}.
# But slot[3]=Kyle, so only slot[2] can be Helen or Irving. Can't have both.
# Therefore: Nina cannot be on Monday.
solver.add(Implies(slots[0] == 5, And(
    Or(slots[2] == 1, slots[3] == 1),  # Helen on Tuesday
    Or(slots[2] == 2, slots[3] == 2)   # Irving on Tuesday
)))

# Nina on Tuesday → both Helen and Irving on Wednesday
# Wednesday has slots 4 and 5. slot[5]=Helen. So Irving must be slot[4].
solver.add(Implies(Or(slots[2] == 5, slots[3] == 5), And(
    Or(slots[4] == 1, slots[5] == 1),  # Helen on Wednesday
    Or(slots[4] == 2, slots[5] == 2)   # Irving on Wednesday
)))

# Nina on Wednesday → no constraint (already handled by not triggering the above)

# Now test each option for morning reports (Mon_morning, Tue_morning, Wed_morning) = (slot[0], slot[2], slot[4])

options = {
    "A": (2, 4, 5),   # Irving, Lenore, Nina
    "B": (4, 0, 2),   # Lenore, George, Irving
    "C": (5, 2, 4),   # Nina, Irving, Lenore
    "D": (7, 0, 2),   # Robert, George, Irving
    "E": (7, 2, 4),   # Robert, Irving, Lenore
}

found_options = []
for letter, (mon_m, tue_m, wed_m) in options.items():
    solver.push()
    solver.add(slots[0] == mon_m)
    solver.add(slots[2] == tue_m)
    solver.add(slots[4] == wed_m)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT:")
        for i in range(6):
            print(f"  {slot_names[i]} = {students[m[slots[i]].as_long()]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")