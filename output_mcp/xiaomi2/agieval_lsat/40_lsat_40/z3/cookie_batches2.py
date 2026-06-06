from z3 import *

solver = Solver()

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Batches are ordered chronologically: O1 < O2 < O3, etc.
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Each batch is on a day 0-4
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Batches are ordered chronologically within each kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)

# No two batches of the same kind on the same day (already implied by strict ordering, but explicit)
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver.add(Or([b == 0 for b in all_batches]))

# O2 is made on the same day as P1
solver.add(O2 == P1)

# S2 is made on Thursday
solver.add(S2 == 3)

# No batch is made on Wednesday
for b in all_batches:
    solver.add(b != 2)

# First check: is the base problem satisfiable?
result = solver.check()
print(f"Base satisfiability: {result}")

if result == sat:
    m = solver.model()
    print("Sample model:")
    for b in all_batches:
        print(f"  {b} = {m[b]}")
    
    # Count batches per day
    for d in range(5):
        day_name = ["Mon","Tue","Wed","Thu","Fri"][d]
        cnt = sum(1 for b in all_batches if m[b].as_long() == d)
        print(f"  {day_name}: {cnt} batches")

# Helper: count batches on a given day
def count_on_day(day):
    return Sum([If(b == day, 1, 0) for b in all_batches])

# Define answer choice constraints
opt_a = (count_on_day(1) == 3)  # Exactly 3 on Tuesday
opt_b = (count_on_day(4) == 3)  # Exactly 3 on Friday
opt_c = (count_on_day(0) >= 2)  # At least 2 on Monday
opt_d = (count_on_day(3) >= 2)  # At least 2 on Thursday
opt_e = (count_on_day(0) < count_on_day(1))  # Fewer on Mon than Tue

# Test each option: check if it MUST be true (negation is unsat)
must_be_true = []
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    s = Solver()
    for c in solver.assertions():
        s.add(c)
    s.add(Not(constr))
    res = s.check()
    print(f"Option {letter}: negation is {res} -> {'MUST be true' if res == unsat else 'not necessarily true'}")
    if res == unsat:
        must_be_true.append(letter)

print(f"\nOptions that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")