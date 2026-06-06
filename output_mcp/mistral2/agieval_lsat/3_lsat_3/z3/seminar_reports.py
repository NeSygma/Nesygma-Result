from z3 import *

solver = Solver()

# Entities and domains
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# Decision variables:
# student_day[student] = day assigned
# student_slot[student] = slot assigned
student_day = {s: EnumSort(f"day_{s}", days) for s in students}
student_slot = {s: EnumSort(f"slot_{s}", slots) for s in students}

# Helper functions to extract day/slot from EnumSort
# We will use the .val() method to get the actual value from the model

# Total reports per day
reports_per_day = {d: Int(f"reports_{d}") for d in days}

# Constraints

# Exactly six students give reports
solver.add(Sum([1 for s in students]) == 6)

# Exactly two reports per day (one morning, one afternoon)
for d in days:
    solver.add(reports_per_day[d] == 2)

# Tuesday is the only day George can give a report
solver.add(student_day["George"] == "Tuesday")

# Neither Olivia nor Robert can give an afternoon report
solver.add(student_slot["Olivia"] != "Afternoon")
solver.add(student_slot["Robert"] != "Afternoon")

# If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# We need to encode this as a constraint.
# Let's define a helper function to get the next day
from z3 import If, And, Or, Not, Implies

def next_day(d):
    return If(d == "Monday", "Tuesday", 
              If(d == "Tuesday", "Wednesday", "Monday"))

# For Nina, if she is assigned a day that is not Wednesday, then Helen and Irving must both give reports the next day.
# We need to ensure that if Nina is assigned to a day d != "Wednesday", then Helen and Irving are both assigned to next_day(d).
# We also need to ensure that if Nina is assigned to Wednesday, there is no constraint.

# We will encode this as:
# For all days d:
#   If Nina is assigned to d and d != "Wednesday", then Helen and Irving are both assigned to next_day(d).
for d in days:
    solver.add(
        Implies(
            And(student_day["Nina"] == d, d != "Wednesday"),
            And(student_day["Helen"] == next_day(d), student_day["Irving"] == next_day(d))
        )
    )

# Base constraints for the number of reports per day
# We need to ensure that exactly two students are assigned to each day.
# We will use a list of booleans for each day to track which students are assigned to it.
assigned_to_day = {d: [Bool(f"assigned_{s}_{d}") for s in students] for d in days}

# Each student is assigned to exactly one day
for s in students:
    solver.add(Or([student_day[s] == d for d in days]))
    solver.add(Sum([1 if s_ == s else 0 for s_ in students]) == 1)  # Ensure each student is assigned to exactly one day

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

# Now, we need to evaluate the multiple choice options.
# The question asks: Which one of the following is a pair of students who, if they give reports on the same day as each other, must give reports on Wednesday?

# We will test each option to see if it is possible for the pair to be assigned to the same day, and if so, whether that day must be Wednesday.

# For each option, we will:
# 1. Constrain the pair to be assigned to the same day.
# 2. Check if the solver can find a model where the pair is assigned to a day other than Wednesday.
# 3. If the solver cannot find such a model (i.e., unsat), then the pair must be assigned to Wednesday if they are assigned to the same day.

# We will use the following logic:
# For each option (A, B, C, D, E), we will:
#   - Constrain the pair to be assigned to the same day.
#   - Check if there exists a model where the pair is assigned to a day other than Wednesday.
#   - If no such model exists (unsat), then the pair must be assigned to Wednesday if they are assigned to the same day.

# We will then check if exactly one option satisfies this condition.

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