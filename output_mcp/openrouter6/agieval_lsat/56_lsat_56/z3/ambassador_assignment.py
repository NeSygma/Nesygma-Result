from z3 import *

# Constants for ambassadors
J, K, L, N, O = 0, 1, 2, 3, 4

# Variables for assignments to countries
V = Int('V')  # Venezuela
Y = Int('Y')  # Yemen
Z = Int('Z')  # Zambia

solver = Solver()

# Domain constraints: each variable must be one of the ambassadors
solver.add(V >= 0, V <= 4)
solver.add(Y >= 0, Y <= 4)
solver.add(Z >= 0, Z <= 4)

# Each ambassador assigned at most once (all distinct)
solver.add(Distinct(V, Y, Z))

# Helper expressions for assignments
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)
L_assigned = Or(V == L, Y == L, Z == L)

# Constraint 1: Exactly one of Kayne or Novetzke is assigned
solver.add(Or(K_assigned, N_assigned))
solver.add(Not(And(K_assigned, N_assigned)))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(J_assigned, K_assigned))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(V == O, Y != K))

# Constraint 4: If Landon is assigned, it is to Zambia
solver.add(Implies(L_assigned, Z == L))

# Now evaluate each multiple choice option
found_options = []

# Option A: Jaramillo and Landon
opt_a = Or(And(Y == J, Z == L), And(Y == L, Z == J))
solver.push()
solver.add(V == O)
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Jaramillo and Novetzke
opt_b = Or(And(Y == J, Z == N), And(Y == N, Z == J))
solver.push()
solver.add(V == O)
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Kayne and Landon
opt_c = Or(And(Y == K, Z == L), And(Y == L, Z == K))
solver.push()
solver.add(V == O)
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Kayne and Novetzke
opt_d = Or(And(Y == K, Z == N), And(Y == N, Z == K))
solver.push()
solver.add(V == O)
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Landon and Novetzke
opt_e = Or(And(Y == L, Z == N), And(Y == N, Z == L))
solver.push()
solver.add(V == O)
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")