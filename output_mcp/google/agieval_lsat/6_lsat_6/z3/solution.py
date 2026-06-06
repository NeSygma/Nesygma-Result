from z3 import *

# Students
students = ['G', 'H', 'I', 'K', 'L', 'N', 'O', 'R']
# Slots: 0:Mon-AM, 1:Mon-PM, 2:Tue-AM, 3:Tue-PM, 4:Wed-AM, 5:Wed-PM
slots = range(6)

# Variables: slot_to_student[s] = student_id (0-7) or 8 if empty
# Actually, let's use a function: student_in_slot[s] = student_id
# student_id: 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R
# 8: None
slot_to_student = [Int(f'slot_{s}') for s in slots]

solver = Solver()

# Each slot has exactly one student
for s in slots:
    solver.add(slot_to_student[s] >= 0, slot_to_student[s] <= 7)

# Each student appears at most once
for i in range(8):
    solver.add(Sum([If(slot_to_student[s] == i, 1, 0) for s in slots]) <= 1)

# Exactly 6 students give reports
solver.add(Sum([If(slot_to_student[s] < 8, 1, 0) for s in slots]) == 6)

# C1: Tuesday is the only day George can give a report.
# G is 0.
for s in slots:
    if s != 2 and s != 3:
        solver.add(slot_to_student[s] != 0)

# C2: Neither Olivia (6) nor Robert (7) can give an afternoon report (1, 3, 5).
for s in [1, 3, 5]:
    solver.add(slot_to_student[s] != 6)
    solver.add(slot_to_student[s] != 7)

# C3: If Nina (5) gives a report, then on the next day Helen (1) and Irving (2) must both give reports, unless Nina's report is given on Wednesday.
# Nina in Mon (0, 1) -> H and I in Tue (2, 3)
# Nina in Tue (2, 3) -> H and I in Wed (4, 5)
# Nina in Wed (4, 5) -> no restriction
n_in_mon = Or(slot_to_student[0] == 5, slot_to_student[1] == 5)
n_in_tue = Or(slot_to_student[2] == 5, slot_to_student[3] == 5)
h_in_tue = Or(slot_to_student[2] == 1, slot_to_student[3] == 1)
i_in_tue = Or(slot_to_student[2] == 2, slot_to_student[3] == 2)
h_in_wed = Or(slot_to_student[4] == 1, slot_to_student[5] == 1)
i_in_wed = Or(slot_to_student[4] == 2, slot_to_student[5] == 2)

solver.add(Implies(n_in_mon, And(h_in_tue, i_in_tue)))
solver.add(Implies(n_in_tue, And(h_in_wed, i_in_wed)))

# Q: If Helen (1), Kyle (3), and Lenore (4) give the three morning reports (0, 2, 4).
# {H, K, L} = {slot_0, slot_2, slot_4}
morning_slots = [0, 2, 4]
morning_students = [slot_to_student[s] for s in morning_slots]
solver.add(Or(
    And(slot_to_student[0] == 1, slot_to_student[2] == 3, slot_to_student[4] == 4),
    And(slot_to_student[0] == 1, slot_to_student[2] == 4, slot_to_student[4] == 3),
    And(slot_to_student[0] == 3, slot_to_student[2] == 1, slot_to_student[4] == 4),
    And(slot_to_student[0] == 3, slot_to_student[2] == 4, slot_to_student[4] == 1),
    And(slot_to_student[0] == 4, slot_to_student[2] == 1, slot_to_student[4] == 3),
    And(slot_to_student[0] == 4, slot_to_student[2] == 3, slot_to_student[4] == 1)
))

# Answer Choices
# (A) Helen gives a report on Monday. (slot_0 == 1 or slot_1 == 1)
# (B) Irving gives a report on Monday. (slot_0 == 2 or slot_1 == 2)
# (C) Irving gives a report on Wednesday. (slot_4 == 2 or slot_5 == 2)
# (D) Kyle gives a report on Tuesday. (slot_2 == 3 or slot_3 == 3)
# (E) Kyle gives a report on Wednesday. (slot_4 == 3 or slot_5 == 3)

options = [
    ("A", Or(slot_to_student[0] == 1, slot_to_student[1] == 1)),
    ("B", Or(slot_to_student[0] == 2, slot_to_student[1] == 2)),
    ("C", Or(slot_to_student[4] == 2, slot_to_student[5] == 2)),
    ("D", Or(slot_to_student[2] == 3, slot_to_student[3] == 3)),
    ("E", Or(slot_to_student[4] == 3, slot_to_student[5] == 3))
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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