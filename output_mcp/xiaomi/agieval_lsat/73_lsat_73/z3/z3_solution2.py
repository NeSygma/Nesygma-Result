from z3 import *

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Session: 0=morning, 1=afternoon
# Each assistant assigned to a (day, session) pair

solver = Solver()

# Variables: for each assistant, their day and session
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
day = {a: Int(f'day_{a}') for a in assistants}
session = {a: Int(f'session_{a}') for a in assistants}

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(session[a] >= 0, session[a] <= 1)

# All assistants assigned to different (day, session) pairs
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        solver.add(Or(day[assistants[i]] != day[assistants[j]], 
                       session[assistants[i]] != session[assistants[j]]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(session['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Additional constraint from question: Kevin's session meets on the day before Nessa's
solver.add(day['Kevin'] == day['Nessa'] - 1)

# Now we need to find who could lead Thursday afternoon session
# Thursday = day 1, afternoon = session 1
# We need to find all assistants who CAN be assigned to (day=1, session=1)

# Check each assistant individually
could_lead = []
for a in assistants:
    s = Solver()
    # Copy all base constraints
    for c in solver.assertions():
        s.add(c)
    # Add that this assistant leads Thursday afternoon
    s.add(day[a] == 1, session[a] == 1)
    if s.check() == sat:
        could_lead.append(a)

print("STATUS: sat")
print(f"Could lead Thursday afternoon: {could_lead}")

# Now match to answer choices
options = {
    "A": ['Julio', 'Nessa'],
    "B": ['Kevin', 'Rebecca'],
    "C": ['Kevin', 'Nessa', 'Rebecca'],
    "D": ['Julio', 'Kevin', 'Nessa', 'Rebecca'],
    "E": ['Julio', 'Kevin', 'Lan', 'Nessa', 'Rebecca']
}

# Find which option exactly matches could_lead
for letter, opt_list in options.items():
    if set(opt_list) == set(could_lead):
        print(f"answer:{letter}")
        break
else:
    print("No exact match found")
    print(f"Answer choices don't match: {could_lead}")