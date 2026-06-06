from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']
days = ['Monday', 'Tuesday', 'Wednesday']

# Each witness assigned to exactly one day
day = [Int(f'day_{w}') for w in range(5)]
for i in range(5):
    solver.add(day[i] >= 0, day[i] <= 2)

# Constraint 1: Franco and Garcia not on same day
solver.add(day[0] != day[1])

# Constraint 2: Iturbe on Wednesday
solver.add(day[3] == 2)

# Constraint 3: Exactly two witnesses on Tuesday
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

# Constraint 4: Hong not on Monday
solver.add(day[2] != 0)

# Constraint 5: At least one witness on Monday
solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Additional condition: Franco on same day as Hong
solver.add(day[0] == day[2])

# Define answer choice constraints
# (A) Franco is on Wednesday
opt_a = (day[0] == 2)
# (B) Garcia is on Monday
opt_b = (day[1] == 0)
# (C) Garcia is on Wednesday
opt_c = (day[1] == 2)
# (D) Hong is on Tuesday
opt_d = (day[2] == 1)
# (E) Iturbe is the only witness on Wednesday
opt_e = And(day[3] == 2, 
            And([day[i] != 2 for i in range(5) if i != 3]))

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

# Also print a sample valid schedule for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample valid schedule:")
    for i in range(5):
        print(f"  {witnesses[i]}: {days[m[day[i]].as_long()]}")
solver.pop()