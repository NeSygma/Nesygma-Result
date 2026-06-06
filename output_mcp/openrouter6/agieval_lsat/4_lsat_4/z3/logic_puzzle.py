from z3 import *

solver = Solver()

# Student indices
GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT = range(8)
student_names = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Variables
gives = [Bool(f'gives_{i}') for i in range(8)]
day = [Int(f'day_{i}') for i in range(8)]
time = [Int(f'time_{i}') for i in range(8)]

# Domain constraints for day and time (0..2, 0..1)
for i in range(8):
    solver.add(day[i] >= 0, day[i] <= 2)
    solver.add(time[i] >= 0, time[i] <= 1)

# Base constraints from problem statement
# 1. George, Nina, Robert give reports
solver.add(gives[GEORGE])
solver.add(gives[NINA])
solver.add(gives[ROBERT])

# 2. George only on Tuesday
solver.add(day[GEORGE] == 1)  # Tuesday

# 3. Robert only morning
solver.add(time[ROBERT] == 0)

# 4. Olivia only morning if she gives a report
solver.add(Implies(gives[OLIVIA], time[OLIVIA] == 0))

# 5. Exactly six reports, each day two reports (one morning, one afternoon)
# Count per (day, time) slot
for d in range(3):
    for t in range(2):
        count = Sum([If(And(gives[i], day[i] == d, time[i] == t), 1, 0) for i in range(8)])
        solver.add(count == 1)

# Total reports
solver.add(Sum([If(gives[i], 1, 0) for i in range(8)]) == 6)

# 6. Condition: If Nina gives a report, then next day Helen and Irving both give reports, unless Nina on Wednesday
d_nina = day[NINA]
solver.add(Implies(d_nina != 2, And(gives[HELEN], day[HELEN] == d_nina + 1,
                                    gives[IRVING], day[IRVING] == d_nina + 1)))

# 7. George, Nina, Robert on different days
solver.add(day[NINA] != day[GEORGE])  # George is Tuesday, so Nina != Tuesday
solver.add(day[ROBERT] != day[GEORGE])
solver.add(day[NINA] != day[ROBERT])

# Additional constraints to ensure distinct days (already enforced above)

# Now evaluate each option
found_options = []

# Option A: Helen gives a report on Wednesday
opt_a = And(gives[HELEN], day[HELEN] == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Nina gives a report on Monday
opt_b = (day[NINA] == 0)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Nina gives a report on Tuesday
opt_c = (day[NINA] == 1)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Olivia gives a report on Monday
opt_d = And(gives[OLIVIA], day[OLIVIA] == 0)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Robert gives a report on Wednesday
opt_e = (day[ROBERT] == 2)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")