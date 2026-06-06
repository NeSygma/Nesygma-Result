from z3 import *

G, H, I, K, L, N, O, R = range(8)
students = 8

solver = Solver()

# gives[i]: whether student i gives a report
gives = [Bool(f'gives_{i}') for i in range(students)]

# day[i]: 0=Mon, 1=Tue, 2=Wed - only meaningful if gives[i] is True
day = [Int(f'day_{i}') for i in range(students)]
for i in range(students):
    solver.add(Implies(gives[i], And(day[i] >= 0, day[i] <= 2)))

# time[i]: 0=AM, 1=PM - only meaningful if gives[i] is True
time = [Int(f'time_{i}') for i in range(students)]
for i in range(students):
    solver.add(Implies(gives[i], And(time[i] >= 0, time[i] <= 1)))

# Constraint 1: Exactly 6 students give reports
solver.add(Sum([If(gives[i], 1, 0) for i in range(students)]) == 6)

# Constraint 2: Exactly 2 reports per day, one AM and one PM
for d in range(3):
    solver.add(Sum([If(And(gives[i], day[i] == d), 1, 0) for i in range(students)]) == 2)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 0), 1, 0) for i in range(students)]) == 1)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 1), 1, 0) for i in range(students)]) == 1)

# Constraint 3: Tuesday is the only day George can give a report
solver.add(Implies(gives[G], day[G] == 1))

# Constraint 4: Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(gives[O], time[O] != 1))
solver.add(Implies(gives[R], time[R] != 1))

# Constraint 5: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
solver.add(Implies(And(gives[N], day[N] == 0), 
                   And(gives[H], day[H] == 1, gives[I], day[I] == 1)))
solver.add(Implies(And(gives[N], day[N] == 1), 
                   And(gives[H], day[H] == 2, gives[I], day[I] == 2)))

# First, let's verify the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
if result == sat:
    m = solver.model()
    name_map = {0: "George", 1: "Helen", 2: "Irving", 3: "Kyle", 4: "Lenore", 5: "Nina", 6: "Olivia", 7: "Robert"}
    day_map = {0: "Mon", 1: "Tue", 2: "Wed"}
    time_map = {0: "AM", 1: "PM"}
    print("Base model (satisfiable):")
    for i in range(students):
        if m.eval(gives[i]):
            print(f"  {name_map[i]}: {day_map[m.eval(day[i]).as_long()]} {time_map[m.eval(time[i]).as_long()]}")
        else:
            print(f"  {name_map[i]}: no report")
elif result == unsat:
    print("Base constraints are UNSAT!")
else:
    print(f"Base constraints: {result}")

# Test each option
options = [
    ("A", (G, L)),
    ("B", (H, N)),
    ("C", (I, R)),
    ("D", (K, N)),
    ("E", (O, K)),
]

found_options = []

for letter, (s1, s2) in options:
    solver.push()
    # Constraint: s1 and s2 give reports on the same day
    solver.add(gives[s1])
    solver.add(gives[s2])
    solver.add(day[s1] == day[s2])
    
    # Check if they MUST be on Wednesday
    # Try to find a model where they're on the same day but NOT Wednesday
    solver.add(day[s1] != 2)
    
    result = solver.check()
    if result == unsat:
        # No way to have them on the same day that isn't Wednesday
        found_options.append(letter)
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