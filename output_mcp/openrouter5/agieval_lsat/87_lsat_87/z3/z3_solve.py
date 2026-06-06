from z3 import *

# Seven sales representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Three zones: Zone 1, Zone 2, Zone 3
# Each works in exactly one zone.

# We'll use integer variables with domain {1, 2, 3}
Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
reps = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()

# Domain constraints: each rep works in zone 1, 2, or 3
for r in reps:
    solver.add(Or(r == 1, r == 2, r == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(Parra == 1, Tiao == 1))
solver.add(Not(And(Parra == 1, Tiao == 1)))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(Tiao == 2, Udall == 2))
solver.add(Not(And(Tiao == 2, Udall == 2)))

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(Parra == Quinn)

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(Stuckey == Udall)

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
# Count reps in Zone 3 > reps in Zone 2
zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Additional condition from the question: Mahr and Stuckey work in the same sales zone.
solver.add(Mahr == Stuckey)

# Now evaluate each option
found_options = []

# Option A: Kim works in Zone 2.
opt_a = (Kim == 2)

# Option B: Mahr works in Zone 1.
opt_b = (Mahr == 1)

# Option C: Parra works in Zone 3.
opt_c = (Parra == 3)

# Option D: Stuckey works in Zone 2.
opt_d = (Stuckey == 2)

# Option E: Tiao works in Zone 1.
opt_e = (Tiao == 1)

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