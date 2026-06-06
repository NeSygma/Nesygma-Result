from z3 import *

solver = Solver()

# Students: George=0, Helen=1, Irving=2, Nina=3, Olivia=4, Robert=5
# (Kyle and Lenore excluded per the question)
# Days: Mon=0, Tue=1, Wed=2
# Periods: am=0, pm=1

# slot[d][p] = student index (0-5)
slot = [[Int(f"slot_{d}_{p}") for p in range(2)] for d in range(3)]

# Each slot must be assigned a student from 0-5
for d in range(3):
    for p in range(2):
        solver.add(slot[d][p] >= 0, slot[d][p] <= 5)

# All 6 slots must have distinct students (each student gives exactly one report)
all_slots = [slot[d][p] for d in range(3) for p in range(2)]
solver.add(Distinct(all_slots))

# Constraint 1: George (0) can only be on Tuesday (day 1)
for d in range(3):
    for p in range(2):
        if d != 1:
            solver.add(slot[d][p] != 0)

# Constraint 2: Olivia (4) cannot give an afternoon report (p=1)
for d in range(3):
    solver.add(slot[d][1] != 4)

# Constraint 3: Robert (5) cannot give an afternoon report (p=1)
for d in range(3):
    solver.add(slot[d][1] != 5)

# Constraint 4: If Nina (3) gives a report on day d, then on day d+1
# Helen (1) and Irving (2) must both give reports, unless Nina's report is on Wednesday.
# If Nina on Monday -> Tuesday must have both Helen and Irving
nina_on_mon = Or(slot[0][0] == 3, slot[0][1] == 3)
tue_has_helen = Or(slot[1][0] == 1, slot[1][1] == 1)
tue_has_irving = Or(slot[1][0] == 2, slot[1][1] == 2)
solver.add(Implies(nina_on_mon, And(tue_has_helen, tue_has_irving)))

# If Nina on Tuesday -> Wednesday must have both Helen and Irving
nina_on_tue = Or(slot[1][0] == 3, slot[1][1] == 3)
wed_has_helen = Or(slot[2][0] == 1, slot[2][1] == 1)
wed_has_irving = Or(slot[2][0] == 2, slot[2][1] == 2)
solver.add(Implies(nina_on_tue, And(wed_has_helen, wed_has_irving)))

# Answer choices: (Mon-morning, Tue-morning, Wed-morning) as student indices
# A: Helen(1), George(0), Nina(3)
# B: Irving(2), Robert(5), Helen(1)
# C: Nina(3), Helen(1), Olivia(4)
# D: Olivia(4), Robert(5), Irving(2)
# E: Robert(5), George(0), Helen(1)

choices = {
    "A": (1, 0, 3),
    "B": (2, 5, 1),
    "C": (3, 1, 4),
    "D": (4, 5, 2),
    "E": (5, 0, 1),
}

found_options = []
for letter, (mon_am, tue_am, wed_am) in choices.items():
    solver.push()
    solver.add(slot[0][0] == mon_am)
    solver.add(slot[1][0] == tue_am)
    solver.add(slot[2][0] == wed_am)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for d in range(3):
            for p in range(2):
                print(f"  Day {d} Period {p}: student {m[slot[d][p]]}")
    else:
        print(f"Option {letter} is {result}")
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