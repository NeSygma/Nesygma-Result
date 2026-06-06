from z3 import *

solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Periods: 0=Morning, 1=Afternoon
# Each assistant gets a day and a period
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
day = {a: Int(f'day_{a}') for a in assistants}
period = {a: Int(f'period_{a}') for a in assistants}

# Domain constraints: days 0-2, periods 0-1
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(period[a] >= 0, period[a] <= 1)

# All assignments must be unique (each session is unique day+period combo)
# Encode as: for every pair of assistants, they differ in day or period
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1, a2 = assistants[i], assistants[j]
        solver.add(Or(day[a1] != day[a2], period[a1] != period[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(period['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Additional condition: Lan does NOT lead a Wednesday session
solver.add(day['Lan'] != 0)

# Now check which assistant MUST lead a Thursday session
# We check each option: does adding "assistant NOT on Thursday" make it UNSAT?
# If so, that assistant MUST be on Thursday.

must_be_thursday = []
for a in assistants:
    s = Solver()
    # Copy all base constraints
    for c in solver.assertions():
        s.add(c)
    # Add: this assistant is NOT on Thursday
    s.add(day[a] != 1)
    if s.check() == unsat:
        must_be_thursday.append(a)

print("Assistants that MUST be on Thursday:", must_be_thursday)

# Map to answer choices
# (A) Rebecca, (B) Olivia, (C) Nessa, (D) Kevin, (E) Julio
choice_map = {'Rebecca': 'A', 'Olivia': 'B', 'Nessa': 'C', 'Kevin': 'D', 'Julio': 'E'}

found_options = []
for a in must_be_thursday:
    if a in choice_map:
        found_options.append(choice_map[a])

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")