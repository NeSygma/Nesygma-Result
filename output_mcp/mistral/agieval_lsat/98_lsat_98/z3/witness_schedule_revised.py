from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each witness's day
# 0 = Monday, 1 = Tuesday, 2 = Wednesday
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

# Base constraints
solver = Solver()

# Each witness testifies on exactly one day
solver.add(Or(Franco == 0, Franco == 1, Franco == 2))
solver.add(Or(Garcia == 0, Garcia == 1, Garcia == 2))
solver.add(Or(Hong == 0, Hong == 1, Hong == 2))
solver.add(Or(Iturbe == 0, Iturbe == 1, Iturbe == 2))
solver.add(Or(Jackson == 0, Jackson == 1, Jackson == 2))

# Iturbe testifies on Wednesday
solver.add(Iturbe == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(Franco == 1, 1, 0), If(Garcia == 1, 1, 0), If(Hong == 1, 1, 0), If(Iturbe == 1, 1, 0), If(Jackson == 1, 1, 0)]) == 2)

# Hong does not testify on Monday
solver.add(Hong != 0)

# At least one witness testifies on Monday
solver.add(Sum([If(Franco == 0, 1, 0), If(Garcia == 0, 1, 0), If(Hong == 0, 1, 0), If(Iturbe == 0, 1, 0), If(Jackson == 0, 1, 0)]) >= 1)

# Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# Evaluate each option
found_options = []

# Option A: Monday: Franco; Tuesday: Hong and Iturbe; Wednesday: Garcia and Jackson
# Iturbe must be on Wednesday, so this option is invalid.
solver.push()
solver.add(Franco == 0)
solver.add(Hong == 1)
solver.add(Iturbe == 1)  # This violates Iturbe == 2
solver.add(Garcia == 2)
solver.add(Jackson == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Monday: Franco and Hong; Tuesday: Iturbe and Jackson; Wednesday: Garcia
# Iturbe must be on Wednesday, so this option is invalid.
solver.push()
solver.add(Franco == 0)
solver.add(Hong == 0)
solver.add(Iturbe == 1)  # This violates Iturbe == 2
solver.add(Jackson == 1)
solver.add(Garcia == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Monday: Garcia; Tuesday: Franco and Iturbe; Wednesday: Hong and Jackson
# Iturbe must be on Wednesday, so this option is invalid.
solver.push()
solver.add(Garcia == 0)
solver.add(Franco == 1)
solver.add(Iturbe == 1)  # This violates Iturbe == 2
solver.add(Hong == 2)
solver.add(Jackson == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Monday: Garcia and Jackson; Tuesday: Franco and Hong; Wednesday: Iturbe
# Iturbe is on Wednesday, exactly two on Tuesday, Hong not on Monday, at least one on Monday, Franco and Garcia not on same day.
solver.push()
solver.add(Garcia == 0)
solver.add(Jackson == 0)
solver.add(Franco == 1)
solver.add(Hong == 1)
solver.add(Iturbe == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Monday: Garcia and Jackson; Tuesday: Hong; Wednesday: Franco and Iturbe
# Only one witness on Tuesday (Hong), but exactly two are required.
solver.push()
solver.add(Garcia == 0)
solver.add(Jackson == 0)
solver.add(Hong == 1)
solver.add(Franco == 2)
solver.add(Iturbe == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")