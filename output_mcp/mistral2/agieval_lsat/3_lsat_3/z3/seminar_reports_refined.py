from z3 import *

solver = Solver()

# Entities and domains
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Decision variables:
# student_day[student] = day assigned (as a String)
# student_slot[student] = slot assigned (as a String)
student_day = {s: String(f"day_{s}") for s in students}
student_slot = {s: String(f"slot_{s}") for s in students}

# Helper function to get the next day as a Z3 expression
def next_day_expr(current_day):
    return If(current_day == "Monday", "Tuesday",
              If(current_day == "Tuesday", "Wednesday",
                 "Monday"))

# Constraints

# Exactly six students give reports
solver.add(Sum([1 for s in students]) == 6)

# Tuesday is the only day George can give a report
solver.add(student_day["George"] == "Tuesday")

# Neither Olivia nor Robert can give an afternoon report
solver.add(student_slot["Olivia"] != "Afternoon")
solver.add(student_slot["Robert"] != "Afternoon")

# If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# We encode this as:
# For all days d:
#   If Nina is assigned to d and d != Wednesday, then Helen and Irving are both assigned to next_day(d).
for d in days:
    solver.add(
        Implies(
            And(student_day["Nina"] == d, d != "Wednesday"),
            And(student_day["Helen"] == next_day_expr(d), 
                student_day["Irving"] == next_day_expr(d))
        )
    )

# Each day has exactly two students
for d in days:
    solver.add(Sum([If(student_day[s] == d, 1, 0) for s in students]) == 2)

# Each student is assigned to exactly one slot
for s in students:
    solver.add(Or([student_slot[s] == slot for slot in slots]))

# Each slot per day has exactly one student
for d in days:
    for slot in slots:
        solver.add(Sum([If(And(student_day[s] == d, student_slot[s] == slot), 1, 0) for s in students]) == 1)

# Now, evaluate the multiple choice options.
found_options = []

# Option A: George and Lenore
solver.push()
solver.add(student_day["George"] == student_day["Lenore"])
# Check if it is possible for George and Lenore to be assigned to a day other than Wednesday
solver.push()
solver.add(student_day["George"] != "Wednesday")
res = solver.check()
if res == unsat:
    # This means George and Lenore cannot be assigned to a day other than Wednesday if they are assigned to the same day
    found_options.append("A")
solver.pop()
solver.pop()

# Option B: Helen and Nina
solver.push()
solver.add(student_day["Helen"] == student_day["Nina"])
# Check if it is possible for Helen and Nina to be assigned to a day other than Wednesday
solver.push()
solver.add(student_day["Helen"] != "Wednesday")
res = solver.check()
if res == unsat:
    # This means Helen and Nina cannot be assigned to a day other than Wednesday if they are assigned to the same day
    found_options.append("B")
solver.pop()
solver.pop()

# Option C: Irving and Robert
solver.push()
solver.add(student_day["Irving"] == student_day["Robert"])
# Check if it is possible for Irving and Robert to be assigned to a day other than Wednesday
solver.push()
solver.add(student_day["Irving"] != "Wednesday")
res = solver.check()
if res == unsat:
    # This means Irving and Robert cannot be assigned to a day other than Wednesday if they are assigned to the same day
    found_options.append("C")
solver.pop()
solver.pop()

# Option D: Kyle and Nina
solver.push()
solver.add(student_day["Kyle"] == student_day["Nina"])
# Check if it is possible for Kyle and Nina to be assigned to a day other than Wednesday
solver.push()
solver.add(student_day["Kyle"] != "Wednesday")
res = solver.check()
if res == unsat:
    # This means Kyle and Nina cannot be assigned to a day other than Wednesday if they are assigned to the same day
    found_options.append("D")
solver.pop()
solver.pop()

# Option E: Olivia and Kyle
solver.push()
solver.add(student_day["Olivia"] == student_day["Kyle"])
# Check if it is possible for Olivia and Kyle to be assigned to a day other than Wednesday
solver.push()
solver.add(student_day["Olivia"] != "Wednesday")
res = solver.check()
if res == unsat:
    # This means Olivia and Kyle cannot be assigned to a day other than Wednesday if they are assigned to the same day
    found_options.append("E")
solver.pop()
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