from z3 import *

# Students: 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R
# Slots: 0:MonAM, 1:MonPM, 2:TueAM, 3:TuePM, 4:WedAM, 5:WedPM

solver = Solver()

# Variables: which student is in which slot
# slot_student[s] = student_id
slot_student = [Int(f'slot_{s}') for s in range(6)]

# Domain: students 0-7
for s in range(6):
    solver.add(slot_student[s] >= 0, slot_student[s] <= 7)

# Exactly 6 students give reports, K(3) and L(4) do not.
# So the students are {0, 1, 2, 5, 6, 7}
students_giving_reports = [0, 1, 2, 5, 6, 7]
solver.add(Distinct(slot_student))
for s in range(6):
    solver.add(Or([slot_student[s] == st for st in students_giving_reports]))

# C1: George (0) can only be in TueAM (2) or TuePM (3)
# George must be in one of the slots
solver.add(Or([slot_student[s] == 0 for s in range(6)]))
for s in range(6):
    if s != 2 and s != 3:
        solver.add(slot_student[s] != 0)

# C2: Olivia (6) and Robert (7) cannot give afternoon reports (1, 3, 5)
for s in [1, 3, 5]:
    solver.add(slot_student[s] != 6)
    solver.add(slot_student[s] != 7)

# C3: If Nina (5) gives a report, then on the next day Helen (1) and Irving (2) must both give reports,
# unless Nina's report is on Wednesday (4, 5).
# Nina is in the set of students giving reports, so she must be in one of the slots.
nina_slot = Int('nina_slot')
solver.add(Or([slot_student[s] == 5 for s in range(6)]))
for s in range(6):
    solver.add(Implies(slot_student[s] == 5, nina_slot == s))

# If Nina is in Mon (0, 1), then Tue (2, 3) must be H(1) and I(2)
solver.add(Implies(Or(nina_slot == 0, nina_slot == 1), 
                   And(Or(slot_student[2] == 1, slot_student[2] == 2),
                       Or(slot_student[3] == 1, slot_student[3] == 2),
                       slot_student[2] != slot_student[3])))

# If Nina is in Tue (2, 3), then Wed (4, 5) must be H(1) and I(2)
solver.add(Implies(Or(nina_slot == 2, nina_slot == 3), 
                   And(Or(slot_student[4] == 1, slot_student[4] == 2),
                       Or(slot_student[5] == 1, slot_student[5] == 2),
                       slot_student[4] != slot_student[5])))

# Options for (MonAM, TueAM, WedAM) -> (slot_student[0], slot_student[2], slot_student[4])
# A: H(1), G(0), N(5)
# B: I(2), R(7), H(1)
# C: N(5), H(1), O(6)
# D: O(6), R(7), I(2)
# E: R(7), G(0), H(1)

options = [
    ("A", [1, 0, 5]),
    ("B", [2, 7, 1]),
    ("C", [5, 1, 6]),
    ("D", [6, 7, 2]),
    ("E", [7, 0, 1])
]

found_options = []
for letter, opt in options:
    solver.push()
    solver.add(slot_student[0] == opt[0])
    solver.add(slot_student[2] == opt[1])
    solver.add(slot_student[4] == opt[2])
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