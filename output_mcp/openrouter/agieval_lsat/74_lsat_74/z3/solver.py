from z3 import *

# Assistants
assistants = ['Julio','Kevin','Lan','Nessa','Olivia','Rebecca']
# Variables: day 0=Wed,1=Thu,2=Fri; time 0=morning,1=afternoon
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

solver = Solver()
# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All distinct slots (day*2+time)
slots = [day[a]*2 + time[a] for a in assistants]
for i in range(len(slots)):
    for j in range(i+1, len(slots)):
        solver.add(slots[i] != slots[j])

# Base constraints
solver.add(day['Kevin'] == day['Rebecca'])          # same day
solver.add(day['Lan'] != day['Olivia'])            # different day
solver.add(time['Nessa'] == 1)                    # afternoon
solver.add(day['Julio'] < day['Olivia'])          # earlier day
# Additional condition: Julio and Kevin both morning
solver.add(time['Julio'] == 0)
solver.add(time['Kevin'] == 0)

# Option constraints (the statement to be true)
opt_a = And(day['Lan'] == 0, time['Lan'] == 0)   # Wed morning
opt_b = And(day['Lan'] == 1, time['Lan'] == 1)   # Thu afternoon
opt_c = And(day['Nessa'] == 2, time['Nessa'] == 1) # Fri afternoon
opt_d = And(day['Olivia'] == 1, time['Olivia'] == 0) # Thu morning
opt_e = And(day['Olivia'] == 2, time['Olivia'] == 0) # Fri morning

impossible = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible.append(letter)
    solver.pop()

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")