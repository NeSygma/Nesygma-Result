from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = ['F', 'G', 'H', 'I', 'J']
days = [0, 1, 2]  # Mon=0, Tue=1, Wed=2

# Each witness testifies on exactly one day
day_of = {w: Int(f'day_{w}') for w in witnesses}

solver = Solver()

# Domain constraints: each day is 0, 1, or 2
for w in witnesses:
    solver.add(day_of[w] >= 0, day_of[w] <= 2)

# Franco does not testify on the same day as Garcia
solver.add(day_of['F'] != day_of['G'])

# Iturbe testifies on Wednesday (day 2)
solver.add(day_of['I'] == 2)

# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(day_of[w] == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday (day 0)
solver.add(day_of['H'] != 0)

# At least one witness testifies on Monday (day 0)
solver.add(Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Now evaluate each option

# Option A: Franco is the only witness scheduled to testify on Monday.
# That means Franco is on Monday, and no one else is on Monday.
opt_a = And(day_of['F'] == 0, Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 1)

# Option B: Franco is scheduled to testify on the same day as Iturbe.
# Iturbe is on Wednesday (day 2), so Franco must also be on Wednesday.
opt_b = (day_of['F'] == day_of['I'])  # i.e., day_of['F'] == 2

# Option C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(day_of['G'] == 1, day_of['H'] == 1)

# Option D: Garcia is the only witness scheduled to testify on Monday
# and Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d = And(
    day_of['G'] == 0,
    Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 1,
    day_of['H'] == 2,
    Sum([If(day_of[w] == 2, 1, 0) for w in witnesses]) == 2
)

# Option E: Jackson is scheduled to testify on Tuesday
# and two witnesses are scheduled to testify on Monday.
opt_e = And(
    day_of['J'] == 1,
    Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 2
)

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