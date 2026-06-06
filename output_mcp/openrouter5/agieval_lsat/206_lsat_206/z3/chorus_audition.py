from z3 import *

solver = Solver()

# Six singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# Positions 1 through 6 (1-indexed for readability)
K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Each singer gets a distinct position from 1 to 6
singers = [K, L, T, W, Y, Z]
solver.add(Distinct(singers))
for s in singers:
    solver.add(s >= 1, s <= 6)

# Recorded auditions: Kammer (K) and Lugo (L)
# The fourth audition cannot be recorded.
# So K != 4 and L != 4
solver.add(K != 4)
solver.add(L != 4)

# The fifth audition must be recorded.
# So either K == 5 or L == 5 (since only K and L are recorded)
solver.add(Or(K == 5, L == 5))

# Waite's audition must take place earlier than the two recorded auditions.
# So W < K and W < L
solver.add(W < K)
solver.add(W < L)

# Kammer's audition must take place earlier than Trillo's audition.
solver.add(K < T)

# Zinn's audition must take place earlier than Yoshida's audition.
solver.add(Z < Y)

# Now evaluate each option for Yoshida's position
# Option A: fifth -> Y == 5
# Option B: fourth -> Y == 4
# Option C: third -> Y == 3
# Option D: second -> Y == 2
# Option E: first -> Y == 1

found_options = []
for letter, constr in [("A", Y == 5), ("B", Y == 4), ("C", Y == 3), ("D", Y == 2), ("E", Y == 1)]:
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