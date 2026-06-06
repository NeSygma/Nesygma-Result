from z3 import *

solver = Solver()
# Define variables for days 1..7
kitten = [Int(f'kitten_{i}') for i in range(8)]  # index 0 unused
puppy = [Int(f'puppy_{i}') for i in range(8)]

# Domain constraints: each variable in {0,1,2}
for i in range(1,8):
    solver.add(Or(kitten[i]==0, kitten[i]==1, kitten[i]==2))
    solver.add(Or(puppy[i]==0, puppy[i]==1, puppy[i]==2))

# No breed on consecutive days (for kitten and puppy)
for i in range(1,7):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Any breed featured on day 1 is not featured on day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Greyhounds are featured on day 1
solver.add(puppy[1] == 0)

# Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kitten[i]==0, 1, 0) for i in range(1,8)]) == 3)
solver.add(kitten[1] != 0)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[7] != 2)
for i in range(1,8):
    solver.add(Or(kitten[i] != 0, puppy[i] != 2))

# Define option constraints
opt_a_constr = And([
    kitten[1]==0, kitten[2]==1, kitten[3]==2, kitten[4]==0, kitten[5]==1, kitten[6]==0, kitten[7]==2
])
opt_b_constr = And([
    kitten[1]==1, kitten[2]==0, kitten[3]==2, kitten[4]==0, kitten[5]==1, kitten[6]==0, kitten[7]==1
])
opt_c_constr = And([
    kitten[1]==1, kitten[2]==0, kitten[3]==1, kitten[4]==0, kitten[5]==2, kitten[6]==1, kitten[7]==2
])
opt_d_constr = And([
    kitten[1]==2, kitten[2]==0, kitten[3]==1, kitten[4]==0, kitten[5]==2, kitten[6]==2, kitten[7]==0
])
opt_e_constr = And([
    kitten[1]==2, kitten[2]==0, kitten[3]==2, kitten[4]==0, kitten[5]==1, kitten[6]==2, kitten[7]==0
])

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