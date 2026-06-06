from z3 import *

solver = Solver()

# Days 1-7
days = range(1, 8)

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = {d: Int(f'kitten_{d}') for d in days}
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = {d: Int(f'puppy_{d}') for d in days}

# Domain constraints
for d in days:
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds on day 1
solver.add(puppy[1] == 0)

# Constraint 2: No breed on two consecutive days
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed on day 1 is not on day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Constraint 4: Himalayans on exactly 3 days, not on day 1
solver.add(kitten[1] != 0)  # Not on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Constraint 5: Rottweilers not on day 7
solver.add(puppy[7] != 2)

# Constraint 5 continued: Rottweilers not on any day with Himalayans
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Additional constraint from question: Himalayans not on day 7
solver.add(kitten[7] != 0)

# Now evaluate each option
found_options = []

# Option A: Greyhounds on days 3 and 5
opt_a = And(puppy[3] == 0, puppy[5] == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Newfoundlands on day 3
opt_b = (puppy[3] == 1)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Rottweilers on day 6
opt_c = (puppy[6] == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Rottweilers only on day 3
opt_d = And(puppy[3] == 2, 
            And([puppy[d] != 2 for d in days if d != 3]))
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Rottweilers on exactly three days
opt_e = (Sum([If(puppy[d] == 2, 1, 0) for d in days]) == 3)
solver.push()
solver.add(opt_e)
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