from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=oatmeal, P=peanut butter, S=sugar
# Batches: 1, 2, 3

# Declare variables
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()

# Domain constraints: all days between 1 and 5
for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]:
    solver.add(var >= 1, var <= 5)

# Constraint 1: No two batches of same kind on same day
solver.add(O1 != O2, O1 != O3, O2 != O3)
solver.add(P1 != P2, P1 != P3, P2 != P3)
solver.add(S1 != S2, S1 != S3, S2 != S3)

# Constraint 2: At least one batch on Monday (day 1)
solver.add(Or([var == 1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# Constraint 3: Second batch of oatmeal on same day as first batch of peanut butter
solver.add(O2 == P1)

# Constraint 4: Second batch of sugar on Thursday (day 4)
solver.add(S2 == 4)

# Additional constraint from question: "one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
first_batches = [O1, P1, S1]
third_batches = [O3, P3, S3]
solver.add(Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
))

# Check if (B) can be false: At least two batches on Wednesday (day 3)
# So we want Wednesday to have 0 or 1 batch
# Count batches on Wednesday
wed_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
# We want sum of (var == 3) <= 1
# Use If to count
count_wed = Sum([If(var == 3, 1, 0) for var in wed_batches])
solver.add(count_wed <= 1)

if solver.check() == sat:
    print("(B) can be false: Wednesday has at most 1 batch")
    m = solver.model()
    print("Example model:")
    print(f"Oatmeal: batch1={m[O1]}, batch2={m[O2]}, batch3={m[O3]}")
    print(f"Peanut butter: batch1={m[P1]}, batch2={m[P2]}, batch3={m[P3]}")
    print(f"Sugar: batch1={m[S1]}, batch2={m[S2]}, batch3={m[S3]}")
    
    # Count batches per day
    for day in [1, 2, 3, 4, 5]:
        count = sum(1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3] if m[var] == day)
        print(f"Day {day}: {count} batches")
else:
    print("(B) cannot be false: Wednesday must have at least 2 batches")