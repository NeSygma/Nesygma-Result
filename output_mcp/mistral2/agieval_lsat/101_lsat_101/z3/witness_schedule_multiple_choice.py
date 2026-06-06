from z3 import *

solver = Solver()

# Days: Monday (0), Tuesday (1), Wednesday (2)
# Witnesses: Franco (0), Garcia (1), Hong (2), Iturbe (3), Jackson (4)

# Assign each witness to a day
days = [Int(f"day_{witness}") for witness in range(5)]

# Each witness testifies on exactly one day
for i in range(5):
    solver.add(days[i] >= 0, days[i] <= 2)

# Iturbe testifies on Wednesday (day 2)
solver.add(days[3] == 2)

# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(d == 1, 1, 0) for d in days]) == 2)

# At least one witness testifies on Monday (day 0)
solver.add(Sum([If(d == 0, 1, 0) for d in days]) >= 1)

# Hong does not testify on Monday (day 0)
solver.add(days[2] != 0)

# Franco does not testify on the same day as Garcia
solver.add(days[0] != days[1])

# Jackson is the only witness scheduled to testify on Monday (day 0)
solver.add(days[4] == 0)
solver.add(Sum([If(d == 0, 1, 0) for d in days]) == 1)

# Now, evaluate each option to see which one is valid under the constraints
found_options = []

# Option A: Franco is scheduled to testify on Wednesday (day 2)
solver.push()
solver.add(days[0] == 2)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is valid")
else:
    print("Option A is invalid")
solver.pop()

# Option B: Hong is scheduled to testify on Tuesday (day 1)
solver.push()
solver.add(days[2] == 1)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is valid")
else:
    print("Option B is invalid")
solver.pop()

# Option C: Garcia is scheduled to testify on Tuesday (day 1)
solver.push()
solver.add(days[1] == 1)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is valid")
else:
    print("Option C is invalid")
solver.pop()

# Option D: Franco is scheduled to testify on the same day as Hong
solver.push()
solver.add(days[0] == days[2])
if solver.check() == sat:
    found_options.append("D")
    print("Option D is valid")
else:
    print("Option D is invalid")
solver.pop()

# Option E: Garcia is scheduled to testify on the same day as Hong
solver.push()
solver.add(days[1] == days[2])
if solver.check() == sat:
    found_options.append("E")
    print("Option E is valid")
else:
    print("Option E is invalid")
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