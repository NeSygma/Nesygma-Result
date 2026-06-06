from z3 import *

solver = Solver()

# Entities and days
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Decision variables:
# student_day[student] = day assigned (Monday=0, Tuesday=1, Wednesday=2, unassigned=-1)
# student_slot[student] = slot assigned (Morning=0, Afternoon=1, unassigned=-1)

student_day = {s: Int(f"day_{s}") for s in students}
student_slot = {s: Int(f"slot_{s}") for s in students}

# Constraints:

# 1. George can only give a report on Tuesday
solver.add(student_day["George"] == 1)

# 2. Olivia and Robert cannot give afternoon reports
solver.add(student_slot["Olivia"] != 1)
solver.add(student_slot["Robert"] != 1)

# 3. Each day has exactly 2 reports (one morning, one afternoon)
for d in range(3):  # Monday=0, Tuesday=1, Wednesday=2
    solver.add(Sum([If(And(student_day[s] == d, student_slot[s] == 0), 1, 0) for s in students]) == 1)
    solver.add(Sum([If(And(student_day[s] == d, student_slot[s] == 1), 1, 0) for s in students]) == 1)

# 4. Exactly 6 students are assigned (day != -1)
solver.add(Sum([If(student_day[s] >= 0, 1, 0) for s in students]) == 6)

# 5. All assigned students have valid day and slot
for s in students:
    solver.add(Or(
        And(student_day[s] == 0, student_slot[s] == 0),
        And(student_day[s] == 0, student_slot[s] == 1),
        And(student_day[s] == 1, student_slot[s] == 0),
        And(student_day[s] == 1, student_slot[s] == 1),
        And(student_day[s] == 2, student_slot[s] == 0),
        And(student_day[s] == 2, student_slot[s] == 1),
        And(student_day[s] == -1, student_slot[s] == -1)
    ))

# 6. George, Nina, and Robert give reports and they do so on different days from one another
solver.add(student_day["George"] != student_day["Nina"])
solver.add(student_day["George"] != student_day["Robert"])
solver.add(student_day["Nina"] != student_day["Robert"])

# 7. If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
nina_day = student_day["Nina"]
helen_day = student_day["Helen"]
irving_day = student_day["Irving"]

# If Nina is on Monday (0), Helen and Irving must be on Tuesday (1)
solver.add(Implies(nina_day == 0, And(helen_day == 1, irving_day == 1)))

# If Nina is on Tuesday (1), Helen and Irving must be on Wednesday (2)
solver.add(Implies(nina_day == 1, And(helen_day == 2, irving_day == 2)))

# If Nina is on Wednesday (2), no constraint
solver.add(Implies(nina_day == 2, True))

# 8. Nina, George, and Robert are assigned (since they give reports)
solver.add(student_day["Nina"] >= 0)
solver.add(student_day["George"] >= 0)
solver.add(student_day["Robert"] >= 0)

# Now, evaluate the multiple choice options under the above constraints

# Option A: Helen gives a report on Wednesday
opt_a_constr = (student_day["Helen"] == 2)

# Option B: Nina gives a report on Monday
opt_b_constr = (student_day["Nina"] == 0)

# Option C: Nina gives a report on Tuesday
opt_c_constr = (student_day["Nina"] == 1)

# Option D: Olivia gives a report on Monday
opt_d_constr = (student_day["Olivia"] == 0)

# Option E: Robert gives a report on Wednesday
opt_e_constr = (student_day["Robert"] == 2)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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