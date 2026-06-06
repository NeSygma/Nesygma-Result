from z3 import *

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
idx = {name: i for i, name in enumerate(assistants)}

# Create solver
solver = Solver()

# Variables: day (0=Wed, 1=Thu, 2=Fri) and time (0=morning, 1=afternoon)
day = [Int(f"day_{i}") for i in range(6)]
time = [Int(f"time_{i}") for i in range(6)]

# Constraint: each (day, time) pair must be unique
# Use session index: day*2 + time (0-5)
session_idx = [day[i]*2 + time[i] for i in range(6)]
solver.add(Distinct(session_idx))

# Constraint: day and time must be in valid ranges
for i in range(6):
    solver.add(day[i] >= 0, day[i] <= 2)
    solver.add(time[i] >= 0, time[i] <= 1)

# Base constraints
# 1. Kevin and Rebecca same day
solver.add(day[idx["Kevin"]] == day[idx["Rebecca"]])

# 2. Lan and Olivia different days
solver.add(day[idx["Lan"]] != day[idx["Olivia"]])

# 3. Nessa afternoon
solver.add(time[idx["Nessa"]] == 1)

# 4. Julio earlier than Olivia
solver.add(day[idx["Julio"]] < day[idx["Olivia"]])

# Additional condition: Kevin's day is day before Nessa's
solver.add(day[idx["Kevin"]] == day[idx["Nessa"]] - 1)

# Now find all possible assistants for Thursday afternoon (day=1, time=1)
possible_assistants = []
for i, name in enumerate(assistants):
    s = Solver()
    s.add(solver.assertions())  # Copy base constraints
    s.add(day[i] == 1, time[i] == 1)
    if s.check() == sat:
        possible_assistants.append(name)

print("Possible assistants for Thursday afternoon:", possible_assistants)

# Compare with answer choices
options = {
    "A": ["Julio", "Nessa"],
    "B": ["Kevin", "Rebecca"],
    "C": ["Kevin", "Nessa", "Rebecca"],
    "D": ["Julio", "Kevin", "Nessa", "Rebecca"],
    "E": ["Julio", "Kevin", "Lan", "Nessa", "Rebecca"]
}

correct_option = None
for letter, names in options.items():
    if set(names) == set(possible_assistants):
        correct_option = letter
        break

if correct_option:
    print(f"STATUS: sat")
    print(f"answer:{correct_option}")
else:
    print("STATUS: unsat")
    print("Refine: No matching option found")