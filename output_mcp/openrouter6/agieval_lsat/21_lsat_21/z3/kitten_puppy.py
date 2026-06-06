from z3 import *

# Define enumerations for kitten and puppy breeds
KittenBreed = Datatype('KittenBreed')
KittenBreed.declare('H', 'M', 'S')
KittenBreed = KittenBreed.create()

PuppyBreed = Datatype('PuppyBreed')
PuppyBreed.declare('G', 'N', 'R')
PuppyBreed = PuppyBreed.create()

# Variables for each day (1..7) -> indices 0..6
K = [KittenBreed(f'K_{d}') for d in range(1, 8)]
P = [PuppyBreed(f'P_{d}') for d in range(1, 8)]

solver = Solver()

# Base constraints
# 1. Greyhounds on day 1
solver.add(P[0] == PuppyBreed.G)

# 2. No breed on consecutive days (for each breed type)
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# 3. Any breed on day 1 not on day 7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# 4. Himalayans exactly three days, not on day 1
himalayan_count = Sum([If(K[d] == KittenBreed.H, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)
solver.add(K[0] != KittenBreed.H)

# 5. Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(P[6] != PuppyBreed.R)
for d in range(7):
    solver.add(Implies(K[d] == KittenBreed.H, P[d] != PuppyBreed.R))

# Define option constraints
opt_a_constr = And(P[1] == PuppyBreed.G, K[1] == KittenBreed.S)  # day 2
opt_b_constr = And(P[6] == PuppyBreed.G, K[6] == KittenBreed.H)  # day 7
opt_c_constr = And(P[3] == PuppyBreed.R, K[3] == KittenBreed.H)  # day 4
opt_d_constr = And(P[4] == PuppyBreed.R, K[4] == KittenBreed.M)  # day 5
opt_e_constr = And(P[5] == PuppyBreed.N, K[5] == KittenBreed.M)  # day 6

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