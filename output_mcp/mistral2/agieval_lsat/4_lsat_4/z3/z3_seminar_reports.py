from z3 import *

solver = Solver()

# Entities and days
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Total reports: 6 out of 8 students
# Exactly 2 reports per day (one morning, one afternoon)
# George can only report on Tuesday
# Olivia and Robert cannot give afternoon reports
# If Nina reports, then on the next day Helen and Irving must both report, unless Nina's report is on Wednesday

# Decision variables:
# student_day[student] = day assigned (or "None" if not assigned)
# student_slot[student] = slot assigned (or "None" if not assigned)

# We will model assignments as:
# For each student, assign a day and a slot, or leave unassigned.
# Since exactly 6 students report, 2 do not.

# Use Int to represent day and slot assignments for each student
# Days: Monday=0, Tuesday=1, Wednesday=2
# Slots: Morning=0, Afternoon=1
# Unassigned: -1

student_day = {s: Int(f"day_{s}") for s in students}
student_slot = {s: Int(f"slot_{s}") for s in students}

# Helper: day_to_int and slot_to_int
# Monday=0, Tuesday=1, Wednesday=2
# Morning=0, Afternoon=1

# Constraints:

# 1. George can only give a report on Tuesday
solver.add(student_day["George"] == 1)

# 2. Olivia and Robert cannot give afternoon reports
solver.add(student_slot["Olivia"] != 1)
solver.add(student_slot["Robert"] != 1)

# 3. Exactly 6 students give reports (others are unassigned)
# We will enforce that exactly 6 students have day != -1
assigned_students = [s for s in students if solver.check() == sat]  # Not used directly; see below

# Instead, we will enforce that exactly 6 students have day >= 0 and <= 2
# and slot >= 0 and <= 1
# Unassigned students have day = -1 and slot = -1

# 4. Each day has exactly 2 reports (one morning, one afternoon)
for day in days:
    d = days.index(day)
    # Exactly one morning and one afternoon report on this day
    morning_reporters = [s for s in students if student_day[s] == d and student_slot[s] == 0]
    afternoon_reporters = [s for s in students if student_day[s] == d and student_slot[s] == 1]
    solver.add(Sum([If(And(student_day[s] == d, student_slot[s] == 0), 1, 0) for s in students]) == 1)
    solver.add(Sum([If(And(student_day[s] == d, student_slot[s] == 1), 1, 0) for s in students]) == 1)

# 5. If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
# We will enforce this as a constraint on assignments

# 6. George, Nina, and Robert give reports and they do so on different days from one another
solver.add(student_day["George"] != student_day["Nina"])
solver.add(student_day["George"] != student_day["Robert"])
solver.add(student_day["Nina"] != student_day["Robert"])

# 7. All assigned students have valid day and slot
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

# 8. Exactly 6 students are assigned (day != -1)
solver.add(Sum([If(student_day[s] >= 0, 1, 0) for s in students]) == 6)

# 9. Nina's constraint: If Nina reports (day != -1), then on the next day Helen and Irving must both report, unless Nina's report is on Wednesday
# We will enforce this as a constraint
nina_day = student_day["Nina"]
helen_day = student_day["Helen"]
irving_day = student_day["Irving"]

# If Nina is assigned and not on Wednesday, then Helen and Irving must both be assigned on the next day
for d in [0, 1]:  # Monday or Tuesday
    solver.add(Implies(
        And(nina_day == d, nina_day != -1),
        And(
            helen_day == d + 1,
            irving_day == d + 1
        )
    ))

# If Nina is on Wednesday, no constraint
solver.add(Implies(nina_day == 2, True))

# Now, evaluate the multiple choice options under the above constraints

# Base constraints are already added above

# Define the options as constraints on assignments
# We will check each option independently

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