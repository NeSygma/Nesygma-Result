from z3 import *

# Assistant indices
JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA = range(6)
assistants = [JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA]

solver = Solver()

# Variables: day and time for each assistant
day = [Int(f"day_{i}") for i in assistants]   # 0=Wed,1=Thu,2=Fri
time = [Int(f"time_{i}") for i in assistants] # 0=morning,1=afternoon

# Domain constraints
for i in assistants:
    solver.add(day[i] >= 0, day[i] <= 2)
    solver.add(time[i] >= 0, time[i] <= 1)

# All slots distinct
for i in assistants:
    for j in assistants:
        if i < j:
            solver.add(Or(day[i] != day[j], time[i] != time[j]))

# Problem constraints
# Kevin and Rebecca same day
solver.add(day[KEVIN] == day[REBECCA])
# Lan and Olivia different day
solver.add(day[LAN] != day[OLIVIA])
# Nessa afternoon
solver.add(time[NESSA] == 1)
# Julio earlier day than Olivia
solver.add(day[JULIO] < day[OLIVIA])
# Condition: Lan not Wednesday
solver.add(day[LAN] != 0)

# Define option constraints: each option asserts that that assistant leads Thursday (day == 1)
opt_a_constr = (day[REBECCA] == 1)  # A: Rebecca
opt_b_constr = (day[OLIVIA] == 1)   # B: Olivia
opt_c_constr = (day[NESSA] == 1)    # C: Nessa
opt_d_constr = (day[KEVIN] == 1)    # D: Kevin
opt_e_constr = (day[JULIO] == 1)    # E: Julio

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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