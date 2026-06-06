from z3 import *

# Declare the breeds as symbolic constants
Breed = Datatype('Breed')
Breed.declare('Himalayan')
Breed.declare('Manx')
Breed.declare('Siamese')
Breed.declare('Greyhound')
Breed.declare('Newfoundland')
Breed.declare('Rottweiler')
Breed = Breed.create()

Himalayan, Manx, Siamese, Greyhound, Newfoundland, Rottweiler = (
    Breed.Himalayan,
    Breed.Manx,
    Breed.Siamese,
    Breed.Greyhound,
    Breed.Newfoundland,
    Breed.Rottweiler,
)

# Days 1 through 7
Day = IntSort()
days = range(1, 8)

# Kitten and puppy breeds for each day
kitten = [Int(f'kitten_{d}') for d in days]
puppy = [Int(f'puppy_{d}') for d in days]

# Helper function to convert breed to Int for Z3
# We map each breed to a unique integer for easier constraint handling
breed_to_int = {
    Himalayan: 0,
    Manx: 1,
    Siamese: 2,
    Greyhound: 3,
    Newfoundland: 4,
    Rottweiler: 5,
}

# Base constraints
solver = Solver()

# 1. Greyhounds are featured on day 1 (puppy on day 1 is Greyhound)
solver.add(puppy[0] == breed_to_int[Greyhound])

# 2. No breed is featured on any two consecutive days
for d in range(6):
    solver.add(And(
        kitten[d] != kitten[d+1],
        puppy[d] != puppy[d+1]
    ))

# 3. Any breed featured on day 1 is not featured on day 7
# Day 1 breeds: kitten[0] and puppy[0]
# Day 7 breeds: kitten[6] and puppy[6]
solver.add(And(
    kitten[0] != kitten[6],
    puppy[0] != puppy[6]
))

# 4. Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kitten[d] == breed_to_int[Himalayan], 1, 0) for d in range(7)]) == 3)
solver.add(kitten[0] != breed_to_int[Himalayan])

# 5. Rottweilers are not featured on day 7
solver.add(puppy[6] != breed_to_int[Rottweiler])

# 6. Rottweilers are not featured on any day that features Himalayans
for d in range(7):
    solver.add(Implies(kitten[d] == breed_to_int[Himalayan], puppy[d] != breed_to_int[Rottweiler]))

# 7. Himalayans are not featured on day 7
solver.add(kitten[6] != breed_to_int[Himalayan])

# Additional constraints: Each day has exactly one kitten and one puppy breed
# Kitten breeds: Himalayan, Manx, Siamese
# Puppy breeds: Greyhound, Newfoundland, Rottweiler
for d in range(7):
    solver.add(Or(*[kitten[d] == breed_to_int[b] for b in [Himalayan, Manx, Siamese]]))
    solver.add(Or(*[puppy[d] == breed_to_int[b] for b in [Greyhound, Newfoundland, Rottweiler]]))

# Evaluate each option
found_options = []

# Option A: Greyhounds are featured on days 3 and 5
opt_a_constr = And(
    puppy[2] == breed_to_int[Greyhound],  # day 3
    puppy[4] == breed_to_int[Greyhound]   # day 5
)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Newfoundlands are featured on day 3
opt_b_constr = (puppy[2] == breed_to_int[Newfoundland])  # day 3
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Rottweilers are featured on day 6
opt_c_constr = (puppy[5] == breed_to_int[Rottweiler])  # day 6
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Rottweilers are featured only on day 3
opt_d_constr = And(
    puppy[2] == breed_to_int[Rottweiler],  # day 3
    And(
        *[puppy[d] != breed_to_int[Rottweiler] for d in range(7) if d != 2]
    )
)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Rottweilers are featured on exactly three days
opt_e_constr = (Sum([If(puppy[d] == breed_to_int[Rottweiler], 1, 0) for d in range(7)]) == 3)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
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