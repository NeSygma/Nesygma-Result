from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for witnesses and their assigned days
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
days = ["Monday", "Tuesday", "Wednesday"]
day_to_int = {"Monday": 0, "Tuesday": 1, "Wednesday": 2}
int_to_day = {0: "Monday", 1: "Tuesday", 2: "Wednesday"}

# Assign each witness to a day (0=Monday, 1=Tuesday, 2=Wednesday)
assign = {w: Int(f"assign_{w}") for w in witnesses}

# Base constraints
solver = Solver()

# Each witness is assigned to exactly one day
for w in witnesses:
    solver.add(assign[w] >= 0, assign[w] <= 2)

# Iturbe testifies on Wednesday
solver.add(assign["Iturbe"] == day_to_int["Wednesday"])

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(assign[w] == day_to_int["Tuesday"], 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday
solver.add(assign["Hong"] != day_to_int["Monday"])

# At least one witness testifies on Monday
solver.add(Sum([If(assign[w] == day_to_int["Monday"], 1, 0) for w in witnesses]) >= 1)

# Franco does not testify on the same day as Garcia
solver.add(assign["Franco"] != assign["Garcia"])

# Jackson is scheduled to testify on Wednesday (given in the question)
solver.add(assign["Jackson"] == day_to_int["Wednesday"])

# Additional constraint: Iturbe and Jackson are both on Wednesday, so no other witness can be on Wednesday
solver.add(assign["Franco"] != day_to_int["Wednesday"])
solver.add(assign["Garcia"] != day_to_int["Wednesday"])
solver.add(assign["Hong"] != day_to_int["Wednesday"])

# Since Iturbe and Jackson are on Wednesday, the remaining witnesses (Franco, Garcia, Hong) must be on Monday or Tuesday
# Exactly two witnesses are on Tuesday, so one of Franco, Garcia, or Hong must be on Monday

# Evaluate each option
found_options = []

# Option A: Franco is scheduled to testify on Monday
solver.push()
solver.add(assign["Franco"] == day_to_int["Monday"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia is scheduled to testify on Monday
solver.push()
solver.add(assign["Garcia"] == day_to_int["Monday"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Exactly one witness is scheduled to testify on Monday
solver.push()
solver.add(Sum([If(assign[w] == day_to_int["Monday"], 1, 0) for w in witnesses]) == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Exactly two witnesses are scheduled to testify on Monday
solver.push()
solver.add(Sum([If(assign[w] == day_to_int["Monday"], 1, 0) for w in witnesses]) == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Garcia is scheduled to testify on the same day as Hong
solver.push()
solver.add(assign["Garcia"] == assign["Hong"])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")