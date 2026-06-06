from z3 import *

# Reps: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
reps = ['K', 'M', 'P', 'Q', 'S', 'T', 'U']
zones = {r: Int(f'{r}_zone') for r in reps}

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
def count_in_zone(z):
    return Sum([If(zones[r] == z, 1, 0) for r in reps])

count1 = count_in_zone(1)
count2 = count_in_zone(2)
count3 = count_in_zone(3)

solver.add(count3 > count2)

# Q: If more sales representatives work in Zone 1 than in Zone 3, then which one of the following could be true?
solver.add(count1 > count3)

# Options
options = [
    ("A", zones['K'] == 2),
    ("B", zones['M'] == 2),
    ("C", zones['P'] == 3),
    ("D", zones['T'] == 1),
    ("E", zones['U'] == 3)
]

found_options = []
for letter, constr in options:
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