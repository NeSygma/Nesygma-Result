from z3 import *

solver = Solver()

# Declare position variables for each singer
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_T = Int('pos_T')
pos_W = Int('pos_W')
pos_Y = Int('pos_Y')
pos_Z = Int('pos_Z')

# All positions are between 1 and 6 inclusive
solver.add(pos_K >= 1, pos_K <= 6)
solver.add(pos_L >= 1, pos_L <= 6)
solver.add(pos_T >= 1, pos_T <= 6)
solver.add(pos_W >= 1, pos_W <= 6)
solver.add(pos_Y >= 1, pos_Y <= 6)
solver.add(pos_Z >= 1, pos_Z <= 6)

# All positions are distinct
solver.add(Distinct([pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]))

# Constraint: The fourth audition cannot be recorded (i.e., not Kammer or Lugo)
solver.add(pos_K != 4)
solver.add(pos_L != 4)

# Constraint: The fifth audition must be recorded (i.e., Kammer or Lugo)
solver.add(Or(pos_K == 5, pos_L == 5))

# Constraint: Waite's audition must take place earlier than the two recorded auditions
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)

# Constraint: Kammer's audition must take place earlier than Trillo's audition
solver.add(pos_K < pos_T)

# Constraint: Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos_Z < pos_Y)

# Now test each answer choice
found_options = []
for letter, constr in [
    ("A", pos_K == 6),
    ("B", pos_L == 6),
    ("C", pos_T == 6),
    ("D", pos_W == 6),
    ("E", pos_Z == 6)
]:
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