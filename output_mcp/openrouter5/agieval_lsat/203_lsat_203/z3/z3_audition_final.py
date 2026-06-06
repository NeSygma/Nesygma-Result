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

# Evaluate each option: which CANNOT be the second audition?
found_options = []
for letter, constr in [("A", K == 2), ("B", L == 2), ("C", T == 2), ("D", W == 2), ("E", Z == 2)]:
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