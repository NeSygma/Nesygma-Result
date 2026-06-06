from z3 import *

# Define breed constants
HIMALAYAN = 0
MANX = 1
SIAMESE = 2
GREYHOUND = 0
NEWFOUNDLAND = 1
ROTTWEILER = 2

# Days 1..7 (index 0..6 for Python list)
kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy = [Int(f'puppy_{i}') for i in range(7)]

solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(Or(kitten[i] == HIMALAYAN, kitten[i] == MANX, kitten[i] == SIAMESE))
    solver.add(Or(puppy[i] == GREYHOUND, puppy[i] == NEWFOUNDLAND, puppy[i] == ROTTWEILER))

# Greyhounds on day 1 (index 0)
solver.add(puppy[0] == GREYHOUND)

# No breed on consecutive days (for each breed separately)
for b in [HIMALAYAN, MANX, SIAMESE]:
    for i in range(6):
        solver.add(Not(And(kitten[i] == b, kitten[i+1] == b)))
for b in [GREYHOUND, NEWFOUNDLAND, ROTTWEILER]:
    for i in range(6):
        solver.add(Not(And(puppy[i] == b, puppy[i+1] == b)))

# Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayans exactly three days, not on day 1
solver.add(Sum([If(kitten[i] == HIMALAYAN, 1, 0) for i in range(7)]) == 3)
solver.add(kitten[0] != HIMALAYAN)

# Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != ROTTWEILER)
for i in range(7):
    solver.add(Implies(kitten[i] == HIMALAYAN, puppy[i] != ROTTWEILER))

# Additional condition: Himalayans not on day 2 (index 1)
solver.add(kitten[1] != HIMALAYAN)

# Define option constraints
opt_a_constr = (kitten[2] == MANX)   # day 3 index 2
opt_b_constr = (kitten[3] == SIAMESE) # day 4 index 3
opt_c_constr = (puppy[4] == ROTTWEILER) # day 5 index 4
opt_d_constr = (kitten[5] == HIMALAYAN) # day 6 index 5
opt_e_constr = (puppy[6] == GREYHOUND)  # day 7 index 6

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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