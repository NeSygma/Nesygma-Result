from z3 import *

# Students: 0:George, 1:Helen, 2:Irving, 3:Kyle, 4:Lenore, 5:Nina, 6:Olivia, 7:Robert
# Slots: 0:MonAM, 1:MonPM, 2:TueAM, 3:TuePM, 4:WedAM, 5:WedPM
# Day: 0:Mon, 1:Tue, 2:Wed

solver = Solver()

# student_gives_report[s] = slot_id (0-5) or -1 (not giving)
s_report = [Int(f's_{i}') for i in range(8)]

for s in range(8):
    solver.add(s_report[s] >= -1, s_report[s] <= 5)

# Exactly 6 students give reports
solver.add(Sum([If(s_report[s] != -1, 1, 0) for s in range(8)]) == 6)

# Each slot has exactly one student
for slot in range(6):
    solver.add(Sum([If(s_report[s] == slot, 1, 0) for s in range(8)]) == 1)

# C1: George (0) can only give a report on Tue (slots 2, 3)
solver.add(Implies(s_report[0] != -1, Or(s_report[0] == 2, s_report[0] == 3)))

# C2: Olivia (6) and Robert (7) cannot give an afternoon report (slots 1, 3, 5)
for s in [6, 7]:
    solver.add(Implies(s_report[s] != -1, Not(Or(s_report[s] == 1, s_report[s] == 3, s_report[s] == 5))))

# C3: If Nina (5) gives a report:
# If N gives on Mon (0 or 1), then H (1) and I (2) must give on Tue (2 or 3).
# If N gives on Tue (2 or 3), then H (1) and I (2) must give on Wed (4 or 5).
# If N gives on Wed (4 or 5), no condition.
solver.add(Implies(Or(s_report[5] == 0, s_report[5] == 1), 
                   And(Or(s_report[1] == 2, s_report[1] == 3), Or(s_report[2] == 2, s_report[2] == 3))))
solver.add(Implies(Or(s_report[5] == 2, s_report[5] == 3), 
                   And(Or(s_report[1] == 4, s_report[1] == 5), Or(s_report[2] == 4, s_report[2] == 5))))

# Helper to get day from slot
def get_day_expr(slot_var):
    # slot 0,1 -> 0; 2,3 -> 1; 4,5 -> 2
    return If(slot_var <= 1, 0, If(slot_var <= 3, 1, 2))

options = [
    ("A", 0, 4),
    ("B", 1, 5),
    ("C", 2, 7),
    ("D", 3, 5),
    ("E", 6, 3)
]

valid_options = []
for label, s1, s2 in options:
    solver.push()
    # Add the negation of the condition:
    # There exists a scenario where they give reports on the same day AND that day is NOT Wednesday.
    solver.add(s_report[s1] != -1)
    solver.add(s_report[s2] != -1)
    solver.add(get_day_expr(s_report[s1]) == get_day_expr(s_report[s2]))
    solver.add(get_day_expr(s_report[s1]) != 2)
    
    if solver.check() == unsat:
        valid_options.append(label)
    solver.pop()

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")