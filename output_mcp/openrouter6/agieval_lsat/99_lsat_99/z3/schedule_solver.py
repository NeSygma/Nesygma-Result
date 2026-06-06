from z3 import *

# Base constraints
solver = Solver()

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
F = Int('Franco')
G = Int('Garcia')
H = Int('Hong')
I = Int('Iturbe')
J = Int('Jackson')

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = [F, G, H, I, J]

# Domain constraints: each witness testifies on exactly one day (0,1,2)
for d in days:
    solver.add(Or(d == 0, d == 1, d == 2))

# Constraint 1: Franco does not testify on the same day as Garcia
solver.add(F != G)

# Constraint 2: Iturbe testifies on Wednesday
solver.add(I == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday
# Count of witnesses with day == 1
tuesday_count = Sum([If(d == 1, 1, 0) for d in days])
solver.add(tuesday_count == 2)

# Constraint 4: Hong does not testify on Monday
solver.add(H != 0)

# Constraint 5: At least one witness testifies on Monday
monday_count = Sum([If(d == 0, 1, 0) for d in days])
solver.add(monday_count >= 1)

# Define option constraints
# Option A: Franco is the only witness scheduled to testify on Monday.
opt_a = And(F == 0, G != 0, H != 0, J != 0)  # I is already !=0 (I==2)

# Option B: Franco is scheduled to testify on the same day as Iturbe.
opt_b = (F == 2)  # Iturbe is Wednesday

# Option C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(G == 1, H == 1)

# Option D: Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to Wednesday.
# Part 1: Garcia only on Monday
part1 = And(G == 0, F != 0, H != 0, J != 0)  # I is already !=0
# Part 2: Hong is one of two witnesses on Wednesday
# Count of witnesses on Wednesday must be 2, and Hong must be on Wednesday
wed_count = Sum([If(d == 2, 1, 0) for d in days])
part2 = And(H == 2, wed_count == 2)
opt_d = And(part1, part2)

# Option E: Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
opt_e = And(J == 1, monday_count == 2)

# Evaluate each option: collect options that CANNOT be true (i.e., unsatisfiable when added)
found_options = []
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# According to the skeleton, we should use the exact logic string.
# But we have adapted to collect unsatisfiable options.
# Now, if exactly one option is unsatisfiable, that is the answer.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")