from z3 import *

# Define the businesses
# P: Pharmacy, O: Optometrist, R1: Restaurant 1, R2: Restaurant 2, S: Shoe, T: Toy, V: Vet
# Spaces: 0 to 6 (representing 1 to 7)

def check_constraints(order):
    # order is a list of 7 integers (0-6) representing the position of each business
    # P, O, R1, R2, S, T, V
    # Let's map them:
    # 0: P, 1: O, 2: R1, 3: R2, 4: S, 5: T, 6: V
    
    # Constraint 1: Pharmacy at one end, one restaurant at the other
    # P is at 0 or 6. One of R1, R2 is at 6 or 0.
    c1 = Or(And(order[0] == 0, Or(order[2] == 6, order[3] == 6)),
            And(order[0] == 6, Or(order[2] == 0, order[3] == 0)))
    
    # Constraint 2: Two restaurants separated by at least two other businesses
    # |pos(R1) - pos(R2)| >= 3
    c2 = Abs(order[2] - order[3]) >= 3
    
    # Constraint 3: Pharmacy next to O or V
    # |pos(P) - pos(O)| = 1 OR |pos(P) - pos(V)| = 1
    c3 = Or(Abs(order[0] - order[1]) == 1, Abs(order[0] - order[6]) == 1)
    
    # Constraint 4: Toy store cannot be next to veterinarian
    # |pos(T) - pos(V)| != 1
    c4 = Abs(order[5] - order[6]) != 1
    
    return And(c1, c2, c3, c4)

# Check each option
# A: P, O, S, R, V, T, R
# B: P, V, O, S, R, T, R
# C: R, S, V, P, O, T, R
# D: R, T, O, R, V, S, P
# E: R, O, T, R, S, V, P

# Map businesses to indices in the order list:
# P:0, O:1, R1:2, R2:3, S:4, T:5, V:6
# A: P=0, O=1, S=2, R1=3, V=4, T=5, R2=6
# B: P=0, V=1, O=2, S=3, R1=4, T=5, R2=6
# C: R1=0, S=1, V=2, P=3, O=4, T=5, R2=6
# D: R1=0, T=1, O=2, R2=3, V=4, S=5, P=6
# E: R1=0, O=1, T=2, R2=3, S=4, V=5, P=6

options = {
    "A": [0, 1, 3, 6, 2, 5, 4],
    "B": [0, 2, 4, 6, 3, 5, 1],
    "C": [3, 4, 0, 6, 1, 5, 2],
    "D": [6, 2, 0, 3, 5, 1, 4],
    "E": [6, 1, 0, 3, 4, 2, 5]
}

solver = Solver()
for label, order in options.items():
    solver.push()
    # The order list here is [pos(P), pos(O), pos(R1), pos(R2), pos(S), pos(T), pos(V)]
    # We need to check if this specific assignment satisfies the constraints
    # The constraints are defined on the positions.
    # Let's redefine the check to take the positions directly.
    
    # Wait, the previous check_constraints function was for symbolic variables.
    # Let's just manually check the constraints for each option.
    
    # P=order[0], O=order[1], R1=order[2], R2=order[3], S=order[4], T=order[5], V=order[6]
    P, O, R1, R2, S, T, V = order
    
    c1 = (P == 0 and (R1 == 6 or R2 == 6)) or (P == 6 and (R1 == 0 or R2 == 0))
    c2 = abs(R1 - R2) >= 3
    c3 = (abs(P - O) == 1) or (abs(P - V) == 1)
    c4 = abs(T - V) != 1
    
    if c1 and c2 and c3 and c4:
        print(f"Option {label} is valid.")
    else:
        print(f"Option {label} is invalid.")
    solver.pop()