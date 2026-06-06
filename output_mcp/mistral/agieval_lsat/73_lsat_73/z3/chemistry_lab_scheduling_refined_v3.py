from z3 import *

# Create solver
solver = Solver()

# Lab assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# Sessions: 3 days (0=Wed,1=Thu,2=Fri) × 2 times (0=morning,1=afternoon) = 6 sessions
# Session indices: 0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1), 4:(2,0), 5:(2,1)

# Assign each assistant to a unique session index
session_index = {a: Int(f'{a}_session_idx') for a in assistants}
solver.add(Distinct(list(session_index.values())))  # Each assistant has a different session

# Map session index to (day, time)
def session_idx_to_day_time(idx):
    return (
        If(idx == 0, 0,
          If(idx == 1, 0,
            If(idx == 2, 1,
              If(idx == 3, 1,
                If(idx == 4, 2, 2)  # idx=5 -> (2,1)
              )
            )
          )
        ),
        If(idx == 0, 0,
          If(idx == 1, 1,
            If(idx == 2, 0,
              If(idx == 3, 1,
                If(idx == 4, 0, 1)  # idx=5 -> (2,1)
              )
            )
          )
        )
    )

# Extract day and time for each assistant
day = {}
time = {}
for a in assistants:
    d, t = session_idx_to_day_time(session_index[a])
    day[a] = d
    time[a] = t

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time['Nessa'] == 1)

# Constraint 4: Julio's session must be on an earlier day than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Constraint 5: Kevin's session meets on the day before Nessa's
solver.add(day['Kevin'] + 1 == day['Nessa'])

# Define the options for Thursday afternoon session (session index 3)
options = {
    "A": ["Julio", "Nessa"],
    "B": ["Kevin", "Rebecca"],
    "C": ["Kevin", "Nessa", "Rebecca"],
    "D": ["Julio", "Kevin", "Nessa", "Rebecca"],
    "E": ["Julio", "Kevin", "Lan", "Nessa", "Rebecca"]
}

found_options = []
for letter, assistants_list in options.items():
    solver.push()
    # At least one assistant in the list is assigned to session 3
    solver.add(Or([session_index[a] == 3 for a in assistants_list]))
    
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