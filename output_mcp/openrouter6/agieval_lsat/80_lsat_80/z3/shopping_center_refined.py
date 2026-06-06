from z3 import *

solver = Solver()

# Declare variables
O = Int('O')
P = Int('P')
R1 = Int('R1')
R2 = Int('R2')
S = Int('S')
T = Int('T')
V = Int('V')

# Shoe store is in space 4
solver.add(S == 4)

# All positions between 1 and 7
solver.add(1 <= O, O <= 7)
solver.add(1 <= P, P <= 7)
solver.add(1 <= R1, R1 <= 7)
solver.add(1 <= R2, R2 <= 7)
solver.add(1 <= S, S <= 7)
solver.add(1 <= T, T <= 7)
solver.add(1 <= V, V <= 7)

# All distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Constraint 1: Pharmacy at one end, restaurant at the other
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: Toy store not next to veterinarian
solver.add(Not(Or(
    Abs(T - V) == 1
)))

# Define option constraints (the statements themselves)
opt_a = Or(Abs(O - R1) == 1, Abs(O - R2) == 1)  # optometrist next to a restaurant
opt_b = Abs(P - V) == 1  # pharmacy next to veterinarian
opt_c = Or(Abs(R1 - T) == 1, Abs(R2 - T) == 1)  # restaurant next to toy store
opt_d = Abs(S - T) == 1  # shoe store next to toy store (S=4)
opt_e = Abs(S - V) == 1  # shoe store next to veterinarian (S=4)

# For each option, check if its negation is unsat (i.e., option must be true)
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    solver.pop()
    if result == unsat:
        must_be_true.append(letter)

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")