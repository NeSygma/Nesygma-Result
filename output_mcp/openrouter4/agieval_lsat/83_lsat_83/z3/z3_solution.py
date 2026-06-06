from z3 import *

solver = Solver()

# Variables: zone assignments (1, 2, or 3)
k, m, p, q, s, t, u = Ints('k m p q s t u')

# Domain constraints: each rep works in exactly one zone
reps = [k, m, p, q, s, t, u]
for r in reps:
    solver.add(Or([r == z for z in [1, 2, 3]]))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Xor(p == 1, t == 1))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Xor(t == 2, u == 2))

# Condition 3: Parra and Quinn work in the same sales zone.
solver.add(p == q)

# Condition 4: Stuckey and Udall work in the same sales zone.
solver.add(s == u)

# Condition 5: More reps in Zone 3 than in Zone 2.
count_zone2 = Sum([If(r == 2, 1, 0) for r in reps])
count_zone3 = Sum([If(r == 3, 1, 0) for r in reps])
solver.add(count_zone3 > count_zone2)

# Additional condition from the question: more reps in Zone 1 than in Zone 3.
count_zone1 = Sum([If(r == 1, 1, 0) for r in reps])
solver.add(count_zone1 > count_zone3)

# Now test each option
found_options = []

options = [
    ("A", k == 2),
    ("B", m == 2),
    ("C", p == 3),
    ("D", t == 1),
    ("E", u == 3)
]

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