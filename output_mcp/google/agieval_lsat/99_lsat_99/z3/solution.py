from z3 import *

# Witnesses: 0:Franco, 1:Garcia, 2:Hong, 3:Iturbe, 4:Jackson
# Days: 0:Monday, 1:Tuesday, 2:Wednesday
witnesses = range(5)
days = range(3)

# Variables: day[w] is the day witness w testifies
day = [Int(f'day_{w}') for w in witnesses]

solver = Solver()

# Each witness testifies on exactly one day
for w in witnesses:
    solver.add(day[w] >= 0, day[w] <= 2)

# 1. Franco does not testify on the same day that Garcia testifies.
solver.add(day[0] != day[1])

# 2. Iturbe testifies on Wednesday (day 2).
solver.add(day[3] == 2)

# 3. Exactly two witnesses testify on Tuesday (day 1).
solver.add(Sum([If(day[w] == 1, 1, 0) for w in witnesses]) == 2)

# 4. Hong does not testify on Monday (day 0).
solver.add(day[2] != 0)

# 5. At least one witness testifies on Monday (day 0).
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Define options
# (A) Franco is the only witness scheduled to testify on Monday.
opt_a = And(day[0] == 0, Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1)

# (B) Franco is scheduled to testify on the same day as Iturbe.
opt_b = (day[0] == day[3])

# (C) Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(day[1] == 1, day[2] == 1)

# (D) Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d = And(day[1] == 0, Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 1, 
            day[2] == 2, Sum([If(day[w] == 2, 1, 0) for w in witnesses]) == 2)

# (E) Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
opt_e = And(day[4] == 1, Sum([If(day[w] == 0, 1, 0) for w in witnesses]) == 2)

# We want to find which one CANNOT be true.
# This means we are looking for the option that is UNSATISFIABLE.
# The question asks "Which one of the following CANNOT be true".
# So we test each option. If an option is SAT, it CAN be true. If it is UNSAT, it CANNOT be true.

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
unsat_options = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")