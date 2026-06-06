from z3 import *

# Base constraints
witnesses = ['F','G','H','I','J']
# Days: 0=Mon,1=Tue,2=Wed
day = {w: Int(f'day_{w}') for w in witnesses}
solver = Solver()
for w in witnesses:
    solver.add(day[w] >= 0, day[w] <= 2)
# Each witness exactly one day already via int var domain
# Constraints
solver.add(day['F'] != day['G'])  # Franco not same day as Garcia
solver.add(day['I'] == 2)  # Iturbe Wednesday (2)
solver.add(day['J'] == 2)  # Jackson Wednesday (given premise)
# Exactly two witnesses on Tuesday (day==1)
solver.add(Sum([If(day[w] == 1, 1, 0) for w in witnesses]) == 2)
# Hong not Monday
solver.add(day['H'] != 0)
# At least one witness on Monday
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Define option constraints (as statements that must be true)
# A: Franco Monday
opt_a = day['F'] == 0
# B: Garcia Monday
opt_b = day['G'] == 0
# C: Exactly one witness Monday
opt_c = Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1
# D: Exactly two witnesses Monday
opt_d = Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 2
# E: Garcia same day as Hong
opt_e = day['G'] == day['H']

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine forced options (those not found when requiring the statement)
all_letters = {letter for letter, _ in options}
forced = all_letters - set(found_options)
if len(forced) == 1:
    ans = forced.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
elif len(found_options) == 1:
    # fallback if only one option can be true
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Options found {found_options}, forced {forced}")