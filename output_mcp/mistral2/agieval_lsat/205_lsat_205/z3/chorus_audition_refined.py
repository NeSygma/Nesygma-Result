from z3 import *

solver = Solver()

# Declare the positions (1 to 6)
# We will model the order as a list of singers, where the index represents the position
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']
order = [Int(f'order_{i}') for i in range(6)]

# Each position is assigned a unique singer
solver.add(Distinct(order))
for i in range(6):
    solver.add(order[i] >= 0, order[i] < 6)

# Helper function to get the index of a singer in the order
# Since order[i] is an Int representing a singer, we need to map it back to the singer name
# We will use a list of possible singer indices (0 to 5) and map them to names

# Recorded auditions: Kammer (0) and Lugo (1) are recorded
recorded_indices = [0, 1]

# The fourth audition (index 3) cannot be recorded
solver.add(Not(Or([order[3] == i for i in recorded_indices])))

# The fifth audition (index 4) must be recorded
solver.add(Or([order[4] == i for i in recorded_indices]))

# Waite's audition (index 3) must take place earlier than the two recorded auditions
waite_index = 3
solver.add(Or([
    And(order[i] == waite_index, 
        Or([
            And(order[j] == r, j > i) for j in range(5) for r in recorded_indices
        ]))
    for i in range(5)
]))

# Kammer's audition (index 0) must take place earlier than Trillo's audition (index 2)
trillo_index = 2
solver.add(Or([
    And(order[i] == 0, 
        Or([order[j] == trillo_index for j in range(i+1, 6)]))
    for i in range(5)
]))

# Zinn's audition (index 5) must take place earlier than Yoshida's audition (index 4)
yoshida_index = 4
zinn_index = 5
solver.add(Or([
    And(order[i] == zinn_index, 
        Or([order[j] == yoshida_index for j in range(i+1, 6)]))
    for i in range(5)
]))

# Additional constraint: Kammer's audition is immediately before Yoshida's
solver.add(Or([
    And(order[i] == 0, order[i+1] == yoshida_index)
    for i in range(5)
]))

# Base constraints are set. Now evaluate the multiple-choice options.
# We need to map the options to constraints on the order list

# Option A: Kammer's audition is second (index 1)
opt_A = (order[1] == 0)

# Option B: Trillo's audition is fourth (index 3)
opt_B = (order[3] == 2)

# Option C: Waite's audition is third (index 2)
opt_C = (order[2] == 3)

# Option D: Yoshida's audition is sixth (index 5)
opt_D = (order[5] == 4)

# Option E: Zinn's audition is second (index 1)
opt_E = (order[1] == 5)

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