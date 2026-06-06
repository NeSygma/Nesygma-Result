from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = [Int(f'w_{i}') for i in range(5)]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

# Each witness testifies on exactly one day (0=Mon, 1=Tue, 2=Wed)
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Condition: Franco does not testify on the same day as Garcia
solver.add(witnesses[0] != witnesses[1])

# Condition: Iturbe testifies on Wednesday
solver.add(witnesses[3] == 2)

# Condition: Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Condition: Hong does not testify on Monday
solver.add(witnesses[2] != 0)

# Condition: At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition: Jackson testifies on Wednesday
solver.add(witnesses[4] == 2)

# Define option constraints
# (A) Franco is scheduled to testify on Monday
opt_a = (witnesses[0] == 0)

# (B) Garcia is scheduled to testify on Monday
opt_b = (witnesses[1] == 0)

# (C) Exactly one witness is scheduled to testify on Monday
opt_c = (Sum([If(w == 0, 1, 0) for w in witnesses]) == 1)

# (D) Exactly two witnesses are scheduled to testify on Monday
opt_d = (Sum([If(w == 0, 1, 0) for w in witnesses]) == 2)

# (E) Garcia is scheduled to testify on the same day as Hong
opt_e = (witnesses[1] == witnesses[2])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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