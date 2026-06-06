from z3 import *

# We have 6 lab sessions: 3 days (Wed, Thu, Fri) x 2 slots (morning, afternoon)
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Slots: 0=morning, 1=afternoon
# We'll assign each assistant to a (day, slot) pair.

# Let's use integer variables for each assistant representing the session index (0..5)
# Session indices: 0=Wed morning, 1=Wed afternoon, 2=Thu morning, 3=Thu afternoon, 4=Fri morning, 5=Fri afternoon
# But it's easier to use day and slot variables.

# Six assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
# We'll use Int variables for day (0,1,2) and slot (0,1) for each.

assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

day = {a: Int(f'day_{a}') for a in assistants}
slot = {a: Int(f'slot_{a}') for a in assistants}

solver = Solver()

# Domain constraints: day in {0,1,2}, slot in {0,1}
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(slot[a] >= 0, slot[a] <= 1)

# Each session is different: each assistant gets a unique (day, slot) pair
# We can encode this as: for any two distinct assistants, either day differs or slot differs
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Or(day[a1] != day[a2], slot[a1] != slot[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day.
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day.
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session.
solver.add(slot['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's.
solver.add(day['Julio'] < day['Olivia'])

# Additional condition: Julio and Kevin both lead morning sessions.
solver.add(slot['Julio'] == 0)
solver.add(slot['Kevin'] == 0)

# Now evaluate each option
# Option A: Lan's session meets Wednesday morning. => day['Lan'] == 0, slot['Lan'] == 0
opt_a = And(day['Lan'] == 0, slot['Lan'] == 0)

# Option B: Lan's session meets Thursday afternoon. => day['Lan'] == 1, slot['Lan'] == 1
opt_b = And(day['Lan'] == 1, slot['Lan'] == 1)

# Option C: Nessa's session meets Friday afternoon. => day['Nessa'] == 2, slot['Nessa'] == 1
opt_c = And(day['Nessa'] == 2, slot['Nessa'] == 1)

# Option D: Olivia's session meets Thursday morning. => day['Olivia'] == 1, slot['Olivia'] == 0
opt_d = And(day['Olivia'] == 1, slot['Olivia'] == 0)

# Option E: Olivia's session meets Friday morning. => day['Olivia'] == 2, slot['Olivia'] == 0
opt_e = And(day['Olivia'] == 2, slot['Olivia'] == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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