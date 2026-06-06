from z3 import *

# Define days and times
days = ["Wednesday", "Thursday", "Friday"]
times = ["morning", "afternoon"]

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Create variables
assistant_day = {}
assistant_time = {}
for a in assistants:
    assistant_day[a] = Int(f"day_{a}")
    assistant_time[a] = Int(f"time_{a}")

solver = Solver()

# Domain constraints
for a in assistants:
    solver.add(assistant_day[a] >= 0)
    solver.add(assistant_day[a] <= 2)
    solver.add(assistant_time[a] >= 0)
    solver.add(assistant_time[a] <= 1)

# Create slot variables
slot = {}
for a in assistants:
    slot[a] = Int(f"slot_{a}")
    solver.add(slot[a] == assistant_day[a]*2 + assistant_time[a])
    solver.add(slot[a] >= 0)
    solver.add(slot[a] <= 5)

# All different slots
solver.add(Distinct([slot[a] for a in assistants]))

# Constraints
solver.add(assistant_day["Kevin"] == assistant_day["Rebecca"])
solver.add(assistant_day["Lan"] != assistant_day["Olivia"])
solver.add(assistant_time["Nessa"] == 1)  # afternoon
solver.add(assistant_day["Julio"] < assistant_day["Olivia"])
solver.add(assistant_day["Lan"] != 0)  # Not Wednesday

# Find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for a in assistants:
        day_idx = m[assistant_day[a]].as_long()
        time_idx = m[assistant_time[a]].as_long()
        sol[a] = (days[day_idx], times[time_idx])
    solutions.append(sol)
    
    # Blocking clause to find different solutions
    blocking_clause = []
    for a in assistants:
        blocking_clause.append(slot[a] != m[slot[a]])
    solver.add(Or(blocking_clause))

print(f"Found {len(solutions)} solutions:")
for i, sol in enumerate(solutions):
    print(f"\nSolution {i+1}:")
    for a in assistants:
        day, time = sol[a]
        print(f"  {a}: {day} {time}")

# Check if Julio is always on Thursday
julio_on_thursday = all(sol["Julio"][0] == "Thursday" for sol in solutions)
print(f"\nJulio is on Thursday in all solutions: {julio_on_thursday}")

# Check other assistants
for a in assistants:
    on_thursday = all(sol[a][0] == "Thursday" for sol in solutions)
    print(f"{a} is on Thursday in all solutions: {on_thursday}")