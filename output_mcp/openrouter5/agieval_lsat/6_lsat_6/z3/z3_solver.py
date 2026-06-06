from z3 import *

# Let me rethink. The problem says "exactly six will give individual oral reports"
# So 2 students don't give any report.
# Days: Monday, Tuesday, Wednesday
# Times: morning, afternoon
# Exactly two reports each day - one morning, one afternoon.

# Let me use a different encoding. I'll assign each student either a slot or "no report".
# Slots: 0=MonAM, 1=MonPM, 2=TueAM, 3=TuePM, 4=WedAM, 5=WedPM

students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
s_idx = {name: i for i, name in enumerate(students)}

# Each slot gets a student index (0..7)
slots = [Int(f"slot_{i}") for i in range(6)]

solver = Solver()

# Domain
for i in range(6):
    solver.add(slots[i] >= 0, slots[i] <= 7)

# All slots distinct
solver.add(Distinct(slots))

# Condition 1: Tuesday is the only day on which George can give a report.
# George can only be in TueAM(2) or TuePM(3). Not in Mon or Wed slots.
for slot_idx in [0, 1, 4, 5]:
    solver.add(slots[slot_idx] != s_idx["George"])

# Condition 2: Neither Olivia nor Robert can give an afternoon report.
# Afternoon slots: MonPM(1), TuePM(3), WedPM(5)
for name in ["Olivia", "Robert"]:
    for slot_idx in [1, 3, 5]:
        solver.add(slots[slot_idx] != s_idx[name])

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
# Nina in Monday -> Helen and Irving on Tuesday
nina_mon = Or([slots[i] == s_idx["Nina"] for i in [0, 1]])
helen_tue = Or([slots[i] == s_idx["Helen"] for i in [2, 3]])
irving_tue = Or([slots[i] == s_idx["Irving"] for i in [2, 3]])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# Nina in Tuesday -> Helen and Irving on Wednesday
nina_tue = Or([slots[i] == s_idx["Nina"] for i in [2, 3]])
helen_wed = Or([slots[i] == s_idx["Helen"] for i in [4, 5]])
irving_wed = Or([slots[i] == s_idx["Irving"] for i in [4, 5]])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Question condition: Helen, Kyle, and Lenore give the three morning reports.
# Morning slots: MonAM(0), TueAM(2), WedAM(4)
# So Helen, Kyle, Lenore are in slots 0, 2, 4 (in some order)
morning_students = [s_idx["Helen"], s_idx["Kyle"], s_idx["Lenore"]]
# The three morning slots are occupied by these three students
solver.add(Distinct([slots[0], slots[2], slots[4]]))
for ms in [0, 2, 4]:
    solver.add(Or([slots[ms] == s for s in morning_students]))
for s in morning_students:
    solver.add(Or([slots[ms] == s for ms in [0, 2, 4]]))

# Let me first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    slot_names = ["MonAM", "MonPM", "TueAM", "TuePM", "WedAM", "WedPM"]
    for i in range(6):
        val = m[slots[i]].as_long()
        print(f"  {slot_names[i]}: {students[val]}")
else:
    print("Base constraints unsatisfiable!")
    exit()

# Now evaluate each option
# Option A: Helen gives a report on Monday.
# Since Helen is a morning reporter, this means Helen is in MonAM(0)
opt_a = (slots[0] == s_idx["Helen"])

# Option B: Irving gives a report on Monday.
# Irving could be in MonAM(0) or MonPM(1). But MonAM is taken by Helen/Kyle/Lenore.
# So Irving would be in MonPM(1).
opt_b = Or([slots[i] == s_idx["Irving"] for i in [0, 1]])

# Option C: Irving gives a report on Wednesday.
opt_c = Or([slots[i] == s_idx["Irving"] for i in [4, 5]])

# Option D: Kyle gives a report on Tuesday.
# Kyle is a morning reporter, so TueAM(2).
opt_d = (slots[2] == s_idx["Kyle"])

# Option E: Kyle gives a report on Wednesday.
# Kyle is a morning reporter, so WedAM(4).
opt_e = (slots[4] == s_idx["Kyle"])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")