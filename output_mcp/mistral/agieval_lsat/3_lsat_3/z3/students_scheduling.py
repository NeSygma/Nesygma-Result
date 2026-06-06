from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_vars = {s: Bool(f"gives_report_{s}") for s in students}

# Declare days and times
# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Times: 0=morning, 1=afternoon
day_vars = {s: Int(f"day_{s}") for s in students}
time_vars = {s: Int(f"time_{s}") for s in students}

# Solver
solver = Solver()

# Helper: Exactly 6 students give reports
solver.add(Sum([If(student_vars[s], 1, 0) for s in students]) == 6)

# Each day has exactly 2 reports (one morning, one afternoon)
for day in range(3):
    # Morning report
    solver.add(Sum([If(And(student_vars[s], day_vars[s] == day, time_vars[s] == 0), 1, 0) for s in students]) == 1)
    # Afternoon report
    solver.add(Sum([If(And(student_vars[s], day_vars[s] == day, time_vars[s] == 1), 1, 0) for s in students]) == 1)

# Constraint 1: Tuesday is the only day George can give a report
solver.add(Implies(student_vars["George"], day_vars["George"] == 1))

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(student_vars["Olivia"], time_vars["Olivia"] == 0))
solver.add(Implies(student_vars["Robert"], time_vars["Robert"] == 0))

# Constraint 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday
# We need to handle the "next day" logic carefully.
# For Nina on Monday (day 0): Helen and Irving must give reports on Tuesday (day 1)
# For Nina on Tuesday (day 1): Helen and Irving must give reports on Wednesday (day 2)
# For Nina on Wednesday (day 2): No constraint

# Helper: If Nina gives a report on day d < 2, then Helen and Irving must give reports on day d+1
solver.add(Not(And(
    student_vars["Nina"],
    day_vars["Nina"] < 2,
    Or(
        Not(Or([And(student_vars["Helen"], day_vars["Helen"] == day_vars["Nina"] + 1) for _ in [0]])),
        Not(Or([And(student_vars["Irving"], day_vars["Irving"] == day_vars["Nina"] + 1) for _ in [0]]))
    )
)))

# Ensure days and times are within bounds
for s in students:
    solver.add(day_vars[s] >= 0, day_vars[s] <= 2)
    solver.add(time_vars[s] >= 0, time_vars[s] <= 1)

# Base constraints are now fully encoded.
# Now, evaluate the multiple-choice options.
# We need to check for each option: if the pair gives reports on the same day, must it be Wednesday?

# Define the options as pairs of students
options = [
    ("A", "George", "Lenore"),
    ("B", "Helen", "Nina"),
    ("C", "Irving", "Robert"),
    ("D", "Kyle", "Nina"),
    ("E", "Olivia", "Kyle")
]

found_options = []

for letter, s1, s2 in options:
    solver.push()
    # Add constraint: s1 and s2 give reports on the same day
    solver.add(And(student_vars[s1], student_vars[s2]))
    solver.add(day_vars[s1] == day_vars[s2])
    
    # Check if there exists a model where the pair gives reports on Monday or Tuesday
    # If not, then the pair must give reports on Wednesday if they give reports on the same day
    
    # Try Monday
    solver.push()
    solver.add(day_vars[s1] == 0)
    monday_tuesday_check = solver.check()
    solver.pop()
    
    # Try Tuesday
    solver.push()
    solver.add(day_vars[s1] == 1)
    monday_tuesday_check2 = solver.check()
    solver.pop()
    
    # If neither Monday nor Tuesday is possible, then the pair must be on Wednesday
    if monday_tuesday_check == unsat and monday_tuesday_check2 == unsat:
        # Check if there exists a model where the pair gives reports on Wednesday
        solver.push()
        solver.add(day_vars[s1] == 2)
        wednesday_check = solver.check()
        solver.pop()
        if wednesday_check == sat:
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