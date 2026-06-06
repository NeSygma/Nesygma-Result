from z3 import *

# Map candidates to integers
J, K, L, N, O = 0, 1, 2, 3, 4

solver = Solver()
# Decision variables for each country
V = Int('V')  # Venezuela
Y = Int('Y')  # Yemen
Z = Int('Z')  # Zambia

# Domain constraints
solver.add(And(V >= 0, V <= 4))
solver.add(And(Y >= 0, Y <= 4))
solver.add(And(Z >= 0, Z <= 4))
# Distinctness (no ambassador assigned to more than one country)
solver.add(Distinct(V, Y, Z))

# Helper booleans for assignments
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned
solver.add(K_assigned != N_assigned)  # xor
solver.add(Or(K_assigned, N_assigned))  # at least one of them

# Constraint 2: If J assigned then K assigned
solver.add(Implies(J_assigned, K_assigned))

# Constraint 3: If O assigned to Venezuela then K not assigned to Yemen
solver.add(Implies(V == O, Y != K))

# Constraint 4: If L assigned, it is to Zambia (i.e., L cannot be in V or Y)
solver.add(V != L)
solver.add(Y != L)
# (Z can be L or not, no extra constraint needed)

# Define option constraints
opt_a = And(V == J, Y == O, Z == N)
opt_b = And(V == K, Y == J, Z == L)
opt_c = And(V == L, Y == N, Z == O)
opt_d = And(V == N, Y == J, Z == K)
opt_e = And(V == O, Y == K, Z == L)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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