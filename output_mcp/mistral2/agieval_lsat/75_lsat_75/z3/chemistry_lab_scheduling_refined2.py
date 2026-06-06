from z3 import *

# BENCHMARK_MODE: ON (problem is solvable)
BENCHMARK_MODE = True

# Define assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
assistant_to_idx = {a: i for i, a in enumerate(assistants)}

# Initialize solver
solver = Solver()

# Decision variables: day and time for each assistant
# day: 0=Wed, 1=Thu, 2=Fri
# time: 0=Morning, 1=Afternoon
day = [Int(f'day_{a}') for a in assistants]
time = [Int(f'time_{a}') for a in assistants]

# Each assistant has a unique (day, time) pair
for i in range(len(assistants)):
    for j in range(i + 1, len(assistants)):
        solver.add(Or(day[i] != day[j], time[i] != time[j]))

# Constraints
# 1. Kevin and Rebecca must be on the same day
solver.add(day[assistant_to_idx['Kevin']] == day[assistant_to_idx['Rebecca']])

# 2. Lan and Olivia cannot be on the same day
solver.add(day[assistant_to_idx['Lan']] != day[assistant_to_idx['Olivia']])

# 3. Nessa must be in the afternoon
solver.add(time[assistant_to_idx['Nessa']] == 1)

# 4. Julio's session must be earlier than Olivia's
solver.add(day[assistant_to_idx['Julio']] < day[assistant_to_idx['Olivia']])

# 5. Given: Julio is Thursday afternoon
solver.add(day[assistant_to_idx['Julio']] == 1)
solver.add(time[assistant_to_idx['Julio']] == 1)

# Additional constraints to ensure all days and times are valid
for d in day:
    solver.add(d >= 0, d <= 2)
for t in time:
    solver.add(t >= 0, t <= 1)

# Check if the problem is satisfiable
result = solver.check()
if result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    exit()

model = solver.model()

# Extract the (day, time) for each assistant from the model
assignments = {}
for a in assistants:
    a_idx = assistant_to_idx[a]
    d = model[day[a_idx]]
    t = model[time[a_idx]]
    assignments[a] = (d, t)

# Now, for each assistant (excluding Julio), check if their (day, time) is uniquely determined
# To do this, we block all other possible (day, time) pairs for that assistant and see if the solver still finds a solution
determined_count = 0
for a in assistants:
    if a == 'Julio':
        continue
    a_idx = assistant_to_idx[a]
    d_val = model[day[a_idx]].as_long()
    t_val = model[time[a_idx]].as_long()
    # Create a new solver to check uniqueness
    s = Solver()
    s.add(solver.assertions())
    # Block all other (day, time) pairs for this assistant
    for d in range(3):
        for t in range(2):
            if d == d_val and t == t_val:
                continue
            s.add(Or(day[a_idx] != d, time[a_idx] != t))
    # If no other solution exists, this assistant is determined
    if s.check() == unsat:
        determined_count += 1

# Now, evaluate the answer choices
found_options = []
for letter, count in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    if determined_count == count:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")