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

# Exactly 6 distinct students (2 don't report)
solver.add(Distinct(slots))

# Given: Kyle gives afternoon report on Tuesday (slot 3)
solver.add(slots[3] == 3)

# Given: Helen gives afternoon report on Wednesday (slot 5)
solver.add(slots[5] == 1)

# Condition 1: Tuesday is the only day George can give a report
# George cannot be on Monday or Wednesday
solver.add(slots[0] != 0)  # George not Mon morning
solver.add(slots[1] != 0)  # George not Mon afternoon
solver.add(slots[4] != 0)  # George not Wed morning
solver.add(slots[5] != 0)  # George not Wed afternoon (already Helen)

# Condition 2: Neither Olivia nor Robert can give an afternoon report
# Afternoon slots: 1 (Mon), 3 (Tue), 5 (Wed)
for afternoon_slot in [1, 3, 5]:
    solver.add(slots[afternoon_slot] != 6)  # Olivia
    solver.add(slots[afternoon_slot] != 7)  # Robert

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.

# Nina on Monday (morning OR afternoon) → both Helen and Irving on Tuesday
nina_on_monday = Or(slots[0] == 5, slots[1] == 5)
solver.add(Implies(nina_on_monday, And(
    Or(slots[2] == 1, slots[3] == 1),  # Helen on Tuesday
    Or(slots[2] == 2, slots[3] == 2)   # Irving on Tuesday
)))

# Nina on Tuesday (morning OR afternoon) → both Helen and Irving on Wednesday
nina_on_tuesday = Or(slots[2] == 5, slots[3] == 5)
solver.add(Implies(nina_on_tuesday, And(
    Or(slots[4] == 1, slots[5] == 1),  # Helen on Wednesday
    Or(slots[4] == 2, slots[5] == 2)   # Irving on Wednesday
)))

# Nina on Wednesday → no constraint (already handled by not triggering above)

# Test each option for morning reports (slot[0], slot[2], slot[4])
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