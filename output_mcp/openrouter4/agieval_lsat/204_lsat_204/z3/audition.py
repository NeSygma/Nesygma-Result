from z3 import *

solver = Solver()

# Positions 1-6
K, L, T, W, Y, Z = Ints('K L T W Y Z')
singers = [K, L, T, W, Y, Z]

# Each position is between 1 and 6
for s in singers:
    solver.add(s >= 1, s <= 6)

# All positions are distinct
solver.add(Distinct(singers))

# Kammer (K) and Lugo (L) are recorded
# The other four are not recorded

# Constraint 1: The fourth audition cannot be recorded.
# Position 4 cannot be Kammer or Lugo
solver.add(K != 4)
solver.add(L != 4)

# Constraint 2: The fifth audition must be recorded.
# Position 5 must be Kammer or Lugo
solver.add(Or(K == 5, L == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions.
# W < K AND W < L
solver.add(W < K)
solver.add(W < L)

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition.
# K < T
solver.add(K < T)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition.
# Z < Y
solver.add(Z < Y)

# Now evaluate each option for the sixth position
options = {
    "A": (K == 6, "Kammer"),
    "B": (L == 6, "Lugo"),
    "C": (T == 6, "Trillo"),
    "D": (W == 6, "Waite"),
    "E": (Z == 6, "Zinn")
}

found_options = []
for letter, (constr, name) in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} ({name}) is possible:")
        print(f"  K={m[K]}, L={m[L]}, T={m[T]}, W={m[W]}, Y={m[Y]}, Z={m[Z]}")
    else:
        print(f"Option {letter} ({name}) is impossible.")
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