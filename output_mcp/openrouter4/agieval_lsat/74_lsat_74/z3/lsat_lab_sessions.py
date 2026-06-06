from z3 import *

solver = Solver()

# Days: 0=Wed, 1=Thu, 2=Fri
# Times: 0=morning, 1=afternoon

assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
day = {a: Int(f"day_{a}") for a in assistants}
time = {a: Int(f"time_{a}") for a in assistants}

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# Each session is different - ensure all (day, time) pairs are distinct
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1, a2 = assistants[i], assistants[j]
        solver.add(Not(And(day[a1] == day[a2], time[a1] == time[a2])))

# Constraint 1: Kevin and Rebecca same day
solver.add(day["Kevin"] == day["Rebecca"])

# Constraint 2: Lan and Olivia different days
solver.add(day["Lan"] != day["Olivia"])

# Constraint 3: Nessa afternoon
solver.add(time["Nessa"] == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(day["Julio"] < day["Olivia"])

# Conditional: Julio and Kevin both morning
solver.add(time["Julio"] == 0)
solver.add(time["Kevin"] == 0)

# Now test each option
options = [
    ("A", And(day["Lan"] == 0, time["Lan"] == 0)),  # Wed morning
    ("B", And(day["Lan"] == 1, time["Lan"] == 1)),  # Thu afternoon
    ("C", And(day["Nessa"] == 2, time["Nessa"] == 1)),  # Fri afternoon
    ("D", And(day["Olivia"] == 1, time["Olivia"] == 0)),  # Thu morning
    ("E", And(day["Olivia"] == 2, time["Olivia"] == 0)),  # Fri morning
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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