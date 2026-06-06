from z3 import *

# Candidate indices
J, K, L, N, O = 0, 1, 2, 3, 4

solver = Solver()

# Variables for each country: Venezuela, Yemen, Zambia
V = Int('V')
Y = Int('Y')
Z = Int('Z')

# Domain constraints
solver.add(And(V >= 0, V <= 4))
solver.add(And(Y >= 0, Y <= 4))
solver.add(And(Z >= 0, Z <= 4))
# All distinct (no ambassador assigned to more than one country)
solver.add(Distinct(V, Y, Z))

# Helper predicates for assignment presence
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)
L_assigned = Or(V == L, Y == L, Z == L)

# Constraint 1: Exactly one of Kayne or Novetzke is assigned (XOR)
solver.add(Or(And(K_assigned, Not(N_assigned)), And(N_assigned, Not(K_assigned))))
# Constraint 2: If J assigned then K assigned
solver.add(Implies(J_assigned, K_assigned))
# Constraint 3: If O assigned to Venezuela then K not assigned to Yemen
solver.add(V == O)  # O is assigned to Venezuela (given condition)
solver.add(Y != K)  # K not at Yemen
# Constraint 4: If L assigned then L is at Zambia
solver.add(Implies(L_assigned, Z == L))

# Options definitions: each as a constraint that Y and Z are exactly the two given candidates (order may vary)
options = {
    "A": (J, L),  # Jaramillo and Landon
    "B": (J, N),  # Jaramillo and Novetzke
    "C": (K, L),  # Kayne and Landon
    "D": (K, N),  # Kayne and Novetzke
    "E": (L, N)   # Landon and Novetzke
}

found_options = []
for letter, (c1, c2) in options.items():
    solver.push()
    # Y and Z must be exactly c1 and c2 in some order
    solver.add(Or(And(Y == c1, Z == c2), And(Y == c2, Z == c1)))
    # Also ensure that the third candidate (not O, c1, c2) is not assigned implicitly satisfied by distinctness
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