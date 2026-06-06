from z3 import *

solver = Solver()

# Six singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# Positions 1 through 6 (1-indexed)
K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Each singer gets a distinct position from 1 to 6
solver.add(Distinct(K, L, T, W, Y, Z))
for v in [K, L, T, W, Y, Z]:
    solver.add(v >= 1, v <= 6)

# Recorded auditions: Kammer and Lugo
# The fourth audition cannot be recorded.
solver.add(K != 4)
solver.add(L != 4)

# The fifth audition must be recorded.
solver.add(Or(K == 5, L == 5))

# Waite's audition must take place earlier than the two recorded auditions.
solver.add(W < K)
solver.add(W < L)

# Kammer's audition must take place earlier than Trillo's audition.
solver.add(K < T)

# Zinn's audition must take place earlier than Yoshida's audition.
solver.add(Z < Y)

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("SAT - model found")
    for v in [K, L, T, W, Y, Z]:
        print(f"  {v} = {m[v]}")
else:
    print("UNSAT - base constraints inconsistent")
solver.pop()

# Now let's test each option more carefully
# The question asks: which CANNOT be the second audition?
# So we need to find which option, when forced to be position 2, makes the problem UNSAT

print("\nTesting each option:")
for letter, constr in [("A", K == 2), ("B", L == 2), ("C", T == 2), ("D", W == 2), ("E", Z == 2)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"  Option {letter} ({constr}): {result}")
    if result == sat:
        m = solver.model()
        for v in [K, L, T, W, Y, Z]:
            print(f"    {v} = {m[v]}")
    solver.pop()