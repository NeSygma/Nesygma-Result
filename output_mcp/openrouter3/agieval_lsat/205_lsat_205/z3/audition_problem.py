from z3 import *

solver = Solver()

# Positions for each singer (1-6)
K = Int('Kammer')
L = Int('Lugo')
T = Int('Trillo')
W = Int('Waite')
Y = Int('Yoshida')
Z = Int('Zinn')

# All positions must be distinct and between 1 and 6
all_positions = [K, L, T, W, Y, Z]
solver.add([And(p >= 1, p <= 6) for p in all_positions])
solver.add(Distinct(all_positions))

# Recorded auditions: exactly Kammer and Lugo are recorded
# We'll use a function to check if a position is recorded
# But we can also use constraints: positions 4 and 5 have specific recording constraints
# Constraint 1: Fourth audition cannot be recorded
# This means: if position 4 is K or L, then it's recorded, but it cannot be recorded
# So position 4 cannot be K or L
solver.add(Or([p != 4 for p in [K, L]]))

# Constraint 2: Fifth audition must be recorded
# So position 5 must be either K or L
solver.add(Or(K == 5, L == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
# Recorded auditions are K and L
solver.add(W < K)
solver.add(W < L)

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(K < T)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(Z < Y)

# Additional condition: Kammer's audition is immediately before Yoshida's
# So Y = K + 1
solver.add(Y == K + 1)

# Now we need to check each option
# Option A: Kammer's audition is second (K == 2)
# Option B: Trillo's audition is fourth (T == 4)
# Option C: Waite's audition is third (W == 3)
# Option D: Yoshida's audition is sixth (Y == 6)
# Option E: Zinn's audition is second (Z == 2)

found_options = []

# Option A
solver.push()
solver.add(K == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B
solver.push()
solver.add(T == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C
solver.push()
solver.add(W == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D
solver.push()
solver.add(Y == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E
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