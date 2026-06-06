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

# Each singer in a distinct position 1-6
for s in singers:
    solver.add(s >= 1, s <= 6)
solver.add(Distinct(singers))

# Recorded singers: Kammer and Lugo
# Not recorded: Trillo, Waite, Yoshida, Zinn

# Constraint 1: Fourth audition cannot be recorded
# So position 4 is NOT Kammer and NOT Lugo
solver.add(K != 4)
solver.add(L != 4)

# Constraint 2: Fifth audition must be recorded
# So position 5 IS Kammer OR Lugo
solver.add(Or(K == 5, L == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(K < T)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(Z < Y)

# Now check which option CANNOT be the second audition
# We test each option: can that singer be in position 2?
# If adding "singer == 2" makes it UNSAT, that singer CANNOT be second.

options = [
    ("A", K == 2),  # Kammer
    ("B", L == 2),  # Lugo
    ("C", T == 2),  # Trillo
    ("D", W == 2),  # Waite
    ("E", Z == 2),  # Zinn
]

cannot_be_second = []
can_be_second = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        can_be_second.append(letter)
    else:
        cannot_be_second.append(letter)
    solver.pop()

print(f"Can be second: {can_be_second}")
print(f"Cannot be second: {cannot_be_second}")

if len(cannot_be_second) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_second[0]}")
elif len(cannot_be_second) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be second {cannot_be_second}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be second")