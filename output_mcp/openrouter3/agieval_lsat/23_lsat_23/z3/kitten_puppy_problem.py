from z3 import *

# Days 1-7 (we'll use 0-indexed for programming, but map to 1-7 conceptually)
days = range(7)  # 0=day1, 1=day2, ..., 6=day7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = [Int(f'kitten_{d}') for d in days]
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = [Int(f'puppy_{d}') for d in days]

solver = Solver()

# Domain constraints: each breed must be in {0,1,2}
for d in days:
    solver.add(Or([kitten[d] == i for i in range(3)]))
    solver.add(Or([puppy[d] == i for i in range(3)]))

# Constraint 1: Greyhounds are featured on day 1 (day 1 is index 0)
solver.add(puppy[0] == 0)

# Constraint 2: No breed is featured on any two consecutive days
# For kittens
for d in range(6):  # days 0-5 (1-6) compared to next day
    solver.add(kitten[d] != kitten[d+1])
# For puppies
for d in range(6):
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
# Day 1 is index 0, day 7 is index 6
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans are featured on exactly three days, but not on day 1
himalayan_count = Sum([If(kitten[d] == 0, 1, 0) for d in days])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != 0)  # not on day 1

# Constraint 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != 2)  # not on day 7
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Now test each option
found_options = []

# Option A: There are exactly four breeds that are each featured on three days.
# We need to count how many breeds (out of 6 total: 3 kitten + 3 puppy) appear exactly 3 times.
# Let's define counts for each breed
kitten_counts = [Sum([If(kitten[d] == i, 1, 0) for d in days]) for i in range(3)]
puppy_counts = [Sum([If(puppy[d] == i, 1, 0) for d in days]) for i in range(3)]
all_counts = kitten_counts + puppy_counts  # 6 counts total

# Count how many of these 6 counts equal 3
count_of_three = Sum([If(count == 3, 1, 0) for count in all_counts])
opt_a_constr = (count_of_three == 4)

# Option B: Greyhounds are featured on every day that Himalayans are.
# For each day, if kitten is Himalayan (0), then puppy must be Greyhound (0)
opt_b_constr = And([Implies(kitten[d] == 0, puppy[d] == 0) for d in days])

# Option C: Himalayans are featured on every day that Greyhounds are.
# For each day, if puppy is Greyhound (0), then kitten must be Himalayan (0)
opt_c_constr = And([Implies(puppy[d] == 0, kitten[d] == 0) for d in days])

# Option D: Himalayans are featured on every day that Rottweilers are not.
# For each day, if puppy is NOT Rottweiler (2), then kitten must be Himalayan (0)
opt_d_constr = And([Implies(puppy[d] != 2, kitten[d] == 0) for d in days])

# Option E: Rottweilers are featured on every day that Himalayans are not.
# For each day, if kitten is NOT Himalayan (0), then puppy must be Rottweiler (2)
opt_e_constr = And([Implies(kitten[d] != 0, puppy[d] == 2) for d in days])

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")