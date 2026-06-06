from z3 import *

solver = Solver()

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Variables: batch_i for each cookie type (O=Oatmeal, P=PeanutButter, S=Sugar)
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch on a day 1-5
for v in all_vars:
    solver.add(v >= 1, v <= 5)

# No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver.add(Or([v == 1 for v in all_vars]))

# O2 == P1 (second oatmeal same day as first peanut butter)
solver.add(O2 == P1)

# S2 == 4 (second sugar on Thursday)
solver.add(S2 == 4)

# Additional condition: one kind's first batch same day as another kind's third batch
# (different kinds)
additional = Or(
    O1 == P3, O1 == S3,  # Oatmeal first = PB third or Sugar third
    P1 == O3, P1 == S3,  # PB first = Oatmeal third or Sugar third
    S1 == O3, S1 == P3   # Sugar first = Oatmeal third or PB third
)
solver.add(additional)

# Now test each answer choice
# "Could be false" = satisfiable when negated

# (A) At least one batch on each of the five days
# Each day 1-5 has at least one batch
opt_a = And([Or([v == d for v in all_vars]) for d in range(1, 6)])

# (B) At least two batches on Wednesday (day 3)
# Count batches on day 3 >= 2
count_wed = Sum([If(v == 3, 1, 0) for v in all_vars])
opt_b = (count_wed >= 2)

# (C) Exactly one batch on Monday (day 1)
count_mon = Sum([If(v == 1, 1, 0) for v in all_vars])
opt_c = (count_mon == 1)

# (D) Exactly two batches on Tuesday (day 2)
count_tue = Sum([If(v == 2, 1, 0) for v in all_vars])
opt_d = (count_tue == 2)

# (E) Exactly one batch on Friday (day 5)
count_fri = Sum([If(v == 5, 1, 0) for v in all_vars])
opt_e = (count_fri == 1)

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))  # Could be false = satisfiable when negated
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} COULD BE FALSE. Example: O1={m[O1]},O2={m[O2]},O3={m[O3]},P1={m[P1]},P2={m[P2]},P3={m[P3]},S1={m[S1]},S2={m[S2]},S3={m[S3]}")
    else:
        print(f"Option {letter} MUST BE TRUE (negation is {result})")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")