from z3 import *

solver = Solver()

# Days 1-7 (index 0-6)
days = 7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = [Int(f'kitten_{d}') for d in range(days)]

# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = [Int(f'puppy_{d}') for d in range(days)]

H, M, S = 0, 1, 2  # kitten breeds
G, N, R = 0, 1, 2  # puppy breeds

# Domain constraints: each day exactly one of each (value 0, 1, or 2)
for d in range(days):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds featured on day 1
solver.add(puppy[0] == G)

# Constraint 2: No breed featured on any two consecutive days
for d in range(days - 1):
    solver.add(kitten[d] != kitten[d + 1])
    solver.add(puppy[d] != puppy[d + 1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans on exactly 3 days, not on day 1
solver.add(kitten[0] != H)
solver.add(Sum([If(kitten[d] == H, 1, 0) for d in range(days)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day featuring Himalayans
solver.add(puppy[6] != R)
for d in range(days):
    solver.add(Implies(kitten[d] == H, puppy[d] != R))

# Define the kitten order options
# (A) H, M, S, H, M, H, S
opt_a = [kitten[d] == v for d, v in enumerate([H, M, S, H, M, H, S])]
# (B) M, H, S, H, M, H, M
opt_b = [kitten[d] == v for d, v in enumerate([M, H, S, H, M, H, M])]
# (C) M, H, M, H, S, M, S
opt_c = [kitten[d] == v for d, v in enumerate([M, H, M, H, S, M, S])]
# (D) S, H, M, H, S, S, H
opt_d = [kitten[d] == v for d, v in enumerate([S, H, M, H, S, S, H])]
# (E) S, H, S, H, M, S, H
opt_e = [kitten[d] == v for d, v in enumerate([S, H, S, H, M, S, H])]

options = [
    ("A", And(opt_a)),
    ("B", And(opt_b)),
    ("C", And(opt_c)),
    ("D", And(opt_d)),
    ("E", And(opt_e)),
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        puppy_vals = [m.evaluate(puppy[d]) for d in range(days)]
        kitten_vals = [m.evaluate(kitten[d]) for d in range(days)]
        print(f"  Kittens: {kitten_vals}")
        print(f"  Puppies: {puppy_vals}")
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