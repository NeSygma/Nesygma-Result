from z3 import *

# Define days and times
days = ["Wednesday", "Thursday", "Friday"]
times = ["morning", "afternoon"]

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Create variables: day and time for each assistant
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

# Each slot (day, time) is used by exactly one assistant
# We can create a slot variable for each assistant
slot = {}
for a in assistants:
    slot[a] = Int(f"slot_{a}")
    solver.add(slot[a] == assistant_day[a]*2 + assistant_time[a])
    solver.add(slot[a] >= 0)
    solver.add(slot[a] <= 5)

# All different slots
solver.add(Distinct([slot[a] for a in assistants]))

# Each day has exactly two sessions (morning and afternoon)
# We can enforce this by ensuring that for each day, there are exactly two assistants with that day
for d in range(3):
    # Count assistants on day d
    count_d = Sum([If(assistant_day[a] == d, 1, 0) for a in assistants])
    solver.add(count_d == 2)

# Each time (morning/afternoon) has exactly three sessions (one per day)
for t in range(2):
    count_t = Sum([If(assistant_time[a] == t, 1, 0) for a in assistants])
    solver.add(count_t == 3)

# Constraints
solver.add(assistant_day["Kevin"] == assistant_day["Rebecca"])
solver.add(assistant_day["Lan"] != assistant_day["Olivia"])
solver.add(assistant_time["Nessa"] == 1)  # afternoon
solver.add(assistant_day["Julio"] < assistant_day["Olivia"])
solver.add(assistant_day["Lan"] != 0)  # Not Wednesday (given condition)

# Base constraints are added. Now test each option.
# The question: "If Lan does not lead a Wednesday session, then which one of the following lab assistants must lead a Thursday session?"
# We need to find which assistant must be on Thursday in ALL valid solutions.

# For each option, we add the constraint that the assistant is NOT on Thursday.
# If the problem becomes unsatisfiable, then that assistant MUST be on Thursday.

found_options = []

# Option A: Rebecca
solver.push()
solver.add(assistant_day["Rebecca"] != 1)  # Rebecca not on Thursday
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Olivia
solver.push()
solver.add(assistant_day["Olivia"] != 1)  # Olivia not on Thursday
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Nessa
solver.push()
solver.add(assistant_day["Nessa"] != 1)  # Nessa not on Thursday
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kevin
solver.push()
solver.add(assistant_day["Kevin"] != 1)  # Kevin not on Thursday
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Julio
solver.push()
solver.add(assistant_day["Julio"] != 1)  # Julio not on Thursday
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")