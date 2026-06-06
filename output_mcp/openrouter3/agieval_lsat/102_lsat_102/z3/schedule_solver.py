from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

solver = Solver()

# Base constraints
# Each witness testifies on exactly one day (0,1,2)
solver.add(Franco >= 0, Franco <= 2)
solver.add(Garcia >= 0, Garcia <= 2)
solver.add(Hong >= 0, Hong <= 2)
solver.add(Iturbe >= 0, Iturbe <= 2)
solver.add(Jackson >= 0, Jackson <= 2)

# Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# Iturbe testifies on Wednesday (day 2)
solver.add(Iturbe == 2)

# Exactly two witnesses testify on Tuesday (day 1)
# Count how many have day == 1
tuesday_count = Sum([If(Franco == 1, 1, 0),
                     If(Garcia == 1, 1, 0),
                     If(Hong == 1, 1, 0),
                     If(Iturbe == 1, 1, 0),
                     If(Jackson == 1, 1, 0)])
solver.add(tuesday_count == 2)

# Hong does not testify on Monday (day 0)
solver.add(Hong != 0)

# At least one witness testifies on Monday (day 0)
monday_count = Sum([If(Franco == 0, 1, 0),
                    If(Garcia == 0, 1, 0),
                    If(Hong == 0, 1, 0),
                    If(Iturbe == 0, 1, 0),
                    If(Jackson == 0, 1, 0)])
solver.add(monday_count >= 1)

# Additional condition: Franco and Hong testify on the same day
solver.add(Franco == Hong)

# Now test each answer choice
# Answer choices:
# (A) Franco is scheduled to testify on Wednesday.
# (B) Garcia is scheduled to testify on Monday.
# (C) Garcia is scheduled to testify on Wednesday.
# (D) Hong is scheduled to testify on Tuesday.
# (E) Iturbe is the only witness scheduled to testify on Wednesday.

# Define constraints for each option
opt_a = (Franco == 2)  # Wednesday is day 2
opt_b = (Garcia == 0)  # Monday is day 0
opt_c = (Garcia == 2)  # Wednesday is day 2
opt_d = (Hong == 1)    # Tuesday is day 1
# For E: Iturbe is the only witness on Wednesday means Iturbe=2 and all others !=2
opt_e = And(Iturbe == 2,
            Franco != 2,
            Garcia != 2,
            Hong != 2,
            Jackson != 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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