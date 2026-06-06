from z3 import *

# Declare symbolic variables for each witness's day (0=Monday, 1=Tuesday, 2=Wednesday)
F, G, H, I, J = Ints('F G H I J')

solver = Solver()

# Base constraints
# Each witness testifies on exactly one day (0,1,2)
solver.add(F >= 0, F <= 2)
solver.add(G >= 0, G <= 2)
solver.add(H >= 0, H <= 2)
solver.add(I >= 0, I <= 2)
solver.add(J >= 0, J <= 2)

# Iturbe testifies on Wednesday (2)
solver.add(I == 2)

# Exactly two witnesses on Tuesday (day 1)
solver.add(Sum([If(F == 1, 1, 0), If(G == 1, 1, 0), If(H == 1, 1, 0), If(I == 1, 1, 0), If(J == 1, 1, 0)]) == 2)

# Hong does not testify on Monday (day 0)
solver.add(H != 0)

# At least one witness on Monday
solver.add(Sum([If(F == 0, 1, 0), If(G == 0, 1, 0), If(H == 0, 1, 0), If(I == 0, 1, 0), If(J == 0, 1, 0)]) >= 1)

# Franco and Garcia not on the same day
solver.add(F != G)

# Extra condition: Franco and Hong on the same day
solver.add(F == H)

# Now evaluate each answer choice by testing the negation of the option.
# If the negation is unsatisfiable, then the option must be true.
found_options = []

# Option A: Franco is scheduled to testify on Wednesday.
# Negation: Franco is NOT on Wednesday (F != 2)
solver.push()
solver.add(F != 2)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Garcia is scheduled to testify on Monday.
# Negation: Garcia is NOT on Monday (G != 0)
solver.push()
solver.add(G != 0)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Garcia is scheduled to testify on Wednesday.
# Negation: Garcia is NOT on Wednesday (G != 2)
solver.push()
solver.add(G != 2)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Hong is scheduled to testify on Tuesday.
# Negation: Hong is NOT on Tuesday (H != 1)
solver.push()
solver.add(H != 1)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Iturbe is the only witness scheduled to testify on Wednesday.
# Negation: Iturbe is NOT the only witness on Wednesday.
# Since I is fixed to 2, this means at least one other witness is on Wednesday.
solver.push()
solver.add(Or(F == 2, G == 2, H == 2, J == 2))
if solver.check() == unsat:
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