from z3 import *

solver = Solver()

# Days 1-7 (using 0-indexed: 0..6 representing days 1..7)
N = 7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = [Int(f'kitten_{d}') for d in range(N)]
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = [Int(f'puppy_{d}') for d in range(N)]

# Domain constraints
for d in range(N):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds are featured on day 1
solver.add(puppy[0] == 0)  # Greyhound = 0

# Constraint 2: No breed is featured on any two consecutive days
for d in range(N - 1):
    solver.add(kitten[d] != kitten[d + 1])
    solver.add(puppy[d] != puppy[d + 1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans featured on exactly 3 days, not on day 1
solver.add(kitten[0] != 0)  # Not on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in range(N)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day featuring Himalayans
solver.add(puppy[6] != 2)  # Not on day 7
for d in range(N):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Additional condition: Himalayans not on day 7
solver.add(kitten[6] != 0)

# Now test each option
# Option A: Greyhounds are featured on days 3 and 5
opt_a = And(puppy[2] == 0, puppy[4] == 0)  # days 3 and 5 (0-indexed: 2 and 4)

# Option B: Newfoundlands are featured on day 3
opt_b = (puppy[2] == 1)  # day 3 (0-indexed: 2)

# Option C: Rottweilers are featured on day 6
opt_c = (puppy[5] == 2)  # day 6 (0-indexed: 5)

# Option D: Rottweilers are featured only on day 3
opt_d = And(
    puppy[2] == 2,  # day 3 has Rottweiler
    And([puppy[d] != 2 for d in range(N) if d != 2])  # no other day has Rottweiler
)

# Option E: Rottweilers are featured on exactly three days
opt_e = (Sum([If(puppy[d] == 2, 1, 0) for d in range(N)]) == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for d in range(N):
            k_val = m.evaluate(kitten[d]).as_long()
            p_val = m.evaluate(puppy[d]).as_long()
            k_names = {0: 'H', 1: 'M', 2: 'S'}
            p_names = {0: 'G', 1: 'N', 2: 'R'}
            print(f"  Day {d+1}: kitten={k_names[k_val]}, puppy={p_names[p_val]}")
    else:
        print(f"Option {letter}: UNSAT")
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