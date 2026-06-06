from z3 import *

solver = Solver()

# Declare symbolic variables for each representative's zone
# We represent zones as integers: 1, 2, 3
kim = Int('kim')
mahr = Int('mahr')
parra = Int('parra')
quinn = Int('quinn')
stuckey = Int('stuckey')
tiao = Int('tiao')
udall = Int('udall')

# Each representative works in exactly one zone
solver.add(kim >= 1, kim <= 3)
solver.add(mahr >= 1, mahr <= 3)
solver.add(parra >= 1, parra <= 3)
solver.add(quinn >= 1, quinn <= 3)
solver.add(stuckey >= 1, stuckey <= 3)
solver.add(tiao >= 1, tiao <= 3)
solver.add(udall >= 1, udall <= 3)

# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(parra == 1, tiao != 1), And(tiao == 1, parra != 1)))

# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(tiao == 2, udall != 2), And(udall == 2, tiao != 2)))

# Parra and Quinn work in the same sales zone
solver.add(parra == quinn)

# Stuckey and Udall work in the same sales zone
solver.add(stuckey == udall)

# There are more sales representatives working in Zone 3 than in Zone 2
zone_counts = [
    kim, mahr, parra, quinn, stuckey, tiao, udall
]
count_zone1 = Sum([If(z == 1, 1, 0) for z in zone_counts])
count_zone2 = Sum([If(z == 2, 1, 0) for z in zone_counts])
count_zone3 = Sum([If(z == 3, 1, 0) for z in zone_counts])

solver.add(count_zone3 > count_zone2)

# If more sales representatives work in Zone 1 than in Zone 3
solver.add(count_zone1 > count_zone3)

# Base constraints are set. Now evaluate each option.

# Define the options as constraints
opt_a_constr = (kim == 2)
opt_b_constr = (mahr == 2)
opt_c_constr = (parra == 3)
opt_d_constr = (tiao == 1)
opt_e_constr = (udall == 3)

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