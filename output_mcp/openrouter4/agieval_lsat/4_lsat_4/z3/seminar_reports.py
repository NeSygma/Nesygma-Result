from z3 import *

solver = Solver()

# Students indexed: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
student_names = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
slots = [Int(s) for s in student_names]

# Domain: -1 (no report) or 0..5 (Mon AM, Mon PM, Tue AM, Tue PM, Wed AM, Wed PM)
for s in slots:
    solver.add(Or(s == -1, And(s >= 0, s <= 5)))

# Each slot 0..5 assigned to exactly one student
for s_val in range(6):
    solver.add(Sum([If(slots[i] == s_val, 1, 0) for i in range(8)]) == 1)

# Helper functions for day (0=Mon,1=Tue,2=Wed) and time (0=AM,1=PM)
def day_of(slot):
    return slot / 2  # Z3 integer division

def time_of(slot):
    return slot % 2

# Constraint 3: Tuesday is the only day George can give a report
george = 0
solver.add(Implies(slots[george] != -1, day_of(slots[george]) == 1))

# Constraint 4: Neither Olivia nor Robert can give an afternoon report
olivia = 6
robert = 7
solver.add(Implies(slots[olivia] != -1, time_of(slots[olivia]) == 0))
solver.add(Implies(slots[robert] != -1, time_of(slots[robert]) == 0))

# Constraint 5: If Nina gives a report...
nina = 5
helen = 1
irving = 2

# Nina on Monday -> Tuesday both Helen and Irving give reports
solver.add(Implies(And(slots[nina] != -1, day_of(slots[nina]) == 0),
                   And(slots[helen] != -1, day_of(slots[helen]) == 1,
                       slots[irving] != -1, day_of(slots[irving]) == 1)))

# Nina on Tuesday -> Wednesday both Helen and Irving give reports
solver.add(Implies(And(slots[nina] != -1, day_of(slots[nina]) == 1),
                   And(slots[helen] != -1, day_of(slots[helen]) == 2,
                       slots[irving] != -1, day_of(slots[irving]) == 2)))

# Additional condition from question stem: George, Nina, and Robert give reports
# and they do so on different days from one another
solver.add(slots[george] != -1)
solver.add(slots[nina] != -1)
solver.add(slots[robert] != -1)
solver.add(Distinct(day_of(slots[george]), day_of(slots[nina]), day_of(slots[robert])))

# Options
# (A) Helen gives a report on Wednesday
opt_a = And(slots[helen] != -1, day_of(slots[helen]) == 2)

# (B) Nina gives a report on Monday
opt_b = day_of(slots[nina]) == 0

# (C) Nina gives a report on Tuesday
opt_c = day_of(slots[nina]) == 1

# (D) Olivia gives a report on Monday
opt_d = And(slots[olivia] != -1, day_of(slots[olivia]) == 0)

# (E) Robert gives a report on Wednesday
opt_e = And(slots[robert] != -1, day_of(slots[robert]) == 2)

found_options = []

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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