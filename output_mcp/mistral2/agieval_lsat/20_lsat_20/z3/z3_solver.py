from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for kittens and puppies over 7 days
# Kittens: Himalayan, Manx, Siamese
# Puppies: Greyhound, Newfoundland, Rottweiler

days = 7

# Kittens: 0=Himalayan, 1=Manx, 2=Siamese
kittens = [Int(f'kitten_day_{i+1}') for i in range(days)]

# Puppies: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppies = [Int(f'puppy_day_{i+1}') for i in range(days)]

solver = Solver()

# Constraints

# 1. Greyhounds are featured on day 1
solver.add(puppies[0] == 0)

# 2. No breed is featured on any two consecutive days
for i in range(days - 1):
    # Kittens
    solver.add(kittens[i] != kittens[i+1])
    # Puppies
    solver.add(puppies[i] != puppies[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
# Day 1 kitten breed not on day 7
solver.add(kittens[0] != kittens[6])
# Day 1 puppy breed not on day 7
solver.add(puppies[0] != puppies[6])

# 4. Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kittens[i] == 0, 1, 0) for i in range(days)]) == 3)
solver.add(kittens[0] != 0)

# 5. Rottweilers are not featured on day 7
solver.add(puppies[6] != 2)

# 6. Rottweilers are not featured on any day that features Himalayans
for i in range(days):
    solver.add(Implies(kittens[i] == 0, puppies[i] != 2))

# 7. Himalayans are not featured on day 2
solver.add(kittens[1] != 0)

# Additional constraints to ensure each day has exactly one kitten and one puppy
for i in range(days):
    solver.add(kittens[i] >= 0, kittens[i] <= 2)
    solver.add(puppies[i] >= 0, puppies[i] <= 2)

# Evaluate multiple choice options
found_options = []

# Option A: Manx are featured on day 3
solver.push()
solver.add(kittens[2] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Siamese are featured on day 4
solver.push()
solver.add(kittens[3] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Rottweilers are featured on day 5
solver.push()
solver.add(puppies[4] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Himalayans are featured on day 6
solver.push()
solver.add(kittens[5] == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Greyhounds are featured on day 7
solver.push()
solver.add(puppies[6] == 0)
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