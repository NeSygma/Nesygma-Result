from z3 import *

# Declare symbolic variables for each witness's day
# Days: 0=Monday, 1=Tuesday, 2=Wednesday
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

solver = Solver()

# Base constraints
# Each witness testifies on exactly one day (0, 1, or 2)
solver.add(Franco >= 0, Franco <= 2)
solver.add(Garcia >= 0, Garcia <= 2)
solver.add(Hong >= 0, Hong <= 2)
solver.add(Iturbe >= 0, Iturbe <= 2)
solver.add(Jackson >= 0, Jackson <= 2)

# Constraint 1: Franco does not testify on the same day that Garcia testifies
solver.add(Franco != Garcia)

# Constraint 2: Iturbe testifies on Wednesday (day 2)
solver.add(Iturbe == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday (day 1)
# Count how many witnesses are on day 1
tuesday_count = Sum([If(Franco == 1, 1, 0),
                     If(Garcia == 1, 1, 0),
                     If(Hong == 1, 1, 0),
                     If(Iturbe == 1, 1, 0),
                     If(Jackson == 1, 1, 0)])
solver.add(tuesday_count == 2)

# Constraint 4: Hong does not testify on Monday (day 0)
solver.add(Hong != 0)

# Constraint 5: At least one witness testifies on Monday (day 0)
monday_count = Sum([If(Franco == 0, 1, 0),
                    If(Garcia == 0, 1, 0),
                    If(Hong == 0, 1, 0),
                    If(Iturbe == 0, 1, 0),
                    If(Jackson == 0, 1, 0)])
solver.add(monday_count >= 1)

# Now evaluate each answer choice
# For each choice, we'll add constraints that match the schedule
# and check if it's consistent with the base constraints

found_options = []

# Option A: Monday: Franco, Tuesday: Hong and Iturbe, Wednesday: Garcia and Jackson
opt_a = And(
    Franco == 0,  # Monday
    Hong == 1,    # Tuesday
    Iturbe == 1,  # Tuesday
    Garcia == 2,  # Wednesday
    Jackson == 2  # Wednesday
)

# Option B: Monday: Franco and Hong, Tuesday: Iturbe and Jackson, Wednesday: Garcia
opt_b = And(
    Franco == 0,  # Monday
    Hong == 0,    # Monday
    Iturbe == 1,  # Tuesday
    Jackson == 1, # Tuesday
    Garcia == 2   # Wednesday
)

# Option C: Monday: Garcia, Tuesday: Franco and Iturbe, Wednesday: Hong and Jackson
opt_c = And(
    Garcia == 0,  # Monday
    Franco == 1,  # Tuesday
    Iturbe == 1,  # Tuesday
    Hong == 2,    # Wednesday
    Jackson == 2  # Wednesday
)

# Option D: Monday: Garcia and Jackson, Tuesday: Franco and Hong, Wednesday: Iturbe
opt_d = And(
    Garcia == 0,  # Monday
    Jackson == 0, # Monday
    Franco == 1,  # Tuesday
    Hong == 1,    # Tuesday
    Iturbe == 2   # Wednesday
)

# Option E: Monday: Garcia and Jackson, Tuesday: Hong, Wednesday: Franco and Iturbe
opt_e = And(
    Garcia == 0,  # Monday
    Jackson == 0, # Monday
    Hong == 1,    # Tuesday
    Franco == 2,  # Wednesday
    Iturbe == 2   # Wednesday
)

# Test each option
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")