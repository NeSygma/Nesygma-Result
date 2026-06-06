from z3 import *

solver = Solver()

# Representatives: 0=Kim, 1=Mahr, 2=Parra, 3=Quinn, 4=Stuckey, 5=Tiao, 6=Udall
# Zones: 1, 2, 3
z = [Int(f'z_{i}') for i in range(7)]
names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Each rep works in exactly one zone (1, 2, or 3)
for i in range(7):
    solver.add(z[i] >= 1, z[i] <= 3)

# Condition 1: Either Parra (2) or Tiao (5) but not both works in Zone 1
solver.add(Or(z[2] == 1, z[5] == 1))
solver.add(Not(And(z[2] == 1, z[5] == 1)))

# Condition 2: Either Tiao (5) or Udall (6) but not both works in Zone 2
solver.add(Or(z[5] == 2, z[6] == 2))
solver.add(Not(And(z[5] == 2, z[6] == 2)))

# Condition 3: Parra (2) and Quinn (3) work in the same zone
solver.add(z[2] == z[3])

# Condition 4: Stuckey (4) and Udall (6) work in the same zone
solver.add(z[4] == z[6])

# Condition 5: More reps in Zone 3 than in Zone 2
zone3_count = Sum([If(z[i] == 3, 1, 0) for i in range(7)])
zone2_count = Sum([If(z[i] == 2, 1, 0) for i in range(7)])
solver.add(zone3_count > zone2_count)

# Additional condition from the question: More reps in Zone 1 than in Zone 3
zone1_count = Sum([If(z[i] == 1, 1, 0) for i in range(7)])
solver.add(zone1_count > zone3_count)

# Now evaluate each option
found_options = []

# Option A: Kim works in Zone 2
opt_a = (z[0] == 2)
# Option B: Mahr works in Zone 2
opt_b = (z[1] == 2)
# Option C: Parra works in Zone 3
opt_c = (z[2] == 3)
# Option D: Tiao works in Zone 1
opt_d = (z[5] == 1)
# Option E: Udall works in Zone 3
opt_e = (z[6] == 3)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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