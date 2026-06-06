from z3 import *

# Companies
RealProp, Southco, Trustcorp = 0, 1, 2
companies = [RealProp, Southco, Trustcorp]

# Buildings and their classes
buildings = [
    ("Garza Tower", 1),
    ("Yates House", 3),
    ("Zimmer House", 3),
    ("Flores Tower", 1),
    ("Lynch Building", 2),
    ("King Building", 2),
    ("Meyer Building", 2),
    ("Ortiz Building", 2)
]
num_buildings = len(buildings)
classes = [b[1] for b in buildings]

# Initial ownership: building index -> company
initial_owner = [0, 0, 0, 1, 1, 2, 2, 2]  # based on the list above

# Define final ownership variables: O[b][c] = True if building b is owned by company c
O = [[Bool(f"O_{b}_{c}") for c in companies] for b in range(num_buildings)]

# Base constraints: each building owned by exactly one company
solver = Solver()
for b in range(num_buildings):
    solver.add(Sum([If(O[b][c], 1, 0) for c in companies]) == 1)

# Now, define the trade variables: x2_AB, x3_AB for each ordered pair (A,B)
# We have 3 companies, so 3*2 = 6 ordered pairs (A != B)
x2 = {}
x3 = {}
for A in companies:
    for B in companies:
        if A != B:
            x2[(A,B)] = Int(f"x2_{A}_{B}")
            x3[(A,B)] = Int(f"x3_{A}_{B}")
            solver.add(x2[(A,B)] >= 0)
            solver.add(x3[(A,B)] >= 0)

# Now, compute the final count of each class for each company
# f[c][k] where k is class index: 0 for class 1, 1 for class 2, 2 for class 3
f = [[Int(f"f_{c}_{k}") for k in range(3)] for c in companies]
for c in companies:
    for k in range(3):
        class_val = k + 1  # because classes are 1,2,3
        # f[c][k] = sum over buildings b of class class_val of O[b][c]
        solver.add(f[c][k] == Sum([If(And(O[b][c], classes[b] == class_val), 1, 0) for b in range(num_buildings)]))

# Initial counts i[c][k]
i = [[0 for k in range(3)] for c in companies]
for b in range(num_buildings):
    c_init = initial_owner[b]
    k = classes[b] - 1  # convert class to index 0,1,2
    i[c_init][k] += 1

# Delta: change in count for each company and class
delta = {}
for c in companies:
    for k in range(3):
        delta[(c,k)] = Int(f"delta_{c}_{k}")
        solver.add(delta[(c,k)] == f[c][k] - i[c][k])

# Constraints from trades:
# For each company A, the delta must be expressible as linear combination of x2 and x3
# Let's define the equations for each company
for A in companies:
    # Get the other companies
    others = [B for B in companies if B != A]
    B, C = others[0], others[1]
    
    # Equation for delta[A][0] (class 1)
    # delta[A][0] = -x2[A,B] - x2[A,C] + x2[B,A] + x2[C,A]
    solver.add(delta[(A,0)] == -x2[(A,B)] - x2[(A,C)] + x2[(B,A)] + x2[(C,A)])
    
    # Equation for delta[A][1] (class 2)
    # delta[A][1] = 2*x2[A,B] + 2*x2[A,C] - x2[B,A] - x2[C,A] - x3[A,B] - x3[A,C] + x3[B,A] + x3[C,A]
    solver.add(delta[(A,1)] == 2*x2[(A,B)] + 2*x2[(A,C)] - x2[(B,A)] - x2[(C,A)] - x3[(A,B)] - x3[(A,C)] + x3[(B,A)] + x3[(C,A)])
    
    # Equation for delta[A][2] (class 3)
    # delta[A][2] = 2*x3[A,B] + 2*x3[A,C] - x3[B,A] - x3[C,A]
    solver.add(delta[(A,2)] == 2*x3[(A,B)] + 2*x3[(A,C)] - x3[(B,A)] - x3[(C,A)])

# Now, we have the base solver with constraints that define reachable states.
# Now, we need to evaluate each option.

# Option A: RealProp owns Lynch (4), Meyer (6), Ortiz (7)
# So for RealProp (company 0), O[4][0] = True, O[6][0] = True, O[7][0] = True
# The other buildings can be owned by any company, but we don't care as long as constraints hold.

# Option B: Southco owns Garza Tower (0) and Meyer Building (6)
# So for Southco (company 1), O[0][1] = True, O[6][1] = True

# Option C: Southco owns King Building (5), Meyer Building (6), Ortiz Building (7)
# So for Southco (company 1), O[5][1] = True, O[6][1] = True, O[7][1] = True

# Option D: Trustcorp owns Flores Tower (3) and Yates House (1)
# So for Trustcorp (company 2), O[3][2] = True, O[1][2] = True

# Option E: Trustcorp owns Garza Tower (0) and Lynch Building (4)
# So for Trustcorp (company 2), O[0][2] = True, O[4][2] = True

# Now, we'll test each option using the skeleton
found_options = []

# Option A
solver.push()
solver.add(O[4][0] == True)
solver.add(O[6][0] == True)
solver.add(O[7][0] == True)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B
solver.push()
solver.add(O[0][1] == True)
solver.add(O[6][1] == True)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C
solver.push()
solver.add(O[5][1] == True)
solver.add(O[6][1] == True)
solver.add(O[7][1] == True)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D
solver.push()
solver.add(O[3][2] == True)
solver.add(O[1][2] == True)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E
solver.push()
solver.add(O[0][2] == True)
solver.add(O[4][2] == True)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Now, based on found_options, print the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")