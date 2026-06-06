from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = [Int(f'w_{i}') for i in range(5)]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

# Each witness testifies on exactly one day (0=Mon, 1=Tue, 2=Wed)
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Franco does not testify on the same day as Garcia
solver.add(witnesses[0] != witnesses[1])

# Iturbe testifies on Wednesday
solver.add(witnesses[3] == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday
solver.add(witnesses[2] != 0)

# At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Define each option as constraints on witness assignments
# Option A: Mon: Franco, Tue: Hong+Iturbe, Wed: Garcia+Jackson
opt_a = And(
    witnesses[0] == 0,  # Franco Mon
    witnesses[2] == 1,  # Hong Tue
    witnesses[3] == 1,  # Iturbe Tue
    witnesses[1] == 2,  # Garcia Wed
    witnesses[4] == 2   # Jackson Wed
)

# Option B: Mon: Franco+Hong, Tue: Iturbe+Jackson, Wed: Garcia
opt_b = And(
    witnesses[0] == 0,  # Franco Mon
    witnesses[2] == 0,  # Hong Mon
    witnesses[3] == 1,  # Iturbe Tue
    witnesses[4] == 1,  # Jackson Tue
    witnesses[1] == 2   # Garcia Wed
)

# Option C: Mon: Garcia, Tue: Franco+Iturbe, Wed: Hong+Jackson
opt_c = And(
    witnesses[1] == 0,  # Garcia Mon
    witnesses[0] == 1,  # Franco Tue
    witnesses[3] == 1,  # Iturbe Tue
    witnesses[2] == 2,  # Hong Wed
    witnesses[4] == 2   # Jackson Wed
)

# Option D: Mon: Garcia+Jackson, Tue: Franco+Hong, Wed: Iturbe
opt_d = And(
    witnesses[1] == 0,  # Garcia Mon
    witnesses[4] == 0,  # Jackson Mon
    witnesses[0] == 1,  # Franco Tue
    witnesses[2] == 1,  # Hong Tue
    witnesses[3] == 2   # Iturbe Wed
)

# Option E: Mon: Garcia+Jackson, Tue: Hong, Wed: Franco+Iturbe
opt_e = And(
    witnesses[1] == 0,  # Garcia Mon
    witnesses[4] == 0,  # Jackson Mon
    witnesses[2] == 1,  # Hong Tue
    witnesses[0] == 2,  # Franco Wed
    witnesses[3] == 2   # Iturbe Wed
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