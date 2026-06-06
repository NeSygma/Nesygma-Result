from z3 import *

solver = Solver()

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
n = 8
gives = [Bool(f'gives_{i}') for i in range(n)]
day = [Int(f'day_{i}') for i in range(n)]
time = [Int(f'time_{i}') for i in range(n)]

# Exactly 6 give reports
solver.add(Sum([If(gives[i], 1, 0) for i in range(n)]) == 6)

# Domain constraints for those who give
for i in range(n):
    solver.add(Implies(gives[i], And(day[i] >= 0, day[i] <= 2)))
    solver.add(Implies(gives[i], And(time[i] >= 0, time[i] <= 1)))

# Exactly 2 reports per day (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([If(And(gives[i], day[i] == d), 1, 0) for i in range(n)]) == 2)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Constraint 1: George can only give on Tuesday (day=1)
solver.add(Implies(gives[0], day[0] == 1))

# Constraint 2: Olivia and Robert cannot give afternoon reports
solver.add(Implies(gives[6], time[6] == 0))
solver.add(Implies(gives[7], time[7] == 0))

# Constraint 3: If Nina gives on Monday (day=0) or Tuesday (day=1),
# then on the next day Helen and Irving must both give reports
for d in [0, 1]:
    solver.add(Implies(And(gives[5], day[5] == d),
                       And(gives[1], day[1] == d+1, gives[2], day[2] == d+1)))

# Given condition: Helen, Kyle, Lenore give the three morning reports
solver.add(gives[1])  # Helen gives
solver.add(gives[3])  # Kyle gives
solver.add(gives[4])  # Lenore gives

solver.add(time[1] == 0)  # Helen morning
solver.add(time[3] == 0)  # Kyle morning
solver.add(time[4] == 0)  # Lenore morning

# They are on different days
solver.add(Distinct([day[1], day[3], day[4]]))

# Critical inference:
# Olivia and Robert can only give morning reports. But all 3 morning slots
# are taken by Helen, Kyle, Lenore. So Olivia and Robert cannot give.
solver.add(Not(gives[6]))
solver.add(Not(gives[7]))

# Exactly 6 give reports: Helen, Kyle, Lenore (3 morning) + 3 afternoon
# The remaining people who could give are {George, Irving, Nina, Olivia, Robert}
# Olivia and Robert are out. So George, Irving, Nina must all give afternoon reports.
solver.add(gives[0])  # George gives
solver.add(gives[2])  # Irving gives
solver.add(gives[5])  # Nina gives

solver.add(time[0] == 1)  # George afternoon
solver.add(time[2] == 1)  # Irving afternoon
solver.add(time[5] == 1)  # Nina afternoon

# Now let's look at the Nina constraint more carefully.
# If Nina gives on Monday (day=0), then on Tuesday Helen AND Irving must give.
# But Tuesday has slots: morning (one of Helen/Kyle/Lenore) and afternoon (George).
# If Helen gives on Tuesday, that uses the Tuesday morning slot.
# Then Irving would need the Tuesday afternoon slot, but that's taken by George.
# So this creates a contradiction.
# 
# If Nina gives on Tuesday (day=1), then on Wednesday Helen AND Irving must give.
# Wednesday has slots: morning (one of Helen/Kyle/Lenore) and afternoon (Nina).
# If Helen gives on Wednesday, that uses the Wednesday morning slot.
# Then Irving would need the Wednesday afternoon slot, but that's taken by Nina.
# So this also creates a contradiction.
#
# Therefore, Nina MUST give on Wednesday (day=2).
solver.add(day[5] == 2)  # Nina gives on Wednesday

# Now with Nina on Wednesday, let's verify constraints:
# Since Nina gives on Wednesday, the "unless" clause applies, so no further constraint.
# Tuesday afternoon must be George (since George can only give Tuesday).
solver.add(day[0] == 1)  # George on Tuesday

# Monday afternoon must be Irving (since Irving, George, Nina are the only afternoon speakers)
# and George is Tuesday, Nina is Wednesday, so Irving must be Monday.
solver.add(day[2] == 0)  # Irving on Monday

# Now let's check the model
result = solver.check()
print(f"Model check: {result}")

if result == sat:
    m = solver.model()
    for i, name in enumerate(["George","Helen","Irving","Kyle","Lenore","Nina","Olivia","Robert"]):
        g = m.eval(gives[i])
        if g:
            d = m.eval(day[i])
            t = m.eval(time[i])
            print(f"{name}: day={'Mon' if d==0 else 'Tue' if d==1 else 'Wed'}, time={'morning' if t==0 else 'afternoon'}")
        else:
            print(f"{name}: no report")

print("\n--- Now evaluating options ---")

# Evaluate each option individually
found_options = []

# Option A: Helen gives a report on Monday
solver.push()
solver.add(day[1] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Irving gives a report on Monday
solver.push()
solver.add(gives[2], day[2] == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Irving gives a report on Wednesday
solver.push()
solver.add(gives[2], day[2] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kyle gives a report on Tuesday
solver.push()
solver.add(day[3] == 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Kyle gives a report on Wednesday
solver.push()
solver.add(day[3] == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")