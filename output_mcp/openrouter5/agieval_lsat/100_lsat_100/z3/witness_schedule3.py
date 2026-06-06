from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = ['F', 'G', 'H', 'I', 'J']

day = {w: Int(f'day_{w}') for w in witnesses}

solver = Solver()

# Domain constraints: each day is 0, 1, or 2
for w in witnesses:
    solver.add(day[w] >= 0, day[w] <= 2)

# Franco does not testify on the same day as Garcia
solver.add(day['F'] != day['G'])

# Iturbe testifies on Wednesday (day 2)
solver.add(day['I'] == 2)

# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(day[w] == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday (day 0)
solver.add(day['H'] != 0)

# At least one witness testifies on Monday (day 0)
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition: Jackson is scheduled to testify on Wednesday (day 2)
solver.add(day['J'] == 2)

# Now evaluate each option using the required skeleton
found_options = []

# Option A: Franco on Monday
opt_a = (day['F'] == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia on Monday
opt_b = (day['G'] == 0)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Exactly one witness on Monday
opt_c = (Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Exactly two witnesses on Monday
opt_d = (Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Garcia same day as Hong
opt_e = (day['G'] == day['H'])
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
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