from z3 import *

# We have 6 lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
# 6 sessions: 3 days (Wed, Thu, Fri) x 2 times (morning, afternoon)
# Each session is led by a different assistant.

# Let's encode each assistant's session as a pair (day, time)
# day: 0=Wed, 1=Thu, 2=Fri
# time: 0=morning, 1=afternoon

# We'll use integer variables for each assistant's day and time.
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

solver = Solver()

# Domain constraints: day in {0,1,2}, time in {0,1}
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All sessions are different: each assistant gets a unique (day, time) pair
# We can encode this as: for any two distinct assistants, either day differs or time differs
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day.
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day.
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session.
solver.add(time['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's.
solver.add(day['Julio'] < day['Olivia'])

# Additional condition: Julio leads the Thursday afternoon session.
# Thursday = day 1, afternoon = time 1
solver.add(day['Julio'] == 1)
solver.add(time['Julio'] == 1)

# Now we need to determine: for how many of the OTHER lab assistants
# (i.e., everyone except Julio) can one determine which sessions they lead?
# That means: in ALL possible solutions, does a given assistant have a fixed
# (day, time) assignment?

# Let's enumerate all solutions and check which assistants have fixed assignments.

# First, let's collect all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for a in assistants:
        sol[a] = (m.eval(day[a]).as_long(), m.eval(time[a]).as_long())
    solutions.append(sol)
    # Block this solution
    solver.add(Or([day[a] != sol[a][0] for a in assistants] + 
                  [time[a] != sol[a][1] for a in assistants]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}:")
    for a in assistants:
        day_names = {0: "Wed", 1: "Thu", 2: "Fri"}
        time_names = {0: "morning", 1: "afternoon"}
        print(f"  {a}: {day_names[sol[a][0]]} {time_names[sol[a][1]]}")
    print()

# Now check which assistants (other than Julio) have fixed assignments across all solutions
other_assistants = [a for a in assistants if a != 'Julio']
fixed_count = 0
for a in other_assistants:
    first_val = solutions[0][a]
    if all(sol[a] == first_val for sol in solutions):
        fixed_count += 1
        print(f"{a} is FIXED at {first_val}")
    else:
        print(f"{a} is NOT fixed")

print(f"\nNumber of other assistants with determined sessions: {fixed_count}")

# Now map to answer choices
# The answer choices are: (A)one (B)two (C)three (D)four (E)five
# We need to find which option matches fixed_count

found_options = []
for letter, constr_val in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    solver.add(fixed_count == constr_val)
    # This is a bit different - we already computed fixed_count, so let's just check
    solver.pop()

# Actually, let's just directly determine the answer
if fixed_count == 1:
    print("STATUS: sat")
    print("answer:A")
elif fixed_count == 2:
    print("STATUS: sat")
    print("answer:B")
elif fixed_count == 3:
    print("STATUS: sat")
    print("answer:C")
elif fixed_count == 4:
    print("STATUS: sat")
    print("answer:D")
elif fixed_count == 5:
    print("STATUS: sat")
    print("answer:E")
else:
    print("STATUS: unsat")
    print("Refine: No matching option found")