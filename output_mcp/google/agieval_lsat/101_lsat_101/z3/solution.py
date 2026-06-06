from z3 import *

# Witnesses
witnesses = ['F', 'G', 'H', 'I', 'J']
# Days: 0=Mon, 1=Tue, 2=Wed
day = {w: Int(f'day_{w}') for w in witnesses}

solver = Solver()

# Domain constraints
for w in witnesses:
    solver.add(day[w] >= 0, day[w] <= 2)

# 1. Franco does not testify on the same day that Garcia testifies.
solver.add(day['F'] != day['G'])

# 2. Iturbe testifies on Wednesday.
solver.add(day['I'] == 2)

# 3. Exactly two witnesses testify on Tuesday.
solver.add(Sum([If(day[w] == 1, 1, 0) for w in witnesses]) == 2)

# 4. Hong does not testify on Monday.
solver.add(day['H'] != 0)

# 5. At least one witness testifies on Monday.
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Question constraint: Jackson is the only witness on Monday.
solver.push()
solver.add(day['J'] == 0)
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1)

# Answer choices
# (A) Franco is scheduled to testify on Wednesday.
# (B) Hong is scheduled to testify on Tuesday.
# (C) Garcia is scheduled to testify on Tuesday.
# (D) Franco is scheduled to testify on the same day as Hong.
# (E) Garcia is scheduled to testify on the same day as Hong.

options = [
    ("A", day['F'] == 2),
    ("B", day['H'] == 1),
    ("C", day['G'] == 1),
    ("D", day['F'] == day['H']),
    ("E", day['G'] == day['H'])
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
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