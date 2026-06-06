from z3 import *

solver = Solver()

# Define variables
pianist = [Int(f'pianist_{i}') for i in range(5)]
type_ = [Int(f'type_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(pianist[i] >= 0, pianist[i] <= 1)
    solver.add(type_[i] >= 0, type_[i] <= 1)

# Condition 1: Third solo is traditional
solver.add(type_[2] == 1)

# Condition 2: Exactly two traditional pieces total, and they are consecutive
total_trad = Sum(type_)
solver.add(total_trad == 2)
solver.add(Or([And(type_[i] == 1, type_[i+1] == 1) for i in range(4)]))

# Condition 3: Fourth solo constraint
solver.add(Or(
    And(pianist[3] == 0, type_[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, type_[3] == 0)   # Zara performs modern
))

# Condition 4: Second solo pianist ≠ fifth solo pianist
solver.add(pianist[1] != pianist[4])

# Condition 5: Wayne cannot perform a traditional piece until he has performed a modern piece
for i in range(5):
    # If Wayne performs traditional at i, then there must be a prior Wayne modern
    prior_wayne_modern = Or([And(pianist[j] == 0, type_[j] == 0) for j in range(i)])
    solver.add(Implies(And(pianist[i] == 0, type_[i] == 1), prior_wayne_modern))

# Extra condition for the question: pianist of first solo = pianist of second solo
solver.add(pianist[0] == pianist[1])

# Define options
opt_a_constr = (pianist[0] == 1)  # Zara performs first solo
opt_b_constr = (pianist[2] == 0)  # Wayne performs third solo
opt_c_constr = (pianist[4] == 1)  # Zara performs fifth solo
opt_d_constr = (type_[1] == 1)    # Second solo is traditional
opt_e_constr = (type_[3] == 0)    # Fourth solo is modern

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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