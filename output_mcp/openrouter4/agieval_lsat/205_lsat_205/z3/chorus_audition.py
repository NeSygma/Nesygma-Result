from z3 import *

solver = Solver()

# Positions 1-6
K, L, T, W, Y, Z = Ints('K L T W Y Z')
auditions = [K, L, T, W, Y, Z]

# Domain: each position 1-6
for a in auditions:
    solver.add(a >= 1, a <= 6)

# All distinct positions
solver.add(Distinct(auditions))

# Fourth audition cannot be recorded (K and L are recorded)
solver.add(K != 4)
solver.add(L != 4)

# Fifth audition must be recorded (must be K or L)
solver.add(Or(K == 5, L == 5))

# Waite earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Kammer earlier than Trillo
solver.add(K < T)

# Zinn earlier than Yoshida
solver.add(Z < Y)

# Additional: Kammer's audition is immediately before Yoshida's
solver.add(Y == K + 1)

# Now evaluate each option
# Option A: Kammer's audition is second
opt_a = (K == 2)

# Option B: Trillo's audition is fourth
opt_b = (T == 4)

# Option C: Waite's audition is third
opt_c = (W == 3)

# Option D: Yoshida's audition is sixth
opt_d = (Y == 6)

# Option E: Zinn's audition is second
opt_e = (Z == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: K={m[K]}, L={m[L]}, T={m[T]}, W={m[W]}, Y={m[Y]}, Z={m[Z]}")
    else:
        print(f"Option {letter} is UNSAT")
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