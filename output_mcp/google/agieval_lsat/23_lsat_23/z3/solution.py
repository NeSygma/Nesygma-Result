from z3 import *

# Days 0-6
days = range(7)
# Kitten breeds: 0:H, 1:M, 2:S
kitten = [Int(f'kitten_{d}') for d in days]
# Puppy breeds: 0:G, 1:N, 2:R
puppy = [Int(f'puppy_{d}') for d in days]

solver = Solver()

# Domain constraints
for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# 1. Greyhounds are featured on day 1 (index 0)
solver.add(puppy[0] == 0)

# 2. No breed is featured on any two consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# 3. Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# 5. Himalayans are not on day 1
solver.add(kitten[0] != 0)

# 6. Rottweilers are not featured on day 7
solver.add(puppy[6] != 2)

# 7. Rottweilers are not featured on any day that features Himalayans
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Options
# (A) There are exactly four breeds that are each featured on three days.
# (B) Greyhounds are featured on every day that Himalayans are.
# (C) Himalayans are featured on every day that Greyhounds are.
# (D) Himalayans are featured on every day that Rottweilers are not.
# (E) Rottweilers are featured on every day that Himalayans are not.

def count_breed(breed_type, breed_idx):
    if breed_type == 'kitten':
        return Sum([If(kitten[d] == breed_idx, 1, 0) for d in days])
    else:
        return Sum([If(puppy[d] == breed_idx, 1, 0) for d in days])

opt_a = (Sum([If(count_breed('kitten', i) == 3, 1, 0) for i in range(3)] + 
             [If(count_breed('puppy', i) == 3, 1, 0) for i in range(3)]) == 4)
opt_b = And([Implies(kitten[d] == 0, puppy[d] == 0) for d in days])
opt_c = And([Implies(puppy[d] == 0, kitten[d] == 0) for d in days])
opt_d = And([Implies(puppy[d] != 2, kitten[d] == 0) for d in days])
opt_e = And([Implies(kitten[d] != 0, puppy[d] == 2) for d in days])

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