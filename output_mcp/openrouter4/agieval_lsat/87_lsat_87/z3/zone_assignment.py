from z3 import *

solver = Solver()

# Representatives
K, M, P, Q, S, T, U = Ints('K M P Q S T U')
reps = [K, M, P, Q, S, T, U]

# Domain: each rep works in exactly one of zones 1, 2, 3
for r in reps:
    solver.add(r >= 1, r <= 3)

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
# Exactly one of (P == 1) or (T == 1) is true.
solver.add(Sum([If(P == 1, 1, 0), If(T == 1, 1, 0)]) == 1)

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Sum([If(T == 2, 1, 0), If(U == 2, 1, 0)]) == 1)

# Condition 3: Parra and Quinn work in the same sales zone.
solver.add(P == Q)

# Condition 4: Stuckey and Udall work in the same sales zone.
solver.add(S == U)

# Condition 5: More reps in Zone 3 than in Zone 2.
zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Additional condition: Mahr and Stuckey work in the same zone.
solver.add(M == S)

# Now test each option
# Option A: Kim works in Zone 2
opt_a = (K == 2)

# Option B: Mahr works in Zone 1
opt_b = (M == 1)

# Option C: Parra works in Zone 3
opt_c = (P == 3)

# Option D: Stuckey works in Zone 2
opt_d = (S == 2)

# Option E: Tiao works in Zone 1
opt_e = (T == 1)

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