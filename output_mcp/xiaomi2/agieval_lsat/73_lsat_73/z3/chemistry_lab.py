from z3 import *

assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# Day: 0=Wed, 1=Thu, 2=Fri; Time: 0=morning, 1=afternoon
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

def add_base_constraints(solver):
    for a in assistants:
        solver.add(day[a] >= 0, day[a] <= 2)
        solver.add(time[a] >= 0, time[a] <= 1)
    
    # All 6 (day, time) pairs must be distinct (each slot has exactly one assistant)
    solver.add(Distinct([day[a] * 2 + time[a] for a in assistants]))
    
    # Constraint 1: Kevin and Rebecca must lead sessions on the same day
    solver.add(day['Kevin'] == day['Rebecca'])
    
    # Constraint 2: Lan and Olivia cannot lead sessions on the same day
    solver.add(day['Lan'] != day['Olivia'])
    
    # Constraint 3: Nessa must lead an afternoon session
    solver.add(time['Nessa'] == 1)
    
    # Constraint 4: Julio's session on an earlier day than Olivia's
    solver.add(day['Julio'] < day['Olivia'])
    
    # Constraint 5 (conditional): Kevin's session meets on the day before Nessa's
    solver.add(day['Kevin'] == day['Nessa'] - 1)

# Check each assistant for Thursday afternoon (day=1, time=1)
possible = []
for a in assistants:
    s = Solver()
    add_base_constraints(s)
    s.add(day[a] == 1, time[a] == 1)
    if s.check() == sat:
        possible.append(a)
        m = s.model()
        print(f"  {a} CAN lead Thu afternoon. Sample assignment:")
        for name in assistants:
            print(f"    {name}: day={m[day[name]]}, time={m[time[name]]}")

print(f"\nAll possible Thursday afternoon leaders: {possible}")

# Match to answer choices
options = {
    'A': set(['Julio', 'Nessa']),
    'B': set(['Kevin', 'Rebecca']),
    'C': set(['Kevin', 'Nessa', 'Rebecca']),
    'D': set(['Julio', 'Kevin', 'Nessa', 'Rebecca']),
    'E': set(['Julio', 'Kevin', 'Lan', 'Nessa', 'Rebecca'])
}

found_options = []
for letter, members in options.items():
    if set(possible) == members:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print(f"Refine: No options found. Possible set = {possible}")