from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
day = {w: Int(f"day_{w}") for w in witnesses}

solver = Solver()

# Domain constraints: each witness testifies on one of the three days
for w in witnesses:
    solver.add(Or(day[w] == 0, day[w] == 1, day[w] == 2))

# Constraint 1: Franco does not testify on the same day as Garcia
solver.add(day["Franco"] != day["Garcia"])

# Constraint 2: Iturbe testifies on Wednesday (day 2)
solver.add(day["Iturbe"] == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday (day 1)
tuesday_count = Sum([If(day[w] == 1, 1, 0) for w in witnesses])
solver.add(tuesday_count == 2)

# Constraint 4: Hong does not testify on Monday (day 0)
solver.add(day["Hong"] != 0)

# Constraint 5: At least one witness testifies on Monday
monday_count = Sum([If(day[w] == 0, 1, 0) for w in witnesses])
solver.add(monday_count >= 1)

# Additional condition: Jackson is the only witness on Monday
solver.add(day["Jackson"] == 0)  # Jackson on Monday
# No other witness on Monday
for w in witnesses:
    if w != "Jackson":
        solver.add(day[w] != 0)

# Check base constraints first
print("Checking base constraints...")
if solver.check() == sat:
    print("Base constraints are satisfiable")
    m = solver.model()
    print("Example schedule:")
    for w in witnesses:
        print(f"  {w}: day {m[day[w]]}")
else:
    print("Base constraints are unsatisfiable")
    exit()

# Now test each option
# Option A: Franco is scheduled to testify on Wednesday
opt_a = (day["Franco"] == 2)

# Option B: Hong is scheduled to testify on Tuesday
opt_b = (day["Hong"] == 1)

# Option C: Garcia is scheduled to testify on Tuesday
opt_c = (day["Garcia"] == 1)

# Option D: Franco is scheduled to testify on the same day as Hong
opt_d = (day["Franco"] == day["Hong"])

# Option E: Garcia is scheduled to testify on the same day as Hong
opt_e = (day["Garcia"] == day["Hong"])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"\nOption {letter} is VALID:")
        m = solver.model()
        for w in witnesses:
            print(f"  {w}: day {m[day[w]]}")
    else:
        print(f"\nOption {letter} is INVALID")
    solver.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")