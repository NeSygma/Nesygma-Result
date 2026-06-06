from z3 import *

# Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
days = range(5)

# Variables for each kind and batch
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1,O2,O3,P1,P2,P3,S1,S2,S3]

solver = Solver()
# Domain constraints
for v in all_vars:
    solver.add(And(v >= 0, v <= 4))
# No two batches of same kind on same day (all distinct per kind)
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))
# At least one batch on Monday (day 0)
solver.add(Or([v == 0 for v in all_vars]))
# Specific conditions
solver.add(O2 == P1)          # second oatmeal = first peanut butter
solver.add(S2 == 3)           # second sugar on Thursday (day 3)
# Existence condition: one kind's first batch same day as another kind's third batch (different kinds)
exist_cond = Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
)
solver.add(exist_cond)

# Helper to count batches on a given day
def count_on(day):
    return Sum([If(v == day, 1, 0) for v in all_vars])

found_options = []

# Option A: At least one batch each day -> negation: some day has zero batches
neg_A = Or([And([v != d for v in all_vars]) for d in days])
# Option B: At least two batches on Wednesday (day 2) -> negation: <=1 batch on Wed
neg_B = count_on(2) <= 1
# Option C: Exactly one batch on Monday (day 0) -> negation: >=2 batches on Monday
neg_C = count_on(0) >= 2
# Option D: Exactly two batches on Tuesday (day 1) -> negation: count != 2
neg_D = count_on(1) != 2
# Option E: Exactly one batch on Friday (day 4) -> negation: count != 1
neg_E = count_on(4) != 1

options = [
    ("A", neg_A),
    ("B", neg_B),
    ("C", neg_C),
    ("D", neg_D),
    ("E", neg_E)
]

for letter, constr in options:
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