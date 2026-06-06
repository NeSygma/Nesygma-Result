from z3 import *

# Create solver
solver = Solver()

# Define days as integers: 0=Monday, 1=Tuesday, 2=Wednesday
days = [0, 1, 2]

# Create witness variables
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

witnesses = [Franco, Garcia, Hong, Iturbe, Jackson]

# Base constraints
# Each witness testifies on exactly one day (0, 1, or 2)
for w in witnesses:
    solver.add(Or([w == d for d in days]))

# Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# Iturbe testifies on Wednesday (day 2)
solver.add(Iturbe == 2)

# Exactly two witnesses testify on Tuesday (day 1)
# Count how many witnesses are on Tuesday
tuesday_count = Sum([If(w == 1, 1, 0) for w in witnesses])
solver.add(tuesday_count == 2)

# Hong does not testify on Monday (day 0)
solver.add(Hong != 0)

# At least one witness testifies on Monday (day 0)
monday_count = Sum([If(w == 0, 1, 0) for w in witnesses])
solver.add(monday_count >= 1)

# Define option constraints
# Option A: Franco is the only witness scheduled to testify on Monday
opt_a = And(
    Franco == 0,  # Franco on Monday
    Garcia != 0,  # Others not on Monday
    Hong != 0,
    Iturbe != 0,  # Iturbe is on Wednesday anyway
    Jackson != 0
)

# Option B: Franco is scheduled to testify on the same day as Iturbe
opt_b = (Franco == Iturbe)  # Iturbe is on Wednesday, so Franco would be on Wednesday

# Option C: Garcia and Hong are both scheduled to testify on Tuesday
opt_c = And(Garcia == 1, Hong == 1)

# Option D: Garcia is the only witness scheduled to testify on Monday AND Hong is one of two witnesses scheduled to Wednesday
opt_d = And(
    Garcia == 0,  # Garcia on Monday
    Franco != 0,  # Others not on Monday
    Hong != 0,
    Iturbe != 0,  # Iturbe is on Wednesday anyway
    Jackson != 0,
    # Hong is one of two witnesses on Wednesday
    Hong == 2,
    # Exactly two witnesses on Wednesday
    Sum([If(w == 2, 1, 0) for w in witnesses]) == 2
)

# Option E: Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to Monday
opt_e = And(
    Jackson == 1,  # Jackson on Tuesday
    monday_count == 2  # Exactly two on Monday
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")