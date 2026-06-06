from z3 import *

solver = Solver()

# Six singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# Positions 0-5 (1st through 6th)
K, L, T, W, Y, Z = Ints('K L T W Y Z')
singers = [K, L, T, W, Y, Z]
names = ['K', 'L', 'T', 'W', 'Y', 'Z']

# Each singer gets a distinct position 0..5
solver.add(Distinct(singers))
for s in singers:
    solver.add(s >= 0, s <= 5)

# Recorded auditions: Kammer and Lugo
# The fourth audition (position 3) cannot be recorded.
# So position 3 cannot be K or L.
solver.add(K != 3)
solver.add(L != 3)

# The fifth audition (position 4) must be recorded.
# So position 4 must be K or L.
solver.add(Or(K == 4, L == 4))

# Waite's audition must take place earlier than the two recorded auditions.
# So W < K and W < L
solver.add(W < K)
solver.add(W < L)

# Kammer's audition must take place earlier than Trillo's audition.
solver.add(K < T)

# Zinn's audition must take place earlier than Yoshida's audition.
solver.add(Z < Y)

# Additional condition: Kammer's audition is immediately before Yoshida's.
# So K + 1 == Y
solver.add(K + 1 == Y)

# Now evaluate each option
options = {
    "A": K == 1,  # Kammer's audition is second (position 1)
    "B": T == 3,  # Trillo's audition is fourth (position 3)
    "C": W == 2,  # Waite's audition is third (position 2)
    "D": Y == 5,  # Yoshida's audition is sixth (position 5)
    "E": Z == 1   # Zinn's audition is second (position 1)
}

found_options = []
for letter, constr in options.items():
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