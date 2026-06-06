from z3 import *

solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Slots: 0=morning, 1=afternoon

# Variables: day and slot for each assistant
julio_day = Int('julio_day')
julio_slot = Int('julio_slot')
kevin_day = Int('kevin_day')
kevin_slot = Int('kevin_slot')
lan_day = Int('lan_day')
lan_slot = Int('lan_slot')
nessa_day = Int('nessa_day')
nessa_slot = Int('nessa_slot')
olivia_day = Int('olivia_day')
olivia_slot = Int('olivia_slot')
rebecca_day = Int('rebecca_day')
rebecca_slot = Int('rebecca_slot')

days = [julio_day, kevin_day, lan_day, nessa_day, olivia_day, rebecca_day]
slots = [julio_slot, kevin_slot, lan_slot, nessa_slot, olivia_slot, rebecca_slot]

# Domain constraints: days 0-2, slots 0-1
for d in days:
    solver.add(d >= 0, d <= 2)
for s in slots:
    solver.add(s >= 0, s <= 1)

# All sessions are distinct (each (day, slot) pair used exactly once)
for i in range(6):
    for j in range(i+1, 6):
        solver.add(Or(days[i] != days[j], slots[i] != slots[j]))

# Constraint 1: Kevin and Rebecca must be on the same day
solver.add(kevin_day == rebecca_day)

# Constraint 2: Lan and Olivia cannot be on the same day
solver.add(lan_day != olivia_day)

# Constraint 3: Nessa must be afternoon
solver.add(nessa_slot == 1)

# Constraint 4: Julio's day < Olivia's day
solver.add(julio_day < olivia_day)

# Additional condition: Julio and Kevin both lead morning sessions
solver.add(julio_slot == 0)
solver.add(kevin_slot == 0)

# Test option A: Lan's session meets Wednesday morning
solver.add(lan_day == 0, lan_slot == 0)

result = solver.check()
print(f"Option A check: {result}")

if result == sat:
    m = solver.model()
    print("Option A is SAT - here's a model:")
    for var in [julio_day, julio_slot, kevin_day, kevin_slot, lan_day, lan_slot, 
                nessa_day, nessa_slot, olivia_day, olivia_slot, rebecca_day, rebecca_slot]:
        print(f"{var} = {m[var]}")
else:
    print("Option A is UNSAT - cannot be true")