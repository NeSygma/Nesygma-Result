from z3 import *

# Witnesses
witnesses = ['F', 'G', 'H', 'I', 'J']
# Days: 0: Mon, 1: Tue, 2: Wed
day = {w: Int(w) for w in witnesses}

solver = Solver()

# Each witness testifies on exactly one day
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

# Question condition: Jackson is scheduled to testify on Wednesday.
solver.add(day['J'] == 2)

# Options
# (A) Franco is scheduled to testify on Monday.
# (B) Garcia is scheduled to testify on Monday.
# (C) Exactly one witness is scheduled to testify on Monday.
# (D) Exactly two witnesses are scheduled to testify on Monday.
# (E) Garcia is scheduled to testify on the same day as Hong.

options = [
    ("A", day['F'] == 0),
    ("B", day['G'] == 0),
    ("C", Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1),
    ("D", Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 2),
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