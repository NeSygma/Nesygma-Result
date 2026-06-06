from z3 import *

solver = Solver()

# Six singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# Positions 1 through 6 (1-indexed for readability)
K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Each singer gets a distinct position from 1 to 6
solver.add(Distinct(K, L, T, W, Y, Z))
for v in [K, L, T, W, Y, Z]:
    solver.add(v >= 1, v <= 6)

# Recorded auditions: Kammer and Lugo
# The fourth audition cannot be recorded.
# So position 4 is NOT K and NOT L.
solver.add(K != 4)
solver.add(L != 4)

# The fifth audition must be recorded.
# So position 5 is either K or L.
solver.add(Or(K == 5, L == 5))

# Waite's audition must take place earlier than the two recorded auditions.
# So W < K and W < L.
solver.add(W < K)
solver.add(W < L)

# Kammer's audition must take place earlier than Trillo's audition.
solver.add(K < T)

# Zinn's audition must take place earlier than Yoshida's audition.
solver.add(Z < Y)

# Now test each option for being the second audition.
# Option A: Kammer's audition is second
opt_a = (K == 2)
# Option B: Lugo's audition is second
opt_b = (L == 2)
# Option C: Trillo's audition is second
opt_c = (T == 2)
# Option D: Waite's audition is second
opt_d = (W == 2)
# Option E: Zinn's audition is second
opt_e = (Z == 2)

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