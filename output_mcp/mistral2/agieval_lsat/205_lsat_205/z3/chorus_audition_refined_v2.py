from z3 import *

solver = Solver()

# Declare the positions (1 to 6) as a list of integers representing the singers
# We will use 0 to 5 to represent the singers in the order: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
# This mapping is critical for correct constraint application

# Define the singers as constants for clarity
Kammer, Lugo, Trillo, Waite, Yoshida, Zinn = 0, 1, 2, 3, 4, 5

# The order list represents the sequence of singers in positions 0 to 5 (1st to 6th)
order = [Int(f'order_{i}') for i in range(6)]

# Each position is assigned a unique singer
solver.add(Distinct(order))
for i in range(6):
    solver.add(order[i] >= 0, order[i] <= 5)

# Recorded auditions: Kammer (0) and Lugo (1) are recorded
recorded = [Kammer, Lugo]

# The fourth audition (index 3) cannot be recorded
solver.add(Not(Or([order[3] == r for r in recorded])))

# The fifth audition (index 4) must be recorded
solver.add(Or([order[4] == r for r in recorded]))

# Waite's audition (3) must take place earlier than the two recorded auditions
# This means Waite must be in a position before both recorded auditions
# We need to ensure that Waite is before both recorded auditions in the order
waite_pos = None
for i in range(6):
    solver.add(If(order[i] == Waite, 
                  And([
                      Or([order[j] == r for j in range(i+1, 6)])
                      for r in recorded
                  ]), 
                  True))

# Kammer's audition (0) must take place earlier than Trillo's audition (2)
# This means Kammer must be in a position before Trillo
for i in range(6):
    solver.add(If(order[i] == Kammer, 
                  Or([order[j] == Trillo for j in range(i+1, 6)]), 
                  True))

# Zinn's audition (5) must take place earlier than Yoshida's audition (4)
# This means Zinn must be in a position before Yoshida
for i in range(6):
    solver.add(If(order[i] == Zinn, 
                  Or([order[j] == Yoshida for j in range(i+1, 6)]), 
                  True))

# Additional constraint: Kammer's audition is immediately before Yoshida's
# This means there exists an i such that order[i] = Kammer and order[i+1] = Yoshida
solver.add(Or([
    And(order[i] == Kammer, order[i+1] == Yoshida)
    for i in range(5)
]))

# Base constraints are set. Now evaluate the multiple-choice options.

# Option A: Kammer's audition is second (index 1)
opt_A = (order[1] == Kammer)

# Option B: Trillo's audition is fourth (index 3)
opt_B = (order[3] == Trillo)

# Option C: Waite's audition is third (index 2)
opt_C = (order[2] == Waite)

# Option D: Yoshida's audition is sixth (index 5)
opt_D = (order[5] == Yoshida)

# Option E: Zinn's audition is second (index 1)
opt_E = (order[1] == Zinn)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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