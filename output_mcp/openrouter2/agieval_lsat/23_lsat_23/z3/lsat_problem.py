from z3 import *

solver = Solver()
# Variables: kitten and puppy breeds for days 1..7
# 0=H,1=M,2=S for kittens; 0=G,1=N,2=R for puppies
kitten = [Int(f'kitten_{i}') for i in range(1,8)]
puppy = [Int(f'puppy_{i}') for i in range(1,8)]

# Domain constraints
for k in kitten:
    solver.add(k >= 0, k <= 2)
for p in puppy:
    solver.add(p >= 0, p <= 2)

# Greyhounds on day 1
solver.add(puppy[0] == 0)

# No breed on consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayans on exactly three days, not day 1
solver.add(Sum([If(k == 0, 1, 0) for k in kitten]) == 3)
solver.add(kitten[0] != 0)

# Rottweilers not on day 7
solver.add(puppy[6] != 2)
# Rottweilers not on any day that features Himalayans
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Helper counts for option A
# kitten counts
kitten_counts = [Sum([If(k == b, 1, 0) for k in kitten]) for b in range(3)]
# puppy counts
puppy_counts = [Sum([If(p == b, 1, 0) for p in puppy]) for b in range(3)]
counts = kitten_counts + puppy_counts
# Option A: exactly four breeds appear on 3 days
opt_a_constr = Sum([If(c == 3, 1, 0) for c in counts]) == 4

# Option B: Greyhounds on every day that Himalayans are
opt_b_constr = And([Implies(kitten[i] == 0, puppy[i] == 0) for i in range(7)])

# Option C: Himalayans on every day that Greyhounds are
opt_c_constr = And([Implies(puppy[i] == 0, kitten[i] == 0) for i in range(7)])

# Option D: Himalayans on every day that Rottweilers are not
opt_d_constr = And([Implies(puppy[i] != 2, kitten[i] == 0) for i in range(7)])

# Option E: Rottweilers on every day that Himalayans are not
opt_e_constr = And([Implies(kitten[i] != 0, puppy[i] == 2) for i in range(7)])

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