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

# Constraint 1: Greyhounds are featured on day 1
solver.add(puppy[1] == 0)  # Greyhound = 0

# Constraint 2: No breed is featured on any two consecutive days
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Constraint 4: Himalayans featured on exactly 3 days, not on day 1
solver.add(kitten[1] != 0)  # Not Himalayan on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day featuring Himalayans
solver.add(puppy[7] != 2)  # Rottweiler = 2
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Define option constraints
opt_a = And(puppy[2] == 0, kitten[2] == 2)  # Greyhounds and Siamese on day 2
opt_b = And(puppy[7] == 0, kitten[7] == 0)  # Greyhounds and Himalayans on day 7
opt_c = And(puppy[4] == 2, kitten[4] == 0)  # Rottweilers and Himalayans on day 4
opt_d = And(puppy[5] == 2, kitten[5] == 1)  # Rottweilers and Manx on day 5
opt_e = And(puppy[6] == 1, kitten[6] == 1)  # Newfoundlands and Manx on day 6

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for d in days:
            k_names = {0: "Himalayan", 1: "Manx", 2: "Siamese"}
            p_names = {0: "Greyhound", 1: "Newfoundland", 2: "Rottweiler"}
            print(f"  Day {d}: kitten={k_names[m.evaluate(kitten[d]).as_long()]}, puppy={p_names[m.evaluate(puppy[d]).as_long()]}")
    else:
        print(f"Option {letter} is UNSAT")
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