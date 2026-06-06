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

# The question asks which CANNOT be true.
# We need to find which option is UNSATISFIABLE (cannot be true).
# Let's check each option individually.

options = {
    "A": And(
        day[0] == 0,  # Franco on Monday
        Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 1  # Only one on Monday
    ),
    "B": (day[0] == day[3]),  # Franco same day as Iturbe (Wednesday)
    "C": And(day[1] == 1, day[2] == 1),  # Garcia and Hong both on Tuesday
    "D": And(
        day[1] == 0,  # Garcia on Monday
        Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 1,  # Only one on Monday
        day[2] == 2,  # Hong on Wednesday
        Sum([If(day[w] == 2, 1, 0) for w in range(5)]) == 2  # Exactly two on Wednesday
    ),
    "E": And(
        day[4] == 1,  # Jackson on Tuesday
        Sum([If(day[w] == 0, 1, 0) for w in range(5)]) == 2  # Two on Monday
    )
}

# Check which options CAN be true (satisfiable)
can_be_true = []
cannot_be_true = []

for letter, constr in options.items():
    s = Solver()
    # Add all base constraints
    for w in range(5):
        s.add(Or(day[w] == 0, day[w] == 1, day[w] == 2))
    s.add(day[0] != day[1])
    s.add(day[3] == 2)
    s.add(Sum([If(day[w] == 1, 1, 0) for w in range(5)]) == 2)
    s.add(day[2] != 0)
    s.add(Sum([If(day[w] == 0, 1, 0) for w in range(5)]) >= 1)
    
    # Add the option constraint
    s.add(constr)
    
    if s.check() == sat:
        can_be_true.append(letter)
    else:
        cannot_be_true.append(letter)

print("Options that CAN be true:", can_be_true)
print("Options that CANNOT be true:", cannot_be_true)

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be true")