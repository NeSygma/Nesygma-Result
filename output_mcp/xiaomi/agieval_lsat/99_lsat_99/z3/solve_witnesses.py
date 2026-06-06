from z3 import *

solver = Solver()

# Witnesses: Franco(0), Garcia(1), Hong(2), Iturbe(3), Jackson(4)
# Days: Monday(0), Tuesday(1), Wednesday(2)
witnesses = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']
days = ['Monday', 'Tuesday', 'Wednesday']

# day[w] = which day witness w testifies (0=Mon, 1=Tue, 2=Wed)
day = [Int(f'day_{w}') for w in range(5)]

# Each witness testifies on exactly one day (domain constraint)
for w in range(5):
    solver.add(Or(day[w] == 0, day[w] == 1, day[w] == 2))

# Constraint 1: Franco does not testify on the same day as Garcia
solver.add(day[0] != day[1])

# Constraint 2: Iturbe testifies on Wednesday
solver.add(day[3] == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday
solver.add(Sum([If(day[w] == 1, 1, 0) for w in range(5)]) == 2)

# Constraint 4: Hong does not testify on Monday
solver.add(day[2] != 0)

# Constraint 5: At least one witness testifies on Monday
solver.add(Sum([If(day[w] == 0, 1, 0) for w in range(5)]) >= 1)

# Define option constraints
# (A) Franco is the only witness scheduled to testify on Monday
opt_a = And(
    day[0] == 0,  # Franco on Monday
    Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 1  # Only one on Monday
)

# (B) Franco is scheduled to testify on the same day as Iturbe
opt_b = (day[0] == day[3])

# (C) Garcia and Hong are both scheduled to testify on Tuesday
opt_c = And(day[1] == 1, day[2] == 1)

# (D) Garcia is the only witness on Monday AND Hong is one of two witnesses on Wednesday
opt_d = And(
    day[1] == 0,  # Garcia on Monday
    Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 1,  # Only one on Monday
    day[2] == 2,  # Hong on Wednesday
    Sum([If(day[w] == 2, 1, 0) for w in range(5)]) == 2  # Exactly two on Wednesday
)

# (E) Jackson testifies on Tuesday AND two witnesses testify on Monday
opt_e = And(
    day[4] == 1,  # Jackson on Tuesday
    Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 2  # Two on Monday
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