from z3 import *

# Create solver
solver = Solver()

# Define witnesses and days
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
days = ["Monday", "Tuesday", "Wednesday"]

# Map witnesses to indices
F, G, H, I, J = 0, 1, 2, 3, 4
# Map days to indices
MON, TUE, WED = 0, 1, 2

# Create symbolic variables: day each witness testifies
# Each witness's day is an integer 0, 1, or 2
day = [Int(f"day_{w}") for w in witnesses]

# Base constraints:
# 1. Each witness testifies on exactly one day (0, 1, or 2)
for d in day:
    solver.add(Or(d == MON, d == TUE, d == WED))

# 2. Franco does not testify on the same day as Garcia
solver.add(day[F] != day[G])

# 3. Iturbe testifies on Wednesday
solver.add(day[I] == WED)

# 4. Exactly two witnesses testify on Tuesday
tuesday_count = Sum([If(day[w] == TUE, 1, 0) for w in range(len(witnesses))])
solver.add(tuesday_count == 2)

# 5. Hong does not testify on Monday
solver.add(day[H] != MON)

# 6. At least one witness testifies on Monday
monday_count = Sum([If(day[w] == MON, 1, 0) for w in range(len(witnesses))])
solver.add(monday_count >= 1)

# Additional constraint: Jackson is scheduled to testify on Wednesday (given in the question)
solver.add(day[J] == WED)

# Now test each answer choice for entailment
# For each option, check if its negation makes the constraints unsatisfiable
# If yes, then the option must be true

# Answer choices:
# (A) Franco is scheduled to testify on Monday.
# (B) Garcia is scheduled to testify on Monday.
# (C) Exactly one witness is scheduled to testify on Monday.
# (D) Exactly two witnesses are scheduled to testify on Monday.
# (E) Garcia is scheduled to testify on the same day as Hong.

# Define constraints for each option
opt_a = (day[F] == MON)
opt_b = (day[G] == MON)
opt_c = (monday_count == 1)
opt_d = (monday_count == 2)
opt_e = (day[G] == day[H])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    # Create a new solver for each check
    s = Solver()
    # Add all base constraints
    for d in day:
        s.add(Or(d == MON, d == TUE, d == WED))
    s.add(day[F] != day[G])
    s.add(day[I] == WED)
    s.add(tuesday_count == 2)
    s.add(day[H] != MON)
    s.add(monday_count >= 1)
    s.add(day[J] == WED)
    
    # Add the NEGATION of the option
    s.add(Not(constr))
    
    # Check if the negation is satisfiable
    if s.check() == unsat:
        # If negation is unsatisfiable, then the option must be true
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")