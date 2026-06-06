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

found_options = []

# Option A: Julio, Nessa
opt_a_constr = Or(
    And(day['Julio'] == 1, session['Julio'] == 1),
    And(day['Nessa'] == 1, session['Nessa'] == 1)
)
# Option B: Kevin, Rebecca
opt_b_constr = Or(
    And(day['Kevin'] == 1, session['Kevin'] == 1),
    And(day['Rebecca'] == 1, session['Rebecca'] == 1)
)
# Option C: Kevin, Nessa, Rebecca
opt_c_constr = Or(
    And(day['Kevin'] == 1, session['Kevin'] == 1),
    And(day['Nessa'] == 1, session['Nessa'] == 1),
    And(day['Rebecca'] == 1, session['Rebecca'] == 1)
)
# Option D: Julio, Kevin, Nessa, Rebecca
opt_d_constr = Or(
    And(day['Julio'] == 1, session['Julio'] == 1),
    And(day['Kevin'] == 1, session['Kevin'] == 1),
    And(day['Nessa'] == 1, session['Nessa'] == 1),
    And(day['Rebecca'] == 1, session['Rebecca'] == 1)
)
# Option E: Julio, Kevin, Lan, Nessa, Rebecca
opt_e_constr = Or(
    And(day['Julio'] == 1, session['Julio'] == 1),
    And(day['Kevin'] == 1, session['Kevin'] == 1),
    And(day['Lan'] == 1, session['Lan'] == 1),
    And(day['Nessa'] == 1, session['Nessa'] == 1),
    And(day['Rebecca'] == 1, session['Rebecca'] == 1)
)

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