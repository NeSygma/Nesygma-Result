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

# Condition 5: No traditional piece until Wayne performs at least one modern piece
solver.add(type_[0] == 0)
for i in range(1, 5):
    prior_modern_wayne = Or([And(pianist[j] == 0, type_[j] == 0) for j in range(i)])
    solver.add(Implies(type_[i] == 1, prior_modern_wayne))

# Extra condition for the question: pianist of first solo = pianist of second solo
solver.add(pianist[0] == pianist[1])

result = solver.check()
print(f"Base constraints satisfiable: {result}")
if result == sat:
    m = solver.model()
    print("Model:")
    for i in range(5):
        print(f"Solo {i+1}: Pianist {'Wayne' if m[pianist[i]] == 0 else 'Zara'}, Type {'Modern' if m[type_[i]] == 0 else 'Traditional'}")
else:
    print("Unsatisfiable - need to refine constraints")