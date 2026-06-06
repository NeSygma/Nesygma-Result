from z3 import *

solver = Solver()

# Days 0..6 correspond to day 1..7
k = [Int(f'k_{i}') for i in range(7)]
p = [Int(f'p_{i}') for i in range(7)]

# Domain constraints: 0=Himalayan/Manx/Siamese, 0=Greyhound/Newfoundland/Rottweiler
for i in range(7):
    solver.add(0 <= k[i], k[i] <= 2)
    solver.add(0 <= p[i], p[i] <= 2)

# 1. Greyhounds on day 1
solver.add(p[0] == 0)

# 2. No breed on consecutive days (for kitten and puppy separately)
for i in range(6):
    solver.add(k[i] != k[i+1])
    solver.add(p[i] != p[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# 4. Himalayans exactly three days, not on day 1
solver.add(Sum([If(k[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(k[0] != 0)

# 5. Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(p[6] != 2)
for i in range(7):
    solver.add(Implies(k[i] == 0, p[i] != 2))

# Base constraints are now added.

# Define option constraints
# Option A: exactly four breeds each featured on three days
count_H = Sum([If(k[i] == 0, 1, 0) for i in range(7)])
count_M = Sum([If(k[i] == 1, 1, 0) for i in range(7)])
count_S = Sum([If(k[i] == 2, 1, 0) for i in range(7)])
count_G = Sum([If(p[i] == 0, 1, 0) for i in range(7)])
count_N = Sum([If(p[i] == 1, 1, 0) for i in range(7)])
count_R = Sum([If(p[i] == 2, 1, 0) for i in range(7)])

opt_a_constr = (Sum([If(count_H == 3, 1, 0),
                     If(count_M == 3, 1, 0),
                     If(count_S == 3, 1, 0),
                     If(count_G == 3, 1, 0),
                     If(count_N == 3, 1, 0),
                     If(count_R == 3, 1, 0)]) == 4)

# Option B: Greyhounds on every day that Himalayans are
opt_b_constr = And([Implies(k[i] == 0, p[i] == 0) for i in range(7)])

# Option C: Himalayans on every day that Greyhounds are
opt_c_constr = And([Implies(p[i] == 0, k[i] == 0) for i in range(7)])

# Option D: Himalayans on every day that Rottweilers are not
opt_d_constr = And([Implies(p[i] != 2, k[i] == 0) for i in range(7)])

# Option E: Rottweilers on every day that Himalayans are not
opt_e_constr = And([Implies(k[i] != 0, p[i] == 2) for i in range(7)])

# Evaluate each option
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