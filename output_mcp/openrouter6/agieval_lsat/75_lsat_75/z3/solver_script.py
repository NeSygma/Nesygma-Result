from z3 import *

# Define assistants
assistants = ["julio", "kevin", "lan", "nessa", "olivia", "rebecca"]
# Variables for day and time
day = {}
time = {}
for a in assistants:
    day[a] = Int(f"day_{a}")
    time[a] = Int(f"time_{a}")

solver = Solver()

# Domain constraints: day in {0,1,2}, time in {0,1}
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All (day,time) pairs distinct
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Base constraints
# Kevin and Rebecca same day
solver.add(day["kevin"] == day["rebecca"])
# Lan and Olivia different days
solver.add(day["lan"] != day["olivia"])
# Nessa afternoon
solver.add(time["nessa"] == 1)
# Julio earlier day than Olivia
solver.add(day["julio"] < day["olivia"])
# Julio Thursday afternoon
solver.add(day["julio"] == 1)
solver.add(time["julio"] == 1)

# Enumerate all models
models = []
while True:
    result = solver.check()
    if result != sat:
        break
    m = solver.model()
    # Record assignment for each assistant
    assignment = {}
    for a in assistants:
        d = m.evaluate(day[a], model_completion=True)
        t = m.evaluate(time[a], model_completion=True)
        assignment[a] = (d.as_long(), t.as_long())
    models.append(assignment)
    # Blocking clause: at least one variable differs
    block = []
    for a in assistants:
        block.append(day[a] != m.evaluate(day[a], model_completion=True))
        block.append(time[a] != m.evaluate(time[a], model_completion=True))
    solver.add(Or(block))

# Now compute for each assistant (excluding julio) if their session is determined
determined_count = 0
for a in assistants:
    if a == "julio":
        continue
    sessions = set()
    for m in models:
        sessions.add(m[a])
    if len(sessions) == 1:
        determined_count += 1

# Map count to answer choice
if determined_count == 1:
    answer = "A"
elif determined_count == 2:
    answer = "B"
elif determined_count == 3:
    answer = "C"
elif determined_count == 4:
    answer = "D"
elif determined_count == 5:
    answer = "E"
else:
    answer = "unknown"

print("STATUS: sat")
print(f"answer:{answer}")