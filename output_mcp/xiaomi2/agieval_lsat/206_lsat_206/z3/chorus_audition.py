from z3 import *

solver = Solver()

# Six singers, each assigned a position 1-6
K = Int('Kammer')
L = Int('Lugo')
T = Int('Trillo')
W = Int('Waite')
Y = Int('Yoshida')
Z = Int('Zinn')

singers = [K, L, T, W, Y, Z]

# All positions 1-6, all distinct
for s in singers:
    solver.add(s >= 1, s <= 6)
solver.add(Distinct(singers))

# Recorded: Kammer and Lugo
# Not recorded: Trillo, Waite, Yoshida, Zinn

# Constraint 1: Fourth audition cannot be recorded
solver.add(K != 4)
solver.add(L != 4)

# Constraint 2: Fifth audition must be recorded
solver.add(Or(K == 5, L == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(K < T)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(Z < Y)

# Now test each answer choice for Yoshida
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