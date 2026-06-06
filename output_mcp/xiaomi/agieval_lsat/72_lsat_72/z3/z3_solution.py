from z3 import *

solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=Morning, 1=Afternoon
# Each assistant assigned to a (day, time) pair
# There are 6 sessions: 3 days × 2 times

assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

# For each assistant, assign a day (0,1,2) and a time (0,1)
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All assistants must be in different (day, time) slots - i.e., all 6 slots filled
# This means all (day, time) pairs are distinct
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        solver.add(Or(day[assistants[i]] != day[assistants[j]], 
                       time[assistants[i]] != time[assistants[j]]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Additional constraint from the question: Lan does NOT lead a Wednesday session
solver.add(day['Lan'] != 0)

# Now check each answer option: who MUST lead a Thursday session?
# Option A: Rebecca leads Thursday
# Option B: Olivia leads Thursday
# Option C: Nessa leads Thursday
# Option D: Kevin leads Thursday
# Option E: Julio leads Thursday

options = {
    "A": day['Rebecca'] == 1,
    "B": day['Olivia'] == 1,
    "C": day['Nessa'] == 1,
    "D": day['Kevin'] == 1,
    "E": day['Julio'] == 1,
}

# To find who MUST lead Thursday, we check: for each option, is it possible 
# that the assistant does NOT lead Thursday? If not possible (unsat), they MUST.

must_lead_thursday = []
for letter, assistant_day1 in options.items():
    solver.push()
    solver.add(Not(assistant_day1))  # Try to make them NOT on Thursday
    result = solver.check()
    if result == unsat:
        # Cannot avoid Thursday -> MUST lead Thursday
        must_lead_thursday.append(letter)
    solver.pop()

print(f"Must lead Thursday: {must_lead_thursday}")

if len(must_lead_thursday) == 1:
    print("STATUS: sat")
    print(f"answer:{must_lead_thursday[0]}")
elif len(must_lead_thursday) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must lead Thursday {must_lead_thursday}")
else:
    print("STATUS: unsat")
    print("Refine: No option must lead Thursday")