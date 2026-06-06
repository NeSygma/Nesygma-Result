from z3 import *

# Define assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# Create variables for each assistant: day (0=Wed,1=Thu,2=Fri) and time (0=morning,1=afternoon)
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

# Base constraints
solver = Solver()

# 1. Kevin and Rebecca same day
solver.add(day['Kevin'] == day['Rebecca'])

# 2. Lan and Olivia different days
solver.add(day['Lan'] != day['Olivia'])

# 3. Nessa afternoon
solver.add(time['Nessa'] == 1)

# 4. Julio earlier day than Olivia
solver.add(day['Julio'] < day['Olivia'])

# 5. All sessions distinct: each (day,time) pair used exactly once
# Compute session index = day*2 + time (0..5)
session_index = {}
for a in assistants:
    session_index[a] = day[a] * 2 + time[a]
solver.add(Distinct([session_index[a] for a in assistants]))

# Also ensure days are within 0..2 and times within 0..1
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# Now evaluate each answer choice
found_options = []

# Helper to add assignment constraints for a given choice
def add_choice_constraints(choice_name, assignments):
    # assignments is a list of tuples (day_index, time_index, assistant)
    for d, t, a in assignments:
        solver.add(day[a] == d)
        solver.add(time[a] == t)

# Choice A
choice_A = [
    (0, 0, 'Rebecca'),  # Wednesday morning
    (0, 1, 'Kevin'),    # Wednesday afternoon
    (1, 0, 'Julio'),    # Thursday morning
    (1, 1, 'Lan'),      # Thursday afternoon
    (2, 0, 'Nessa'),    # Friday morning
    (2, 1, 'Olivia')    # Friday afternoon
]

# Choice B
choice_B = [
    (0, 0, 'Olivia'),   # Wednesday morning
    (0, 1, 'Nessa'),    # Wednesday afternoon
    (1, 0, 'Julio'),    # Thursday morning
    (1, 1, 'Lan'),      # Thursday afternoon
    (2, 0, 'Kevin'),    # Friday morning
    (2, 1, 'Rebecca')   # Friday afternoon
]

# Choice C
choice_C = [
    (0, 0, 'Lan'),      # Wednesday morning
    (0, 1, 'Kevin'),    # Wednesday afternoon
    (1, 0, 'Rebecca'),  # Thursday morning
    (1, 1, 'Julio'),    # Thursday afternoon
    (2, 0, 'Olivia'),   # Friday morning
    (2, 1, 'Nessa')     # Friday afternoon
]

# Choice D
choice_D = [
    (0, 0, 'Kevin'),    # Wednesday morning
    (0, 1, 'Rebecca'),  # Wednesday afternoon
    (1, 0, 'Julio'),    # Thursday morning
    (1, 1, 'Nessa'),    # Thursday afternoon
    (2, 0, 'Olivia'),   # Friday morning
    (2, 1, 'Lan')       # Friday afternoon
]

# Choice E
choice_E = [
    (0, 0, 'Julio'),    # Wednesday morning
    (0, 1, 'Lan'),      # Wednesday afternoon
    (1, 0, 'Olivia'),   # Thursday morning
    (1, 1, 'Nessa'),    # Thursday afternoon
    (2, 0, 'Rebecca'),  # Friday morning
    (2, 1, 'Kevin')     # Friday afternoon
]

choices = [('A', choice_A), ('B', choice_B), ('C', choice_C), ('D', choice_D), ('E', choice_E)]

for letter, assignments in choices:
    solver.push()
    add_choice_constraints(letter, assignments)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result as per skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")