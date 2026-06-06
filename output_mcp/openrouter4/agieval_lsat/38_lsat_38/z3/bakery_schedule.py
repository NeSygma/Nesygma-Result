from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday

# Each batch variable represents the day (0-4) it's made on
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain: each batch is made on a day 0-4
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Constraint 1: No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# Constraint 2: At least one batch of cookies is made on Monday
solver.add(Or([b == 0 for b in all_batches]))

# Constraint 3: The second batch of oatmeal cookies (O2) is made on the same day as the first batch of peanut butter cookies (P1)
solver.add(O2 == P1)

# Constraint 4: The second batch of sugar cookies (S2) is made on Thursday (day 3)
solver.add(S2 == 3)

# Now check for each day whether at most 2 batches could be made on that day
# We need to find days d such that there EXISTS a valid schedule where count_on_day_d <= 2

days_with_at_most_two = []

for d in range(5):
    solver.push()
    # Count batches on day d
    day_count = Sum([If(b == d, 1, 0) for b in all_batches])
    solver.add(day_count <= 2)
    result = solver.check()
    if result == sat:
        days_with_at_most_two.append(d)
    solver.pop()

print(f"Days where at most 2 batches could be made: {days_with_at_most_two}")
print(f"Count: {len(days_with_at_most_two)}")

# Map to days of week
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
for d in days_with_at_most_two:
    print(f"  {day_names[d]} ({d})")

# Determine the answer choice
# A=one, B=two, C=three, D=four, E=five
if len(days_with_at_most_two) == 1:
    print("answer:A")
elif len(days_with_at_most_two) == 2:
    print("answer:B")
elif len(days_with_at_most_two) == 3:
    print("answer:C")
elif len(days_with_at_most_two) == 4:
    print("answer:D")
elif len(days_with_at_most_two) == 5:
    print("answer:E")