from z3 import *

solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = 5

# Variables: batch[kind][batch_number] = day (0-4)
# kind: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# batch_number: 0=first, 1=second, 2=third
O = [Int(f'O_{i}') for i in range(3)]  # Oatmeal batches
P = [Int(f'P_{i}') for i in range(3)]  # Peanut Butter batches
S = [Int(f'S_{i}') for i in range(3)]  # Sugar batches

# Domain constraints: each batch on a day 0-4
for b in O + P + S:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))

# At least one batch on Monday (day 0)
all_batches = O + P + S
solver.add(Or([b == 0 for b in all_batches]))

# Second batch of oatmeal = First batch of peanut butter (same day)
solver.add(O[1] == P[0])

# Second batch of sugar = Thursday (day 3)
solver.add(S[1] == 3)

# Additional condition: One kind's first batch = another kind's third batch
# This means there exist two different kinds where first batch of one = third batch of another
first_batches = [O[0], P[0], S[0]]
third_batches = [O[2], P[2], S[2]]

# At least one pair (different kinds) where first = third
solver.add(Or([
    And(first_batches[i] == third_batches[j], i != j)
    for i in range(3) for j in range(3)
]))

# First, let's see if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    print("Oatmeal:", [m.evaluate(O[i]) for i in range(3)])
    print("Peanut Butter:", [m.evaluate(P[i]) for i in range(3)])
    print("Sugar:", [m.evaluate(S[i]) for i in range(3)])
    
    # Count batches per day
    for d in range(5):
        count = sum(1 for b in all_batches if m.evaluate(b) == d)
        print(f"Day {d}: {count} batches")
else:
    print("Base constraints unsatisfiable!")
    exit()

# Now test each option
print("\nTesting which options could be false:")

# Define the options as constraints
# (A) At least one batch on each of the five days
opt_a = And([Or([b == d for b in all_batches]) for d in range(5)])

# (B) At least two batches on Wednesday (day 2)
opt_b = Sum([If(b == 2, 1, 0) for b in all_batches]) >= 2

# (C) Exactly one batch on Monday (day 0)
opt_c = Sum([If(b == 0, 1, 0) for b in all_batches]) == 1

# (D) Exactly two batches on Tuesday (day 1)
opt_d = Sum([If(b == 1, 1, 0) for b in all_batches]) == 2

# (E) Exactly one batch on Friday (day 4)
opt_e = Sum([If(b == 4, 1, 0) for b in all_batches]) == 1

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    s = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s.add(c)
    # Try to make the option false
    s.add(Not(constr))
    if s.check() == sat:
        found_options.append(letter)
        print(f"Option {letter} could be false")
    else:
        print(f"Option {letter} must be true")

print(f"\nOptions that could be false: {found_options}")