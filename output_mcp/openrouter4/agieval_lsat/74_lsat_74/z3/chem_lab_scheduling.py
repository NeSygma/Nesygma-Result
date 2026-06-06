from z3 import *

solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=Morning, 1=Afternoon

assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Variables: day and time for each assistant
day = {a: Int(f"day_{a}") for a in assistants}
time = {a: Int(f"time_{a}") for a in assistants}

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All sessions must be distinct: each (day, time) pair is unique
# Encode as slot = day*2 + time, all slots distinct
slot = {a: Int(f"slot_{a}") for a in assistants}
for a in assistants:
    solver.add(slot[a] == day[a] * 2 + time[a])
solver.add(Distinct([slot[a] for a in assistants]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day["Kevin"] == day["Rebecca"])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day["Lan"] != day["Olivia"])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time["Nessa"] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day["Julio"] < day["Olivia"])

# Additional condition: Julio and Kevin both lead morning sessions
solver.add(time["Julio"] == 0)
solver.add(time["Kevin"] == 0)

# Option constraints
# (A) Lan's session meets Wednesday morning
opt_a = And(day["Lan"] == 0, time["Lan"] == 0)

# (B) Lan's session meets Thursday afternoon
opt_b = And(day["Lan"] == 1, time["Lan"] == 1)

# (C) Nessa's session meets Friday afternoon
opt_c = And(day["Nessa"] == 2, time["Nessa"] == 1)

# (D) Olivia's session meets Thursday morning
opt_d = And(day["Olivia"] == 1, time["Olivia"] == 0)

# (E) Olivia's session meets Friday morning
opt_e = And(day["Olivia"] == 2, time["Olivia"] == 0)

# The question asks: which of the following COULD be true EXCEPT?
# So we need to find the option that CANNOT be true (i.e., unsat).
# 4 options should be possible (sat), 1 should be impossible (unsat).

unsat_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {letter}: {res}")
    if res == unsat:
        unsat_options.append(letter)
    solver.pop()

print("---")
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all could be true)")