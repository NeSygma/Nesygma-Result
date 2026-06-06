from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare days as integers for clarity
Monday = 0
Tuesday = 1
Wednesday = 2

# Declare witnesses
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]

# Create a solver
solver = Solver()

# Assign each witness to a day (0=Monday, 1=Tuesday, 2=Wednesday)
# Use a dictionary to map witness names to their day variables
witness_days = {w: Int(f"{w}_day") for w in witnesses}

# Each witness testifies on exactly one day
for w in witnesses:
    solver.add(Or(witness_days[w] == Monday, 
                  witness_days[w] == Tuesday, 
                  witness_days[w] == Wednesday))

# Constraint: Iturbe testifies on Wednesday
solver.add(witness_days["Iturbe"] == Wednesday)

# Constraint: Exactly two witnesses testify on Tuesday
solver.add(Sum([If(witness_days[w] == Tuesday, 1, 0) for w in witnesses]) == 2)

# Constraint: Hong does not testify on Monday
solver.add(witness_days["Hong"] != Monday)

# Constraint: At least one witness testifies on Monday
solver.add(Sum([If(witness_days[w] == Monday, 1, 0) for w in witnesses]) >= 1)

# Constraint: Franco does not testify on the same day that Garcia testifies
solver.add(witness_days["Franco"] != witness_days["Garcia"])

# Condition for the question: Jackson is the only witness scheduled to testify on Monday
solver.add(witness_days["Jackson"] == Monday)
for w in ["Franco", "Garcia", "Hong", "Iturbe"]:
    solver.add(witness_days[w] != Monday)

# Now, evaluate each option to see which must be true by negating it and checking for unsatisfiability
must_be_true = []

# Option A: Franco is scheduled to testify on Wednesday
# Negation: Franco is NOT scheduled to testify on Wednesday
solver.push()
solver.add(witness_days["Franco"] != Wednesday)
if solver.check() == unsat:
    must_be_true.append("A")
solver.pop()

# Option B: Hong is scheduled to testify on Tuesday
# Negation: Hong is NOT scheduled to testify on Tuesday
solver.push()
solver.add(witness_days["Hong"] != Tuesday)
if solver.check() == unsat:
    must_be_true.append("B")
solver.pop()

# Option C: Garcia is scheduled to testify on Tuesday
# Negation: Garcia is NOT scheduled to testify on Tuesday
solver.push()
solver.add(witness_days["Garcia"] != Tuesday)
if solver.check() == unsat:
    must_be_true.append("C")
solver.pop()

# Option D: Franco is scheduled to testify on the same day as Hong
# Negation: Franco is NOT scheduled to testify on the same day as Hong
solver.push()
solver.add(witness_days["Franco"] != witness_days["Hong"])
if solver.check() == unsat:
    must_be_true.append("D")
solver.pop()

# Option E: Garcia is scheduled to testify on the same day as Hong
# Negation: Garcia is NOT scheduled to testify on the same day as Hong
solver.push()
solver.add(witness_days["Garcia"] != witness_days["Hong"])
if solver.check() == unsat:
    must_be_true.append("E")
solver.pop()

# Output the result
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")