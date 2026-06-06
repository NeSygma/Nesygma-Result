from z3 import *

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=morning, 1=afternoon

# Create variables for each assistant: day and time
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
day = {a: Int(f"day_{a}") for a in assistants}
time = {a: Int(f"time_{a}") for a in assistants}

solver = Solver()

# Domain constraints for days and times
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)  # 0,1,2 for Wed,Thu,Fri
    solver.add(time[a] >= 0, time[a] <= 1)  # 0,1 for morning,afternoon

# All sessions are distinct (each assistant has unique day-time combination)
session_pairs = [(a1, a2) for i, a1 in enumerate(assistants) for a2 in assistants[i+1:]]
for a1, a2 in session_pairs:
    solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day["Kevin"] == day["Rebecca"])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day["Lan"] != day["Olivia"])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time["Nessa"] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day["Julio"] < day["Olivia"])

# Additional constraint from question: Julio and Kevin both lead morning sessions
solver.add(time["Julio"] == 0)
solver.add(time["Kevin"] == 0)

# Now test each option - we want to find which option CANNOT be true
# So we check if adding the option makes the problem UNSAT
impossible_options = []

# Option A: Lan's session meets Wednesday morning
opt_a = And(day["Lan"] == 0, time["Lan"] == 0)
solver.push()
solver.add(opt_a)
if solver.check() == unsat:
    impossible_options.append("A")
solver.pop()

# Option B: Lan's session meets Thursday afternoon
opt_b = And(day["Lan"] == 1, time["Lan"] == 1)
solver.push()
solver.add(opt_b)
if solver.check() == unsat:
    impossible_options.append("B")
solver.pop()

# Option C: Nessa's session meets Friday afternoon
opt_c = And(day["Nessa"] == 2, time["Nessa"] == 1)
solver.push()
solver.add(opt_c)
if solver.check() == unsat:
    impossible_options.append("C")
solver.pop()

# Option D: Olivia's session meets Thursday morning
opt_d = And(day["Olivia"] == 1, time["Olivia"] == 0)
solver.push()
solver.add(opt_d)
if solver.check() == unsat:
    impossible_options.append("D")
solver.pop()

# Option E: Olivia's session meets Friday morning
opt_e = And(day["Olivia"] == 2, time["Olivia"] == 0)
solver.push()
solver.add(opt_e)
if solver.check() == unsat:
    impossible_options.append("E")
solver.pop()

# Print results
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")