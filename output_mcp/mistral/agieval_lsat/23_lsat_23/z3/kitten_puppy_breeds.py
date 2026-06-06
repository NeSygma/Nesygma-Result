from z3 import *

# Define breeds
KittenBreed = EnumSort('KittenBreed', ['Himalayan', 'Manx', 'Siamese'])
PuppyBreed = EnumSort('PuppyBreed', ['Greyhound', 'Newfoundland', 'Rottweiler'])
Himalayan, Manx, Siamese = KittenBreed
Greyhound, Newfoundland, Rottweiler = PuppyBreed

# Days 0 through 6 (representing day 1 through day 7)
solver = Solver()

# For each day, we have a kitten breed and a puppy breed
kitten = [Const(f'kitten_{i}', KittenBreed) for i in range(7)]
puppy = [Const(f'puppy_{i}', PuppyBreed) for i in range(7)]

# Constraint 1: Greyhounds are featured on day 1 (index 0)
solver.add(puppy[0] == Greyhound)

# Constraint 2: No breed is featured on any two consecutive days
for i in range(6):
    # Kitten breeds on consecutive days must differ
    solver.add(kitten[i] != kitten[i+1])
    # Puppy breeds on consecutive days must differ
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Any breed featured on day 1 (index 0) is not featured on day 7 (index 6)
# Day 1 kitten breed not on day 7
solver.add(kitten[0] != kitten[6])
# Day 1 puppy breed not on day 7
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans are featured on exactly three days, but not on day 1 (index 0)
solver.add(Sum([If(kitten[i] == Himalayan, 1, 0) for i in range(7)]) == 3)
solver.add(kitten[0] != Himalayan)  # Not on day 1

# Constraint 5: Rottweilers are not featured on day 7 (index 6), nor on any day that features Himalayans
solver.add(puppy[6] != Rottweiler)  # Not on day 7
for i in range(7):
    solver.add(Implies(kitten[i] == Himalayan, puppy[i] != Rottweiler))

# Base constraints are set. Now evaluate multiple-choice options.

# Option B: Greyhounds are featured on every day that Himalayans are.
# This means: If Himalayan is featured on day i, then Greyhound must be featured on day i.
opt_b_constr = And([
    Implies(kitten[i] == Himalayan, puppy[i] == Greyhound) for i in range(7)
])

# Option C: Himalayans are featured on every day that Greyhounds are.
# This means: If Greyhound is featured on day i, then Himalayan must be featured on day i.
opt_c_constr = And([
    Implies(puppy[i] == Greyhound, kitten[i] == Himalayan) for i in range(7)
])

# Option D: Himalayans are featured on every day that Rottweilers are not.
# This means: If Rottweiler is not featured on day i, then Himalayan must be featured on day i.
opt_d_constr = And([
    Implies(puppy[i] != Rottweiler, kitten[i] == Himalayan) for i in range(7)
])

# Option E: Rottweilers are featured on every day that Himalayans are not.
# This means: If Himalayan is not featured on day i, then Rottweiler must be featured on day i.
opt_e_constr = And([
    Implies(kitten[i] != Himalayan, puppy[i] == Rottweiler) for i in range(7)
])

# Evaluate each option
found_options = []
for letter, constr in [("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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