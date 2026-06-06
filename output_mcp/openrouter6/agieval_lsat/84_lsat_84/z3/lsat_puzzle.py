from z3 import *

# Base constraints
solver = Solver()

# Declare zone variables for each person
kim = Int('kim')
mahr = Int('mahr')
parra = Int('parra')
quinn = Int('quinn')
stuckey = Int('stuckey')
tiao = Int('tiao')
udall = Int('udall')

people = [kim, mahr, parra, quinn, stuckey, tiao, udall]

# Each person works in exactly one zone: 1, 2, or 3
for p in people:
    solver.add(p >= 1, p <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1.
# Exactly one of parra==1 and tiao==1
solver.add(Or(And(parra == 1, tiao != 1), And(parra != 1, tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(And(tiao == 2, udall != 2), And(tiao != 2, udall == 2)))

# Constraint 3: Parra and Quinn work in the same sales zone.
solver.add(parra == quinn)

# Constraint 4: Stuckey and Udall work in the same sales zone.
solver.add(stuckey == udall)

# Constraint 5: More representatives in Zone 3 than in Zone 2.
# Count zone 3 and zone 2
count_zone3 = Sum([If(p == 3, 1, 0) for p in people])
count_zone2 = Sum([If(p == 2, 1, 0) for p in people])
solver.add(count_zone3 > count_zone2)

# Now evaluate each option
found_options = []

# Option A: Kim and Stuckey both work in Zone 1.
opt_a = And(kim == 1, stuckey == 1)
# Option B: Kim and Stuckey both work in Zone 3.
opt_b = And(kim == 3, stuckey == 3)
# Option C: Mahr and Stuckey both work in Zone 3.
opt_c = And(mahr == 3, stuckey == 3)
# Option D: Mahr and Udall both work in Zone 3.
opt_d = And(mahr == 3, udall == 3)
# Option E: Parra and Stuckey both work in Zone 1.
opt_e = And(parra == 1, stuckey == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    # We want to find which option must be false, i.e., adding it makes the problem unsatisfiable.
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# According to the problem, exactly one option must be false.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")