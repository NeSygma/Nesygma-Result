from z3 import *

solver = Solver()

# Variables: day assignment for each witness (0=Monday, 1=Tuesday, 2=Wednesday)
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

witnesses = [Franco, Garcia, Hong, Iturbe, Jackson]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

# Each witness testifies on exactly one day (0, 1, or 2)
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# Iturbe testifies on Wednesday
solver.add(Iturbe == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday
solver.add(Hong != 0)

# At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Jackson is the only witness scheduled to testify on Monday
solver.add(Jackson == 0)
solver.add(Franco != 0)
solver.add(Garcia != 0)
solver.add(Hong != 0)
solver.add(Iturbe != 0)

# Define option constraints
# (A) Franco is scheduled to testify on Wednesday
opt_a = (Franco == 2)

# (B) Hong is scheduled to testify on Tuesday
opt_b = (Hong == 1)

# (C) Garcia is scheduled to testify on Tuesday
opt_c = (Garcia == 1)

# (D) Franco is scheduled to testify on the same day as Hong
opt_d = (Franco == Hong)

# (E) Garcia is scheduled to testify on the same day as Hong
opt_e = (Garcia == Hong)

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