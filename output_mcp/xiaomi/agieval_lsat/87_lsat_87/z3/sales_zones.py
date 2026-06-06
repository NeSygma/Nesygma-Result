from z3 import *

solver = Solver()

# Sales representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Zones: 1, 2, 3 (represented as integers 1, 2, 3)

Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
reps = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

# Each rep works in exactly one zone (1, 2, or 3)
for r in reps:
    solver.add(Or(r == 1, r == 2, r == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(Parra == 1, Tiao == 1))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(Tiao == 2, Udall == 2))

# Condition 3: Parra and Quinn work in the same sales zone
solver.add(Parra == Quinn)

# Condition 4: Stuckey and Udall work in the same sales zone
solver.add(Stuckey == Udall)

# Condition 5: More reps in Zone 3 than in Zone 2
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Additional condition: Mahr and Stuckey work in the same sales zone
solver.add(Mahr == Stuckey)

# Define option constraints
opt_a = (Kim == 2)       # Kim works in Zone 2
opt_b = (Mahr == 1)      # Mahr works in Zone 1
opt_c = (Parra == 3)     # Parra works in Zone 3
opt_d = (Stuckey == 2)   # Stuckey works in Zone 2
opt_e = (Tiao == 1)      # Tiao works in Zone 1

found_options = []
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