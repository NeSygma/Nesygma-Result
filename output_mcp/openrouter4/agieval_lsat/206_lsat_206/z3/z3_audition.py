from z3 import *

solver = Solver()

# Variables: positions 1-6 for each singer
pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z = Ints('pos_K pos_L pos_T pos_W pos_Y pos_Z')

# Domain: each position is 1-6
solver.add(pos_K >= 1, pos_K <= 6)
solver.add(pos_L >= 1, pos_L <= 6)
solver.add(pos_T >= 1, pos_T <= 6)
solver.add(pos_W >= 1, pos_W <= 6)
solver.add(pos_Y >= 1, pos_Y <= 6)
solver.add(pos_Z >= 1, pos_Z <= 6)

# All distinct positions
solver.add(Distinct(pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z))

# Constraint 1: The fourth audition cannot be recorded (not K or L)
# So position 4 is not assigned to K or L
solver.add(pos_K != 4)
solver.add(pos_L != 4)

# Constraint 2: The fifth audition must be recorded (must be K or L)
solver.add(Or(pos_K == 5, pos_L == 5))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(pos_K < pos_T)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos_Z < pos_Y)

# Now check each possible position for Yoshida
# Options: (A)fifth=5, (B)fourth=4, (C)third=3, (D)second=2, (E)first=1

found_options = []
for letter, pos_val in [("A", 5), ("B", 4), ("C", 3), ("D", 2), ("E", 1)]:
    solver.push()
    solver.add(pos_Y == pos_val)
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