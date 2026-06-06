from z3 import *

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
# Days: Monday=0, Tuesday=1, Wednesday=2
# Each witness testifies on exactly one day.

solver = Solver()

# Create variables: day for each witness (0=Mon, 1=Tue, 2=Wed)
F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]

# Domain: each witness testifies on exactly one of the three days
for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Condition 1: Franco does not testify on the same day as Garcia
solver.add(F != G)

# Condition 2: Iturbe testifies on Wednesday (day 2)
solver.add(I == 2)

# Condition 3: Exactly two witnesses testify on Tuesday (day 1)
# Count how many have day == 1
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Condition 4: Hong does not testify on Monday (day 0)
solver.add(H != 0)

# Condition 5: At least one witness testifies on Monday (day 0)
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition from the question: Franco is scheduled to testify on the same day as Hong
solver.add(F == H)

# Now evaluate each option
# Option A: Franco is scheduled to testify on Wednesday (day 2)
opt_a = (F == 2)

# Option B: Garcia is scheduled to testify on Monday (day 0)
opt_b = (G == 0)

# Option C: Garcia is scheduled to testify on Wednesday (day 2)
opt_c = (G == 2)

# Option D: Hong is scheduled to testify on Tuesday (day 1)
opt_d = (H == 1)

# Option E: Iturbe is the only witness scheduled to testify on Wednesday (day 2)
# That means: I == 2, and for all other witnesses w != I, w != 2
opt_e_constrs = [I == 2]
for w in [F, G, H, J]:
    opt_e_constrs.append(w != 2)
opt_e = And(opt_e_constrs)

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