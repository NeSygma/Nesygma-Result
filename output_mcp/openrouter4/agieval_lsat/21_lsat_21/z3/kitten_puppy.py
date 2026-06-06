from z3 import *

solver = Solver()

# Days 1..7, use 1-indexed lists for clarity (index 0 unused)
kitten = [Int(f'kitten_{i}') for i in range(8)]  # 0..2
puppy = [Int(f'puppy_{i}') for i in range(8)]    # 0..2

# Domain constraints: 0=Himalayan/Manx/Siamese for kitten, 0=Greyhound/Newfoundland/Rottweiler for puppy
for i in range(1, 8):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# 1. Greyhounds on day 1
solver.add(puppy[1] == 0)

# 2. No breed on consecutive days
for i in range(1, 7):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
# puppy[1]=0 (Greyhound), so puppy[7] != 0
solver.add(puppy[7] != 0)
# kitten[1] cannot be 0 (Himalayan) per condition 4, but we still enforce that kitten[7] != kitten[1]
# Actually condition says "Any breed featured on day 1" — that includes the kitten breed on day 1.
solver.add(kitten[7] != kitten[1])

# 4. Himalayans (kitten == 0) exactly three days, not on day 1
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(1, 8)]) == 3)
solver.add(kitten[1] != 0)

# 5. Rottweilers (puppy == 2) not on day 7, nor on any day with Himalayans
solver.add(puppy[7] != 2)
for i in range(1, 8):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Evaluate options
# Option A: Greyhounds and Siamese on day 2
opt_a = And(puppy[2] == 0, kitten[2] == 2)
# Option B: Greyhounds and Himalayans on day 7
opt_b = And(puppy[7] == 0, kitten[7] == 0)
# Option C: Rottweilers and Himalayans on day 4
opt_c = And(puppy[4] == 2, kitten[4] == 0)
# Option D: Rottweilers and Manx on day 5
opt_d = And(puppy[5] == 2, kitten[5] == 1)
# Option E: Newfoundlands and Manx on day 6
opt_e = And(puppy[6] == 1, kitten[6] == 1)

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