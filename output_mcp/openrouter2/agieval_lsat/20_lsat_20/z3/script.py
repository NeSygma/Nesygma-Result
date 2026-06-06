from z3 import *

solver = Solver()

# Define variables for kitten and puppy breeds for days 1..7 (indices 0..6)
kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy  = [Int(f'puppy_{i}')  for i in range(7)]

# Domain constraints: each breed is 0 (H/M/S for kitten) or 0 (G/N/R for puppy)
for i in range(7):
    solver.add(And(kitten[i] >= 0, kitten[i] <= 2))
    solver.add(And(puppy[i]  >= 0, puppy[i]  <= 2))

# Greyhounds are featured on day 1
solver.add(puppy[0] == 0)  # 0 represents Greyhound

# No breed is featured on any two consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i]   != puppy[i+1])

# Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0]  != puppy[6])

# Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(kitten[0] != 0)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != 2)  # 2 represents Rottweiler
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Additional assumption: Himalayans are not featured on day 2
solver.add(kitten[1] != 0)

# Option constraints
opt_a_constr = kitten[2] == 1  # Manx on day 3
opt_b_constr = kitten[3] == 2  # Siamese on day 4
opt_c_constr = puppy[4]  == 2  # Rottweiler on day 5
opt_d_constr = kitten[5] == 0  # Himalayan on day 6
opt_e_constr = puppy[6]  == 0  # Greyhound on day 7

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr),
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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