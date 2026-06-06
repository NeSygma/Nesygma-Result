from z3 import *

# Declare batch day variables
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain: days 1..5
for var in all_batches:
    solver.add(var >= 1, var <= 5)

# No two batches of same kind on same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# At least one batch on Monday (day 1)
solver.add(Or([var == 1 for var in all_batches]))

# Second oatmeal batch same day as first peanut butter batch
solver.add(O2 == P1)

# Second sugar batch on Thursday (day 4)
solver.add(S2 == 4)

# Count days that can have at most two batches
count = 0
for day in range(1, 6):
    solver.push()
    # Constraint: number of batches on this day <= 2
    batch_count = Sum([If(var == day, 1, 0) for var in all_batches])
    solver.add(batch_count <= 2)
    if solver.check() == sat:
        count += 1
    solver.pop()

print(f"Count of days with at most two batches possible: {count}")

# Now determine which option matches
# Use a separate solver for the options
solver2 = Solver()
answer = Int('answer')
solver2.add(answer == count)

found_options = []
for letter, num in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver2.push()
    solver2.add(answer == num)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")