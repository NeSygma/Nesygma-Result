from z3 import *

# Constants for breeds
H, M, S = 0, 1, 2  # kitten breeds: Himalayan, Manx, Siamese
G, N, R = 0, 1, 2  # puppy breeds: Greyhound, Newfoundland, Rottweiler

solver = Solver()

# Variables: kitten[d] and puppy[d] for days 1..7
kitten = [Int(f'kitten_{d}') for d in range(1, 8)]
puppy = [Int(f'puppy_{d}') for d in range(1, 8)]

# Domain constraints
for d in range(7):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Condition 1: Greyhounds on day 1
solver.add(puppy[0] == G)

# Condition 2: No breed on any two consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Condition 3: Any breed featured on day 1 is not featured on day 7
# Day 1 features kitten[0] and puppy[0]=G
solver.add(kitten[0] != kitten[6])  # kitten breed on day 1 != kitten breed on day 7
solver.add(puppy[6] != G)  # Greyhound (on day 1) != puppy on day 7

# Condition 4: Himalayans on exactly three days, not on day 1
solver.add(kitten[0] != H)
solver.add(Sum([If(kitten[d] == H, 1, 0) for d in range(7)]) == 3)

# Condition 5: Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != R)
for d in range(7):
    solver.add(Implies(kitten[d] == H, puppy[d] != R))

# Now evaluate each option
# Option A: Exactly four breeds are each featured on three days
# Count appearances for each breed
kitten_H_days = Sum([If(kitten[d] == H, 1, 0) for d in range(7)])
kitten_M_days = Sum([If(kitten[d] == M, 1, 0) for d in range(7)])
kitten_S_days = Sum([If(kitten[d] == S, 1, 0) for d in range(7)])
puppy_G_days = Sum([If(puppy[d] == G, 1, 0) for d in range(7)])
puppy_N_days = Sum([If(puppy[d] == N, 1, 0) for d in range(7)])
puppy_R_days = Sum([If(puppy[d] == R, 1, 0) for d in range(7)])

breed_days = [kitten_H_days, kitten_M_days, kitten_S_days,
              puppy_G_days, puppy_N_days, puppy_R_days]

# Count how many breeds appear exactly 3 times
count_three = Sum([If(bd == 3, 1, 0) for bd in breed_days])
opt_a_constr = (count_three == 4)

# Option B: Greyhounds are featured on every day that Himalayans are
opt_b_constr = And([Implies(kitten[d] == H, puppy[d] == G) for d in range(7)])

# Option C: Himalayans are featured on every day that Greyhounds are
opt_c_constr = And([Implies(puppy[d] == G, kitten[d] == H) for d in range(7)])

# Option D: Himalayans are featured on every day that Rottweilers are not
opt_d_constr = And([Implies(puppy[d] != R, kitten[d] == H) for d in range(7)])

# Option E: Rottweilers are featured on every day that Himalayans are not
opt_e_constr = And([Implies(kitten[d] != H, puppy[d] == R) for d in range(7)])

# Evaluate options using the required skeleton
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