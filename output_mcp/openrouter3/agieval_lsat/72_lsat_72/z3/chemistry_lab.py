from z3 import *

# Define days and times
days = ["Wednesday", "Thursday", "Friday"]
times = ["morning", "afternoon"]

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Create variables: assistant_day[assistant] = day index (0,1,2)
# assistant_time[assistant] = time index (0=morning, 1=afternoon)
assistant_day = {}
assistant_time = {}
for a in assistants:
    assistant_day[a] = Int(f"day_{a}")
    assistant_time[a] = Int(f"time_{a}")

solver = Solver()

# Domain constraints: days 0-2, times 0-1
for a in assistants:
    solver.add(assistant_day[a] >= 0)
    solver.add(assistant_day[a] <= 2)
    solver.add(assistant_time[a] >= 0)
    solver.add(assistant_time[a] <= 1)

# Each assistant has exactly one session (implied by variables)
# Each day has exactly 2 sessions (morning and afternoon)
# We need to ensure that for each day and time, exactly one assistant is assigned
# This is a permutation constraint - we'll use all-different on pairs (day, time)
# But since we have 6 assistants and 6 slots, we can use all-different on day-time combinations

# Create a combined variable for each assistant: slot = day*2 + time
# This gives 6 possible slots: 0-5
slot = {}
for a in assistants:
    slot[a] = Int(f"slot_{a}")
    solver.add(slot[a] == assistant_day[a]*2 + assistant_time[a])
    solver.add(slot[a] >= 0)
    solver.add(slot[a] <= 5)

# All assistants must have different slots (each slot has exactly one assistant)
solver.add(Distinct([slot[a] for a in assistants]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(assistant_day["Kevin"] == assistant_day["Rebecca"])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(assistant_day["Lan"] != assistant_day["Olivia"])

# Constraint 3: Nessa must lead an afternoon session
solver.add(assistant_time["Nessa"] == 1)  # afternoon

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(assistant_day["Julio"] < assistant_day["Olivia"])

# Additional condition: Lan does not lead a Wednesday session
# Wednesday is day 0
solver.add(assistant_day["Lan"] != 0)

# Now we need to check which assistant MUST lead a Thursday session
# Thursday is day 1

# First, let's check if there's any solution at all
print("Checking base constraints...")
result = solver.check()
if result == sat:
    print("Base constraints are satisfiable")
    m = solver.model()
    print("Example solution:")
    for a in assistants:
        day_idx = m[assistant_day[a]].as_long()
        time_idx = m[assistant_time[a]].as_long()
        print(f"  {a}: {days[day_idx]} {times[time_idx]}")
else:
    print("Base constraints are unsatisfiable - problem has no solution")
    exit()

# Now test each answer choice
# We need to check: if Lan does not lead Wednesday, which assistant MUST lead Thursday?
# This means: for each assistant X, check if in ALL valid solutions, X leads Thursday

# We'll test each option by checking if the assistant leads Thursday in all solutions
# But we need to be careful: we need to check if there exists a solution where X does NOT lead Thursday
# If no such solution exists, then X MUST lead Thursday

# Let's use the multiple choice skeleton
found_options = []

# Option A: Rebecca must lead Thursday
print("\nTesting Option A: Rebecca must lead Thursday")
solver.push()
# We want to check if Rebecca does NOT lead Thursday is possible
# If it's UNSAT, then Rebecca MUST lead Thursday
solver.add(assistant_day["Rebecca"] != 1)  # Not Thursday
result_a = solver.check()
solver.pop()
if result_a == unsat:
    found_options.append("A")
    print("  Rebecca MUST lead Thursday (no solution where she doesn't)")
else:
    print("  Rebecca does NOT necessarily lead Thursday")

# Option B: Olivia must lead Thursday
print("\nTesting Option B: Olivia must lead Thursday")
solver.push()
solver.add(assistant_day["Olivia"] != 1)  # Not Thursday
result_b = solver.check()
solver.pop()
if result_b == unsat:
    found_options.append("B")
    print("  Olivia MUST lead Thursday")
else:
    print("  Olivia does NOT necessarily lead Thursday")

# Option C: Nessa must lead Thursday
print("\nTesting Option C: Nessa must lead Thursday")
solver.push()
solver.add(assistant_day["Nessa"] != 1)  # Not Thursday
result_c = solver.check()
solver.pop()
if result_c == unsat:
    found_options.append("C")
    print("  Nessa MUST lead Thursday")
else:
    print("  Nessa does NOT necessarily lead Thursday")

# Option D: Kevin must lead Thursday
print("\nTesting Option D: Kevin must lead Thursday")
solver.push()
solver.add(assistant_day["Kevin"] != 1)  # Not Thursday
result_d = solver.check()
solver.pop()
if result_d == unsat:
    found_options.append("D")
    print("  Kevin MUST lead Thursday")
else:
    print("  Kevin does NOT necessarily lead Thursday")

# Option E: Julio must lead Thursday
print("\nTesting Option E: Julio must lead Thursday")
solver.push()
solver.add(assistant_day["Julio"] != 1)  # Not Thursday
result_e = solver.check()
solver.pop()
if result_e == unsat:
    found_options.append("E")
    print("  Julio MUST lead Thursday")
else:
    print("  Julio does NOT necessarily lead Thursday")

# Final result
print(f"\nFound options: {found_options}")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")