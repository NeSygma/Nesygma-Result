from z3 import *

# Students: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
names = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
N = 8

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=morning, 1=afternoon
# report[d][s] = student giving report on day d, slot s
report = [[Int(f"report_{d}_{s}") for s in range(2)] for d in range(3)]

solver = Solver()

# Each report slot is assigned a student 0..7
for d in range(3):
    for s in range(2):
        solver.add(report[d][s] >= 0, report[d][s] < N)

# Exactly 6 students give reports (2 per day, 3 days = 6 slots, all distinct)
solver.add(Distinct([report[d][s] for d in range(3) for s in range(2)]))

# Kyle (3) and Lenore (4) do NOT give reports
for d in range(3):
    for s in range(2):
        solver.add(report[d][s] != 3)
        solver.add(report[d][s] != 4)

# Condition 1: Tuesday is the only day George can give a report
# George (0) can only appear on Tuesday (day 1)
for s in range(2):
    solver.add(report[0][s] != 0)  # Not Monday
    solver.add(report[2][s] != 0)  # Not Wednesday

# Condition 2: Neither Olivia (6) nor Robert (7) can give an afternoon report
for d in range(3):
    solver.add(report[d][1] != 6)
    solver.add(report[d][1] != 7)

# Condition 3: If Nina (5) gives a report on day d (not Wednesday),
# then on day d+1, both Helen (1) and Irving (2) must give reports.
# "unless Nina's report is given on Wednesday" means if Nina reports on Wednesday, no constraint.

# For each day d in {0,1} (Monday, Tuesday):
# If Nina appears on day d, then Helen and Irving must both appear on day d+1
for d in range(2):
    nina_on_d = Or(report[d][0] == 5, report[d][1] == 5)
    helen_on_d1 = Or(report[d+1][0] == 1, report[d+1][1] == 1)
    irving_on_d1 = Or(report[d+1][0] == 2, report[d+1][1] == 2)
    solver.add(Implies(nina_on_d, And(helen_on_d1, irving_on_d1)))

# Now evaluate each answer choice for morning reports (slot 0) on Mon, Tue, Wed
# (A) Helen(1), George(0), Nina(5)
# (B) Irving(2), Robert(7), Helen(1)
# (C) Nina(5), Helen(1), Olivia(6)
# (D) Olivia(6), Robert(7), Irving(2)
# (E) Robert(7), George(0), Helen(1)

options = {
    "A": [1, 0, 5],
    "B": [2, 7, 1],
    "C": [5, 1, 6],
    "D": [6, 7, 2],
    "E": [7, 0, 1],
}

found_options = []
for letter, morning_vals in options.items():
    solver.push()
    # Constrain morning reports for Mon, Tue, Wed
    for d in range(3):
        solver.add(report[d][0] == morning_vals[d])
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