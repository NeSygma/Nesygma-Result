from z3 import *

solver = Solver()

# Days 1-7 (using 0-indexed: 0..6)
DAYS = 7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = [Int(f'kitten_{d}') for d in range(DAYS)]
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = [Int(f'puppy_{d}') for d in range(DAYS)]

H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Domain constraints
for d in range(DAYS):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds are featured on day 1 (index 0)
solver.add(puppy[0] == G)

# Constraint 2: No breed is featured on any two consecutive days
for d in range(DAYS - 1):
    solver.add(kitten[d] != kitten[d + 1])
    solver.add(puppy[d] != puppy[d + 1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans on exactly 3 days, not on day 1
solver.add(kitten[0] != H)
solver.add(Sum([If(kitten[d] == H, 1, 0) for d in range(DAYS)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day featuring Himalayans
solver.add(puppy[6] != R)
for d in range(DAYS):
    solver.add(Implies(kitten[d] == H, puppy[d] != R))

# Now evaluate each answer choice
found_options = []

# (A) There are exactly four breeds that are each featured on exactly three days.
# Count how many of the 6 breeds (H,M,S,G,N,R) appear on exactly 3 days
breed_counts = []
for b in range(3):  # kitten breeds
    breed_counts.append(Sum([If(kitten[d] == b, 1, 0) for d in range(DAYS)]))
for b in range(3):  # puppy breeds
    breed_counts.append(Sum([If(puppy[d] == b, 1, 0) for d in range(DAYS)]))

count_exactly_three = Sum([If(bc == 3, 1, 0) for bc in breed_counts])
opt_a_constr = (count_exactly_three == 4)

# (B) Greyhounds are featured on every day that Himalayans are.
opt_b_constr = And([Implies(kitten[d] == H, puppy[d] == G) for d in range(DAYS)])

# (C) Himalayans are featured on every day that Greyhounds are.
opt_c_constr = And([Implies(puppy[d] == G, kitten[d] == H) for d in range(DAYS)])

# (D) Himalayans are featured on every day that Rottweilers are not.
opt_d_constr = And([Implies(puppy[d] != R, kitten[d] == H) for d in range(DAYS)])

# (E) Rottweilers are featured on every day that Himalayans are not.
opt_e_constr = And([Implies(kitten[d] != H, puppy[d] == R) for d in range(DAYS)])

options = [
    ("A", opt_a_constr),
    ("B", opt_b_constr),
    ("C", opt_c_constr),
    ("D", opt_d_constr),
    ("E", opt_e_constr),
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for d in range(DAYS):
            k_val = m.evaluate(kitten[d])
            p_val = m.evaluate(puppy[d])
            k_name = {0: "H", 1: "M", 2: "S"}[int(str(k_val))]
            p_name = {0: "G", 1: "N", 2: "R"}[int(str(p_val))]
            print(f"  Day {d+1}: kitten={k_name}, puppy={p_name}")
    else:
        print(f"Option {letter}: {result}")
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