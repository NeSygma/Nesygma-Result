from z3 import *

# Countries: 0: Venezuela, 1: Yemen, 2: Zambia
# Candidates: 1: Jaramillo, 2: Kayne, 3: Landon, 4: Novetzke, 5: Ong
# 0: None (not used here as we have 3 countries and 5 candidates)

amb = [Int(f'amb_{i}') for i in range(3)]
# Candidates are 1-5
for i in range(3):
    solver = Solver()
    solver.add(amb[i] >= 1, amb[i] <= 5)
solver.add(Distinct(amb))

# Helper to check if a candidate is assigned
def is_assigned(c):
    return Or([amb[i] == c for i in range(3)])

# Constraint 2: Either Kayne or Novetzke, but not both, is assigned
solver.add(Xor(is_assigned(2), is_assigned(4)))

# Constraint 3: If Jaramillo is assigned, then so is Kayne
solver.add(Implies(is_assigned(1), is_assigned(2)))

# Constraint 4: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(amb[0] == 5, amb[1] != 2))

# Constraint 5: If Landon is assigned to an ambassadorship, it is to Zambia
solver.add(Implies(is_assigned(3), amb[2] == 3))

# Test options
options = [
    ("A", [1, 5, 4]), # V:J, Y:O, Z:N
    ("B", [2, 1, 3]), # V:K, Y:J, Z:L
    ("C", [3, 4, 5]), # V:L, Y:N, Z:O
    ("D", [4, 1, 2]), # V:N, Y:J, Z:K
    ("E", [5, 2, 3])  # V:O, Y:K, Z:L
]

found_options = []
for letter, assignment in options:
    solver.push()
    solver.add(amb[0] == assignment[0], amb[1] == assignment[1], amb[2] == assignment[2])
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