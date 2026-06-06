from z3 import *

# Define assistants
assistants = ['Julio', 'Kevin', 'Rebecca', 'Lan', 'Nessa', 'Olivia']
# Create day and time variables for each assistant
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

solver = Solver()
# Domain constraints: days 0=Wed,1=Thu,2=Fri; time 0=morning,1=afternoon
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All assistants have distinct (day,time) slots
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Constraints from problem
# Kevin and Rebecca same day
solver.add(day['Kevin'] == day['Rebecca'])
# Lan and Olivia not same day
solver.add(day['Lan'] != day['Olivia'])
# Nessa afternoon
solver.add(time['Nessa'] == 1)
# Julio earlier day than Olivia
solver.add(day['Julio'] < day['Olivia'])
# Julio leads Thursday afternoon (day=1, time=1)
solver.add(day['Julio'] == 1)
solver.add(time['Julio'] == 1)

# Enumerate all solutions
possible = {a: set() for a in assistants}
models = []
while solver.check() == sat:
    m = solver.model()
    # Record assignments
    for a in assistants:
        d = m[day[a]].as_long()
        t = m[time[a]].as_long()
        possible[a].add((d, t))
    # Block this model
    block = []
    for a in assistants:
        block.append(day[a] != m[day[a]])
        block.append(time[a] != m[time[a]])
    solver.add(Or(block))

# Determine how many assistants (excluding Julio) have uniquely determined slot
unique_count = 0
for a in assistants:
    if a == 'Julio':
        continue
    if len(possible[a]) == 1:
        unique_count += 1

# Prepare option constraints based on the computed count
opt_a_constr = BoolVal(unique_count == 1)  # one
opt_b_constr = BoolVal(unique_count == 2)  # two
opt_c_constr = BoolVal(unique_count == 3)  # three
opt_d_constr = BoolVal(unique_count == 4)  # four
opt_e_constr = BoolVal(unique_count == 5)  # five

# Multiple choice evaluation skeleton
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