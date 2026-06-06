from z3 import *

solver = Solver()

# Sales representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Zones: 1, 2, 3
# Each rep works in exactly one zone (1, 2, or 3)

Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
reps = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

# Each rep is assigned to zone 1, 2, or 3
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

# Define option constraints: which reps are in Zone 3
# Option A: Kim, Mahr in Zone 3 (and only them)
opt_a = And(
    Kim == 3, Mahr == 3,
    Parra != 3, Quinn != 3, Stuckey != 3, Tiao != 3, Udall != 3
)

# Option B: Kim, Tiao in Zone 3 (and only them)
opt_b = And(
    Kim == 3, Tiao == 3,
    Mahr != 3, Parra != 3, Quinn != 3, Stuckey != 3, Udall != 3
)

# Option C: Parra, Quinn in Zone 3 (and only them)
opt_c = And(
    Parra == 3, Quinn == 3,
    Kim != 3, Mahr != 3, Stuckey != 3, Tiao != 3, Udall != 3
)

# Option D: Stuckey, Tiao, Udall in Zone 3 (and only them)
opt_d = And(
    Stuckey == 3, Tiao == 3, Udall == 3,
    Kim != 3, Mahr != 3, Parra != 3, Quinn != 3
)

# Option E: Parra, Quinn, Stuckey, Udall in Zone 3 (and only them)
opt_e = And(
    Parra == 3, Quinn == 3, Stuckey == 3, Udall == 3,
    Kim != 3, Mahr != 3, Tiao != 3
)

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