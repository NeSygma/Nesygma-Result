from z3 import *

# Seven sales representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Three zones: Zone 1, Zone 2, Zone 3
# Each works in exactly one zone.

Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
reps = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()

# Domain constraints: each rep works in zone 1, 2, or 3
for r in reps:
    solver.add(And(r >= 1, r <= 3))

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
zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# The question asks: "Which one of the following must be false?"
# An option that "must be false" means it can never be true under the constraints.
# So we check each option: if it's unsat (impossible), that's the answer.
# If it's sat (possible), it's not "must be false".

# Let's first check the base model to understand the constraints
print("Checking base model...")
base_solver = Solver()
for r in reps:
    base_solver.add(And(r >= 1, r <= 3))
base_solver.add(Or(Parra == 1, Tiao == 1))
base_solver.add(Not(And(Parra == 1, Tiao == 1)))
base_solver.add(Or(Tiao == 2, Udall == 2))
base_solver.add(Not(And(Tiao == 2, Udall == 2)))
base_solver.add(Parra == Quinn)
base_solver.add(Stuckey == Udall)
base_solver.add(zone3_count > zone2_count)

if base_solver.check() == sat:
    m = base_solver.model()
    print("Base model found:")
    for r in reps:
        print(f"  {r} = {m[r]}")
else:
    print("Base model unsat!")

# Now evaluate each option.
# The question asks: "Which one of the following must be false?"
# So we need to find the option that is IMPOSSIBLE (unsat) under the constraints.

# Option A: Kim and Stuckey both work in Zone 1.
opt_a = And(Kim == 1, Stuckey == 1)

# Option B: Kim and Stuckey both work in Zone 3.
opt_b = And(Kim == 3, Stuckey == 3)

# Option C: Mahr and Stuckey both work in Zone 3.
opt_c = And(Mahr == 3, Stuckey == 3)

# Option D: Mahr and Udall both work in Zone 3.
opt_d = And(Mahr == 3, Udall == 3)

# Option E: Parra and Stuckey both work in Zone 1.
opt_e = And(Parra == 1, Stuckey == 1)

# We want the option that is UNSAT (must be false)
# Let's check each one
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    for r in reps:
        s.add(And(r >= 1, r <= 3))
    s.add(Or(Parra == 1, Tiao == 1))
    s.add(Not(And(Parra == 1, Tiao == 1)))
    s.add(Or(Tiao == 2, Udall == 2))
    s.add(Not(And(Tiao == 2, Udall == 2)))
    s.add(Parra == Quinn)
    s.add(Stuckey == Udall)
    s.add(zone3_count > zone2_count)
    s.add(constr)
    res = s.check()
    print(f"Option {letter}: {res}")
    if res == sat:
        print(f"  Model: {s.model()}")