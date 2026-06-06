from z3 import *

# Declare students and days
students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
shifts = ["first", "second"]

# Create a 3D array: student x day x shift
# Each entry is a Bool indicating if the student works that shift on that day
works = [[[Bool(f"{s}_{d}_{sh}") for sh in shifts] for d in days] for s in students]

# Helper: No student works both shifts of any day
solver = Solver()
for s_idx, s in enumerate(students):
    for d_idx, d in enumerate(days):
        solver.add(Not(And(works[s_idx][d_idx][0], works[s_idx][d_idx][1])))

# Each student works exactly two shifts
for s_idx, s in enumerate(students):
    solver.add(Sum([If(works[s_idx][d_idx][sh_idx], 1, 0) for d_idx, d in enumerate(days) for sh_idx, sh in enumerate(shifts)]) == 2)

# Each shift is worked by exactly one student
for d_idx, d in enumerate(days):
    for sh_idx, sh in enumerate(shifts):
        solver.add(Sum([If(works[s_idx][d_idx][sh_idx], 1, 0) for s_idx, s in enumerate(students)]) == 1)

# Katya works on Tuesday and Friday
solver.add(Or(works[students.index("Katya")][days.index("Tuesday")][0], works[students.index("Katya")][days.index("Tuesday")][1]))
solver.add(Or(works[students.index("Katya")][days.index("Friday")][0], works[students.index("Katya")][days.index("Friday")][1]))

# Katya works the second shift on Tuesday (given in the question)
solver.add(works[students.index("Katya")][days.index("Tuesday")][1])

# On two consecutive days, Louise works the second shift
consecutive_pairs = [(days[i], days[i+1]) for i in range(len(days)-1)]
# Louise must work the second shift on exactly two consecutive days
solver.add(Sum([If(works[students.index("Louise")][days.index(d1)][1], 1, 0) for d1, d2 in consecutive_pairs]) == 2)

# On two nonconsecutive days, Grecia works the first shift
nonconsecutive_pairs = [(days[i], days[j]) for i in range(len(days)) for j in range(i+2, len(days))]
# Grecia must work the first shift on exactly two nonconsecutive days
solver.add(Sum([If(works[students.index("Grecia")][days.index(d1)][0], 1, 0) for d1, d2 in nonconsecutive_pairs]) == 2)

# Grecia and Louise never work on the same day as each other
for d_idx, d in enumerate(days):
    # If Grecia works any shift on day d, Louise does not work any shift on day d
    solver.add(Not(Or(
        And(works[students.index("Grecia")][d_idx][0], works[students.index("Louise")][d_idx][0]),
        And(works[students.index("Grecia")][d_idx][0], works[students.index("Louise")][d_idx][1]),
        And(works[students.index("Grecia")][d_idx][1], works[students.index("Louise")][d_idx][0]),
        And(works[students.index("Grecia")][d_idx][1], works[students.index("Louise")][d_idx][1])
    )))
    # Simplified: Grecia and Louise cannot both work on the same day
    solver.add(Not(Or(
        works[students.index("Grecia")][d_idx][0],
        works[students.index("Grecia")][d_idx][1]
    )) | Not(Or(
        works[students.index("Louise")][d_idx][0],
        works[students.index("Louise")][d_idx][1]
    )))

# Hakeem and Joe work on the same day as each other at least once
solver.add(Or([Or(
    And(works[students.index("Hakeem")][d_idx][0], works[students.index("Joe")][d_idx][0]),
    And(works[students.index("Hakeem")][d_idx][0], works[students.index("Joe")][d_idx][1]),
    And(works[students.index("Hakeem")][d_idx][1], works[students.index("Joe")][d_idx][0]),
    And(works[students.index("Hakeem")][d_idx][1], works[students.index("Joe")][d_idx][1])
) for d_idx, d in enumerate(days)]))

# Evaluate each option
found_options = []

# Option A: Grecia works the first shift on Monday
solver.push()
solver.add(works[students.index("Grecia")][days.index("Monday")][0])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Hakeem works the first shift on Monday
solver.push()
solver.add(works[students.index("Hakeem")][days.index("Monday")][0])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Hakeem works the second shift on Wednesday
solver.push()
solver.add(works[students.index("Hakeem")][days.index("Wednesday")][1])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Joe works the second shift on Thursday
solver.push()
solver.add(works[students.index("Joe")][days.index("Thursday")][1])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Louise works the second shift on Monday
solver.push()
solver.add(works[students.index("Louise")][days.index("Monday")][1])
if solver.check() == sat:
    found_options.append("E")
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