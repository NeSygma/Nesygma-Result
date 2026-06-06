from z3 import *

solver = Solver()

# Representatives: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
K, M, P, Q, S, T, U = Ints('K M P Q S T U')

# Domains: each rep works in exactly one zone (1, 2, or 3)
reps = [K, M, P, Q, S, T, U]
for r in reps:
    solver.add(r >= 1, r <= 3)

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(P == 1, T == 1))
solver.add(Not(And(P == 1, T == 1)))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(T == 2, U == 2))
solver.add(Not(And(T == 2, U == 2)))

# Condition 3: Parra and Quinn work in the same sales zone.
solver.add(P == Q)

# Condition 4: Stuckey and Udall work in the same sales zone.
solver.add(S == U)

# Condition 5: More reps in Zone 3 than in Zone 2.
zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Now test each option
# Option A: Kim and Stuckey both work in Zone 1.
opt_a = And(K == 1, S == 1)

# Option B: Kim and Stuckey both work in Zone 3.
opt_b = And(K == 3, S == 3)

# Option C: Mahr and Stuckey both work in Zone 3.
opt_c = And(M == 3, S == 3)

# Option D: Mahr and Udall both work in Zone 3.
opt_d = And(M == 3, U == 3)

# Option E: Parra and Stuckey both work in Zone 1. ("Zone I" = Zone 1)
opt_e = And(P == 1, S == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        m = solver.model()
        for r_name, r_var in [("K", K), ("M", M), ("P", P), ("Q", Q), ("S", S), ("T", T), ("U", U)]:
            print(f"  {r_name} = {m[r_var]}")
    else:
        print(f"Option {letter}: UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print(f"STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")