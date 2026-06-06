from z3 import *

# Define the assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# Define days and times
days = ['Wednesday', 'Thursday', 'Friday']
times = ['Morning', 'Afternoon']

# Create variables: for each assistant, which day and time they are assigned
# day[a] = 0 (Wed), 1 (Thu), 2 (Fri)
# time[a] = 0 (Morning), 1 (Afternoon)
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

solver = Solver()

# Each assistant assigned to exactly one day (0,1,2) and one time (0,1)
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All assignments must be distinct (each session is unique)
# A session is a (day, time) pair. There are 6 sessions total.
# Each assistant gets a unique (day, time) combination.
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1, a2 = assistants[i], assistants[j]
        solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Additional constraint from the question: Julio leads Thursday afternoon session
solver.add(day['Julio'] == 1)  # Thursday
solver.add(time['Julio'] == 1)  # Afternoon

# Now we need to determine for how many OTHER assistants (besides Julio)
# we can uniquely determine their session assignment.
# We'll check each assistant by seeing if their day and time are uniquely determined.

# First, find all possible models
all_models = []
temp_solver = Solver()
# Copy all constraints
for c in solver.assertions():
    temp_solver.add(c)

while temp_solver.check() == sat:
    m = temp_solver.model()
    model_dict = {}
    for a in assistants:
        model_dict[a] = (m.evaluate(day[a]).as_long(), m.evaluate(time[a]).as_long())
    all_models.append(model_dict)
    # Block this specific assignment
    block = []
    for a in assistants:
        block.append(Or(day[a] != m.evaluate(day[a]), time[a] != m.evaluate(time[a])))
    temp_solver.add(Or(block))

print(f"Total valid assignments found: {len(all_models)}")

# For each assistant (except Julio), check if their assignment is the same in all models
determined = []
for a in assistants:
    if a == 'Julio':
        continue
    # Get all assignments for this assistant across models
    assignments = set()
    for model in all_models:
        assignments.add(model[a])
    if len(assignments) == 1:
        determined.append(a)
        print(f"{a} is uniquely determined: Day={days[assignments.pop()[0]]}, Time={times[assignments.pop()[1]] if len(assignments) > 0 else '?'}")
    else:
        print(f"{a} has {len(assignments)} possible assignments")

print(f"\nNumber of other assistants uniquely determined: {len(determined)}")

# Now map to answer choices
# (A) one, (B) two, (C) three, (D) four, (E) five
answer_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}

if len(determined) in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[len(determined)]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Unexpected count {len(determined)}")