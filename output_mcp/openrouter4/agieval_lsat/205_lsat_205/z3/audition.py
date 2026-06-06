from z3 import *

solver = Solver()

# Variables: positions 1-6
K, L, T, W, Y, Z = Ints('K L T W Y Z')

# Domain: each position is 1-6
positions = [K, L, T, W, Y, Z]
for p in positions:
    solver.add(p >= 1, p <= 6)

# All distinct
solver.add(Distinct(positions))

# Recorded: K and L (the other four are not recorded)
# Fourth audition cannot be recorded: position 4 cannot be K or L
solver.add(K != 4)
solver.add(L != 4)

# Fifth audition must be recorded: position 5 must be K or L
solver.add(Or(K == 5, L == 5))

# Waite earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Kammer earlier than Trillo
solver.add(K < T)

# Zinn earlier than Yoshida
solver.add(Z < Y)

# Additional condition: Kammer's audition is immediately before Yoshida's
solver.add(K + 1 == Y)

# Now check each option
options = [
    ("A", K == 2),
    ("B", T == 4),
    ("C", W == 3),
    ("D", Y == 6),
    ("E", Z == 2)
]

found_options = []
for letter, constr in options:
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