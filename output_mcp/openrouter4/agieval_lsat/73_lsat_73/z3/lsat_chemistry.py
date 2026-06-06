from z3 import *

solver = Solver()

# 6 assistants: indices
# 0: Julio, 1: Kevin, 2: Lan, 3: Nessa, 4: Olivia, 5: Rebecca
N = 6
names = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Day: 0=Wed, 1=Thu, 2=Fri
day = [Int(f'day_{i}') for i in range(N)]
# Time: 0=morning, 1=afternoon
time = [Int(f'time_{i}') for i in range(N)]

# Domain constraints
for i in range(N):
    solver.add(day[i] >= 0, day[i] <= 2)
    solver.add(time[i] >= 0, time[i] <= 1)

# All sessions distinct: no two assistants share the same (day, time) pair
for i in range(N):
    for j in range(i+1, N):
        solver.add(Or(day[i] != day[j], time[i] != time[j]))

# Constraint 1: Kevin and Rebecca same day
solver.add(day[1] == day[5])

# Constraint 2: Lan and Olivia not same day
solver.add(day[2] != day[4])

# Constraint 3: Nessa afternoon
solver.add(time[3] == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(day[0] < day[4])

# Conditional: Kevin's session meets on the day before Nessa's
solver.add(day[1] == day[3] - 1)

# Find which assistants can be assigned to Thursday afternoon (day=1, time=1)
possible = []
for i in range(N):
    solver.push()
    solver.add(day[i] == 1, time[i] == 1)
    if solver.check() == sat:
        possible.append(i)
    solver.pop()

possible_names = [names[i] for i in possible]
print("Possible assistants for Thursday afternoon:", possible_names)

# Define option sets (indices)
options = {
    "A": {0, 3},           # Julio, Nessa
    "B": {1, 5},           # Kevin, Rebecca
    "C": {1, 3, 5},        # Kevin, Nessa, Rebecca
    "D": {0, 1, 3, 5},     # Julio, Kevin, Nessa, Rebecca
    "E": {0, 1, 2, 3, 5}   # Julio, Kevin, Lan, Nessa, Rebecca
}

possible_set = set(possible)

# Use the skeleton pattern
found_options = []
for letter, opt_set in options.items():
    if opt_set == possible_set:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")