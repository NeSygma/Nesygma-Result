from z3 import *

# Define assistants
assistants = ['Julio','Kevin','Lan','Nessa','Olivia','Rebecca']
# Create variables for day (0=Wed,1=Thu,2=Fri) and time (0=morning,1=afternoon)
Day = {a: Int(f"day_{a}") for a in assistants}
Time = {a: Int(f"time_{a}") for a in assistants}

solver = Solver()
# Domain constraints
for a in assistants:
    solver.add(Day[a] >= 0, Day[a] <= 2)
    solver.add(Time[a] >= 0, Time[a] <= 1)

# All assistants must occupy distinct sessions (day,time)
# Ensure no two assistants share same day and time
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a = assistants[i]
        b = assistants[j]
        solver.add(Or(Day[a] != Day[b], Time[a] != Time[b]))

# Base constraints
# Kevin and Rebecca same day
solver.add(Day['Kevin'] == Day['Rebecca'])
# Lan and Olivia different days
solver.add(Day['Lan'] != Day['Olivia'])
# Nessa afternoon
solver.add(Time['Nessa'] == 1)
# Julio earlier day than Olivia
solver.add(Day['Julio'] < Day['Olivia'])

# Helper to create option constraints

def option_constraints(assignments):
    # assignments: dict of assistant -> (day, time)
    cons = []
    for a, (d, t) in assignments.items():
        cons.append(Day[a] == d)
        cons.append(Time[a] == t)
    return cons

# Define options
# Days: 0=Wed,1=Thu,2=Fri
# Times: 0=morning,1=afternoon
opt_a = {
    'Rebecca': (0,0), 'Kevin': (0,1),
    'Julio': (1,0), 'Lan': (1,1),
    'Nessa': (2,0), 'Olivia': (2,1)
}
opt_b = {
    'Olivia': (0,0), 'Nessa': (0,1),
    'Julio': (1,0), 'Lan': (1,1),
    'Kevin': (2,0), 'Rebecca': (2,1)
}
opt_c = {
    'Lan': (0,0), 'Kevin': (0,1),
    'Rebecca': (1,0), 'Julio': (1,1),
    'Olivia': (2,0), 'Nessa': (2,1)
}
opt_d = {
    'Kevin': (0,0), 'Rebecca': (0,1),
    'Julio': (1,0), 'Nessa': (1,1),
    'Olivia': (2,0), 'Lan': (2,1)
}
opt_e = {
    'Julio': (0,0), 'Lan': (0,1),
    'Olivia': (1,0), 'Nessa': (1,1),
    'Rebecca': (2,0), 'Kevin': (2,1)
}

# Map letters to constraints
options = {
    'A': option_constraints(opt_a),
    'B': option_constraints(opt_b),
    'C': option_constraints(opt_c),
    'D': option_constraints(opt_d),
    'E': option_constraints(opt_e)
}

found_options = []
for letter, constr in options.items():
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