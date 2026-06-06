from z3 import *

# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
# Wednesday (3) is excluded
VALID_DAYS = [1, 2, 4, 5]

# Batches ordered chronologically: O1<O2<O3 means O1 is earliest oatmeal batch
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Each batch on a valid day (not Wednesday)
for b in all_batches:
    solver.add(Or([b == d for d in VALID_DAYS]))

# Chronological ordering within each kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)

# At least one batch on Monday
solver.add(Or([b == 1 for b in all_batches]))

# Second oatmeal same day as first peanut butter
solver.add(O2 == P1)

# Second sugar on Thursday
solver.add(S2 == 4)

# Count batches per day
def batches_on_day(d):
    return Sum([If(b == d, 1, 0) for b in all_batches])

mon_count = batches_on_day(1)
tue_count = batches_on_day(2)
thu_count = batches_on_day(4)
fri_count = batches_on_day(5)

# Option constraints
opt_a = (tue_count == 3)        # Exactly 3 batches on Tuesday
opt_b = (fri_count == 3)        # Exactly 3 batches on Friday
opt_c = (mon_count >= 2)        # At least 2 batches on Monday
opt_d = (thu_count >= 2)        # At least 2 batches on Thursday
opt_e = (mon_count < tue_count) # Fewer batches on Monday than Tuesday

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