from z3 import *

solver = Solver()

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
# Slots: 0=Mon_AM, 1=Mon_PM, 2=Tue_AM, 3=Tue_PM, 4=Wed_AM, 5=Wed_PM, -1=not reporting
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
slot = [Int(f'slot_{s}') for s in students]

# Each student either gets a slot 0-5 or -1 (not reporting)
for i in range(8):
    solver.add(Or(slot[i] == -1, And(slot[i] >= 0, slot[i] <= 5)))

# Exactly 6 students report
solver.add(Sum([If(slot[i] != -1, 1, 0) for i in range(8)]) == 6)

# All reporting students have distinct slots
for i in range(8):
    for j in range(i+1, 8):
        solver.add(Implies(And(slot[i] != -1, slot[j] != -1), slot[i] != slot[j]))

# Exactly 2 reports per day (1 AM, 1 PM)
for day in range(3):
    am_slot = day * 2
    pm_slot = day * 2 + 1
    solver.add(Sum([If(slot[i] == am_slot, 1, 0) for i in range(8)]) == 1)
    solver.add(Sum([If(slot[i] == pm_slot, 1, 0) for i in range(8)]) == 1)

# Constraint 1: George can only report on Tuesday (slot 2 or 3)
solver.add(Implies(slot[0] != -1, Or(slot[0] == 2, slot[0] == 3)))

# Constraint 2: Olivia and Robert cannot give afternoon reports (slots 1, 3, 5)
for idx in [6, 7]:  # Olivia, Robert
    solver.add(Implies(slot[idx] != -1, Or(slot[idx] == 0, slot[idx] == 2, slot[idx] == 4)))

# Constraint 3: If Nina reports and not on Wednesday, next day Helen and Irving both report
# Nina on Monday (slot 0 or 1) -> Tuesday Helen and Irving both report
# Nina on Tuesday (slot 2 or 3) -> Wednesday Helen and Irving both report
nina_on_monday = And(slot[5] != -1, Or(slot[5] == 0, slot[5] == 1))
nina_on_tuesday = And(slot[5] != -1, Or(slot[5] == 2, slot[5] == 3))

# Helen reports on Tuesday means slot[1] == 2 or 3
helen_on_tuesday = And(slot[1] != -1, Or(slot[1] == 2, slot[1] == 3))
irving_on_tuesday = And(slot[2] != -1, Or(slot[2] == 2, slot[2] == 3))

# Helen reports on Wednesday means slot[1] == 4 or 5
helen_on_wednesday = And(slot[1] != -1, Or(slot[1] == 4, slot[1] == 5))
irving_on_wednesday = And(slot[2] != -1, Or(slot[2] == 4, slot[2] == 5))

solver.add(Implies(nina_on_monday, And(helen_on_tuesday, irving_on_tuesday)))
solver.add(Implies(nina_on_tuesday, And(helen_on_wednesday, irving_on_wednesday)))

# Additional condition: Helen, Kyle, Lenore give the three morning reports (slots 0, 2, 4)
morning_slots = [0, 2, 4]
# Helen, Kyle, Lenore (indices 1, 3, 4) each get a morning slot
for idx in [1, 3, 4]:
    solver.add(Or(slot[idx] == 0, slot[idx] == 2, slot[idx] == 4))
# They are all distinct
solver.add(Distinct(slot[1], slot[3], slot[4]))

# Now evaluate answer choices
# (A) Helen gives a report on Monday -> slot[1] == 0 (Mon_AM, since morning only)
# (B) Irving gives a report on Monday -> slot[2] == 0 or slot[2] == 1
# (C) Irving gives a report on Wednesday -> slot[2] == 4 or slot[2] == 5
# (D) Kyle gives a report on Tuesday -> slot[3] == 2 (Tue_AM, since morning only)
# (E) Kyle gives a report on Wednesday -> slot[3] == 4 (Wed_AM, since morning only)

opt_a = (slot[1] == 0)  # Helen on Monday (Mon_AM)
opt_b = Or(slot[2] == 0, slot[2] == 1)  # Irving on Monday
opt_c = Or(slot[2] == 4, slot[2] == 5)  # Irving on Wednesday
opt_d = (slot[3] == 2)  # Kyle on Tuesday (Tue_AM)
opt_e = (slot[3] == 4)  # Kyle on Wednesday (Wed_AM)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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

# Also print the full solution for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nFull assignment:")
    for i, name in enumerate(students):
        val = m[slot[i]]
        slot_names = {-1: "Not reporting", 0: "Mon_AM", 1: "Mon_PM", 2: "Tue_AM", 3: "Tue_PM", 4: "Wed_AM", 5: "Wed_PM"}
        print(f"  {name}: {slot_names[int(str(val))]}")
solver.pop()