from z3 import *

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
days = range(5)

# Cookie types: O=0 (Oatmeal), P=1 (Peanut Butter), S=2 (Sugar)
cookie_types = range(3)

# Batches: 1st, 2nd, 3rd
batches = range(3)

# Batch variables: batch[type][batch] = day
batch = [[Int(f'batch_{t}_{b}') for b in batches] for t in cookie_types]

solver = Solver()

# Constraint 1: No two batches of the same kind on the same day
for t in cookie_types:
    solver.add(Distinct([batch[t][b] for b in batches]))

# Constraint 2: At least one batch on Monday (day 0)
solver.add(Or([batch[t][b] == 0 for t in cookie_types for b in batches]))

# Constraint 3: O2 (batch[0][1]) is on the same day as P1 (batch[1][0])
solver.add(batch[0][1] == batch[1][0])

# Constraint 4: S2 (batch[2][1]) is on Thursday (day 3)
solver.add(batch[2][1] == 3)

# Condition: One kind's first batch is on the same day as another kind's third batch
# We will encode this as: exists t1, t2: batch[t1][0] == batch[t2][2]
t1_t2_pairs = [(t1, t2) for t1 in cookie_types for t2 in cookie_types]
condition = Or([And(batch[t1][0] == batch[t2][2]) for (t1, t2) in t1_t2_pairs])
solver.add(condition)

# Additional constraint: Each batch is assigned to a day (0-4)
for t in cookie_types:
    for b in batches:
        solver.add(batch[t][b] >= 0, batch[t][b] <= 4)

# Answer choices:
# (A) At least one batch of cookies is made on each of the five days.
choice_A = And([Or([batch[t][b] == d for t in cookie_types for b in batches]) for d in days])

# (B) At least two batches of cookies are made on Wednesday (day 2).
choice_B = Sum([If(batch[t][b] == 2, 1, 0) for t in cookie_types for b in batches]) >= 2

# (C) Exactly one batch of cookies is made on Monday (day 0).
choice_C = Sum([If(batch[t][b] == 0, 1, 0) for t in cookie_types for b in batches]) == 1

# (D) Exactly two batches of cookies are made on Tuesday (day 1).
choice_D = Sum([If(batch[t][b] == 1, 1, 0) for t in cookie_types for b in batches]) == 2

# (E) Exactly one batch of cookies is made on Friday (day 4).
choice_E = Sum([If(batch[t][b] == 4, 1, 0) for t in cookie_types for b in batches]) == 1

# Evaluate each choice under the condition that the condition holds
found_options = []
for letter, constr in [("A", choice_A), ("B", choice_B), ("C", choice_C), ("D", choice_D), ("E", choice_E)]:
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