from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=Oatmeal, P=Peanut butter, S=Sugar
# Batches: 1,2,3 for each type

# Declare variables for each batch's day
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()

# Domain constraints: each batch is made on a day 1-5
all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
for batch in all_batches:
    solver.add(batch >= 1, batch <= 5)

# Constraint 3: No two batches of the same kind on the same day
solver.add(Distinct([O1, O2, O3]))  # Oatmeal batches on different days
solver.add(Distinct([P1, P2, P3]))  # Peanut butter batches on different days
solver.add(Distinct([S1, S2, S3]))  # Sugar batches on different days

# Constraint 4: At least one batch on Monday
solver.add(Or([batch == 1 for batch in all_batches]))

# Constraint 5: O2 made on same day as P1
solver.add(O2 == P1)

# Constraint 6: S2 made on Thursday (day 4)
solver.add(S2 == 4)

# Constraint 7: No batch on Wednesday (day 3)
solver.add(And([batch != 3 for batch in all_batches]))

# Check if there are any valid models
result = solver.check()
print(f"Base constraints result: {result}")

if result == sat:
    m = solver.model()
    print("Example model:")
    print(f"O1={m[O1]}, O2={m[O2]}, O3={m[O3]}")
    print(f"P1={m[P1]}, P2={m[P2]}, P3={m[P3]}")
    print(f"S1={m[S1]}, S2={m[S2]}, S3={m[S3]}")
    
    # Count batches per day
    for day in range(1, 6):
        count = sum(1 for batch in all_batches if m[batch] == day)
        print(f"Day {day}: {count} batches")
else:
    print("No valid models found - constraints are inconsistent")