from z3 import *

solver = Solver()

# Singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# Positions 1-6
K = Int('K')  # Kammer
L = Int('L')  # Lugo
T = Int('T')  # Trillo
W = Int('W')  # Waite
Y = Int('Y')  # Yoshida
Z = Int('Z')  # Zinn

singers = [K, L, T, W, Y, Z]

# All positions are between 1 and 6
for s in singers:
    solver.add(s >= 1, s <= 6)

# All different positions
solver.add(Distinct(singers))

# Recorded: Kammer and Lugo
# Not recorded: Trillo, Waite, Yoshida, Zinn

# Constraint 1: Fourth audition cannot be recorded (not K or L)
solver.add(K != 4)
solver.add(L != 4)

# Constraint 2: Fifth audition must be recorded (K or L)
solver.add(Or(K == 5, L == 5))

# Constraint 3: Waite's audition earlier than both recorded auditions
solver.add(W < K)
solver.add(W < L)

# Constraint 4: Kammer earlier than Trillo
solver.add(K < T)

# Constraint 5: Zinn earlier than Yoshida
solver.add(Z < Y)

# Additional condition: Kammer immediately before Yoshida
solver.add(K + 1 == Y)

# Now test each option
found_options = []

# (A) Kammer's audition is second
solver.push()
solver.add(K == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Trillo's audition is fourth
solver.push()
solver.add(T == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Waite's audition is third
solver.push()
solver.add(W == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Yoshida's audition is sixth
solver.push()
solver.add(Y == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Zinn's audition is second
solver.push()
solver.add(Z == 2)
if solver.check() == sat:
    found_options.append("E")
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