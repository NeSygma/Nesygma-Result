from z3 import *

# Define the assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# Define days and sessions
days = ['Wednesday', 'Thursday', 'Friday']
sessions = ['Morning', 'Afternoon']

# Create variables: for each day and session, which assistant is assigned
# We'll use Int variables for each assistant's day and session
day_of = {a: Int(f'day_{a}') for a in assistants}  # 0=Wed, 1=Thu, 2=Fri
session_of = {a: Int(f'session_{a}') for a in assistants}  # 0=Morning, 1=Afternoon

solver = Solver()

# Each assistant assigned to exactly one day (0,1,2) and one session (0,1)
for a in assistants:
    solver.add(day_of[a] >= 0, day_of[a] <= 2)
    solver.add(session_of[a] >= 0, session_of[a] <= 1)

# All assignments are unique (each day-session slot gets exactly one assistant)
# There are 6 slots: 3 days × 2 sessions
# We need to ensure no two assistants share the same (day, session)
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1, a2 = assistants[i], assistants[j]
        solver.add(Or(day_of[a1] != day_of[a2], session_of[a1] != session_of[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day_of['Kevin'] == day_of['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day_of['Lan'] != day_of['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(session_of['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day_of['Julio'] < day_of['Olivia'])

# Now define each option as constraints
# Option A: Wednesday: Rebecca, Kevin Thursday: Julio, Lan Friday: Nessa, Olivia
opt_a_constr = And(
    day_of['Rebecca'] == 0, session_of['Rebecca'] == 0,  # Wed morning
    day_of['Kevin'] == 0, session_of['Kevin'] == 1,      # Wed afternoon
    day_of['Julio'] == 1, session_of['Julio'] == 0,      # Thu morning
    day_of['Lan'] == 1, session_of['Lan'] == 1,          # Thu afternoon
    day_of['Nessa'] == 2, session_of['Nessa'] == 0,      # Fri morning
    day_of['Olivia'] == 2, session_of['Olivia'] == 1     # Fri afternoon
)

# Option B: Wednesday: Olivia, Nessa Thursday: Julio, Lan Friday: Kevin, Rebecca
opt_b_constr = And(
    day_of['Olivia'] == 0, session_of['Olivia'] == 0,    # Wed morning
    day_of['Nessa'] == 0, session_of['Nessa'] == 1,      # Wed afternoon
    day_of['Julio'] == 1, session_of['Julio'] == 0,      # Thu morning
    day_of['Lan'] == 1, session_of['Lan'] == 1,          # Thu afternoon
    day_of['Kevin'] == 2, session_of['Kevin'] == 0,      # Fri morning
    day_of['Rebecca'] == 2, session_of['Rebecca'] == 1   # Fri afternoon
)

# Option C: Wednesday: Lan, Kevin Thursday: Rebecca, Julio Friday: Olivia, Nessa
opt_c_constr = And(
    day_of['Lan'] == 0, session_of['Lan'] == 0,          # Wed morning
    day_of['Kevin'] == 0, session_of['Kevin'] == 1,      # Wed afternoon
    day_of['Rebecca'] == 1, session_of['Rebecca'] == 0,  # Thu morning
    day_of['Julio'] == 1, session_of['Julio'] == 1,      # Thu afternoon
    day_of['Olivia'] == 2, session_of['Olivia'] == 0,    # Fri morning
    day_of['Nessa'] == 2, session_of['Nessa'] == 1       # Fri afternoon
)

# Option D: Wednesday: Kevin, Rebecca Thursday: Julio, Nessa Friday: Olivia, Lan
opt_d_constr = And(
    day_of['Kevin'] == 0, session_of['Kevin'] == 0,      # Wed morning
    day_of['Rebecca'] == 0, session_of['Rebecca'] == 1,  # Wed afternoon
    day_of['Julio'] == 1, session_of['Julio'] == 0,      # Thu morning
    day_of['Nessa'] == 1, session_of['Nessa'] == 1,      # Thu afternoon
    day_of['Olivia'] == 2, session_of['Olivia'] == 0,    # Fri morning
    day_of['Lan'] == 2, session_of['Lan'] == 1           # Fri afternoon
)

# Option E: Wednesday: Julio, Lan Thursday: Olivia, Nessa Friday: Rebecca, Kevin
opt_e_constr = And(
    day_of['Julio'] == 0, session_of['Julio'] == 0,      # Wed morning
    day_of['Lan'] == 0, session_of['Lan'] == 1,          # Wed afternoon
    day_of['Olivia'] == 1, session_of['Olivia'] == 0,    # Thu morning
    day_of['Nessa'] == 1, session_of['Nessa'] == 1,      # Thu afternoon
    day_of['Rebecca'] == 2, session_of['Rebecca'] == 0,  # Fri morning
    day_of['Kevin'] == 2, session_of['Kevin'] == 1       # Fri afternoon
)

# Test each option
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