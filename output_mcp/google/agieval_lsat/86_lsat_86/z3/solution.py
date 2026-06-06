from z3 import *

# Reps: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
reps = ['K', 'M', 'P', 'Q', 'S', 'T', 'U']
zones = {r: Int(f'zone_{r}') for r in reps}

solver = Solver()

# Each rep works in exactly one zone (1, 2, or 3)
for r in reps:
    solver.add(zones[r] >= 1, zones[r] <= 3)

# 1. Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Xor(zones['P'] == 1, zones['T'] == 1))

# 2. Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Xor(zones['T'] == 2, zones['U'] == 2))

# 3. Parra and Quinn work in the same sales zone as each other.
solver.add(zones['P'] == zones['Q'])

# 4. Stuckey and Udall work in the same sales zone as each other.
solver.add(zones['S'] == zones['U'])

# 5. There are more of the sales representatives working in Zone 3 than in Zone 2.
count_z2 = Sum([If(zones[r] == 2, 1, 0) for r in reps])
count_z3 = Sum([If(zones[r] == 3, 1, 0) for r in reps])
solver.add(count_z3 > count_z2)

# Q: Quinn CANNOT work in the same sales zone as which one of the following?
# We want to find the option X such that (zones['Q'] == zones[X]) is UNSAT.

options = [
    ("A", 'K'),
    ("B", 'M'),
    ("C", 'S'),
    ("D", 'T'),
    ("E", 'U')
]

# The question asks for the one that CANNOT be true.
# So we look for the option where (zones['Q'] == zones[X]) is UNSAT.
# The skeleton logic provided expects us to find the "valid" option.
# If the question is "Which one CANNOT", the "valid" option is the one that is UNSAT.

found_options = []
for letter, rep in options:
    solver.push()
    solver.add(zones['Q'] == zones[rep])
    if solver.check() == unsat:
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