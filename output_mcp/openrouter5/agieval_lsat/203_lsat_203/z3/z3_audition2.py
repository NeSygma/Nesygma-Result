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

# The question asks: which CANNOT be the second audition?
# So we test each option: if adding "X is second" makes it UNSAT, then X cannot be second.
# If it's SAT, then X CAN be second.

# Option A: Kammer's audition is second
solver.push()
solver.add(K == 2)
print("A (Kammer=2):", solver.check())
solver.pop()

# Option B: Lugo's audition is second
solver.push()
solver.add(L == 2)
print("B (Lugo=2):", solver.check())
solver.pop()

# Option C: Trillo's audition is second
solver.push()
solver.add(T == 2)
print("C (Trillo=2):", solver.check())
solver.pop()

# Option D: Waite's audition is second
solver.push()
solver.add(W == 2)
print("D (Waite=2):", solver.check())
solver.pop()

# Option E: Zinn's audition is second
solver.push()
solver.add(Z == 2)
print("E (Zinn=2):", solver.check())
solver.pop()