from z3 import *

solver = Solver()

students = ['G', 'H', 'I', 'K', 'L', 'N', 'O', 'R']
day = {s: Int(f'day_{s}') for s in students}
time = {s: Int(f'time_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(Or(day[s] == -1, day[s] == 0, day[s] == 1, day[s] == 2))
    solver.add(Or(time[s] == -1, time[s] == 0, time[s] == 1))
    # If day is -1 (no report), time must be -1
    solver.add(Implies(day[s] == -1, time[s] == -1))
    # If day is not -1, time must be 0 or 1
    solver.add(Implies(day[s] != -1, Or(time[s] == 0, time[s] == 1)))

# Exactly 6 students give reports (day != -1)
solver.add(Sum([If(day[s] != -1, 1, 0) for s in students]) == 6)

# Exactly 2 reports per day (Monday=0, Tuesday=1, Wednesday=2)
for d in range(3):
    solver.add(Sum([If(day[s] == d, 1, 0) for s in students]) == 2)

# Each day has exactly one morning (time=0) and one afternoon (time=1) report
for d in range(3):
    solver.add(Sum([If(And(day[s] == d, time[s] == 0), 1, 0) for s in students]) == 1)
    solver.add(Sum([If(And(day[s] == d, time[s] == 1), 1, 0) for s in students]) == 1)

# Condition 1: Tuesday (day=1) is the only day George can give a report
solver.add(Or(day['G'] == -1, day['G'] == 1))

# Condition 2: Neither Olivia nor Robert can give an afternoon report (time=1)
solver.add(Implies(day['O'] != -1, time['O'] == 0))
solver.add(Implies(day['R'] != -1, time['R'] == 0))

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday (day=2)
solver.add(Implies(And(day['N'] != -1, day['N'] != 2),
                   And(day['H'] == day['N'] + 1,
                       day['I'] == day['N'] + 1)))

# Quick check to make sure the base constraints are satisfiable
check_result = solver.check()
print(f"Base constraints: {check_result}")
if check_result == sat:
    m = solver.model()
    for s in students:
        print(f"  {s}: day={m[day[s]]}, time={m[time[s]]}")
print()

# Now evaluate each option
options = [("A", ('G', 'L')), ("B", ('H', 'N')), ("C", ('I', 'R')), ("D", ('K', 'N')), ("E", ('O', 'K'))]
found_options = []

for letter, (a, b) in options:
    solver.push()
    # Add constraint: both give reports on the same day that is NOT Wednesday
    solver.add(day[a] != -1)  # A gives a report
    solver.add(day[b] != -1)  # B gives a report
    solver.add(day[a] == day[b])  # Same day
    solver.add(day[a] != 2)  # Not Wednesday
    
    res = solver.check()
    print(f"Option {letter} ({a},{b}) same day not Wed: {res}")
    if res == unsat:
        found_options.append(letter)
    elif res == sat:
        m = solver.model()
        print(f"  Found: day[{a}]={m[day[a]]}, day[{b}]={m[day[b]]}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")