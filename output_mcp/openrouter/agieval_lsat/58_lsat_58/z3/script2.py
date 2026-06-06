from z3 import *

# Base model
J, K, L, N, O = 0, 1, 2, 3, 4
V, Y, Z = Ints('V Y Z')
solver = Solver()
# Domain constraints
solver.add(And(V >= 0, V <= 4))
solver.add(And(Y >= 0, Y <= 4))
solver.add(And(Z >= 0, Z <= 4))
solver.add(Distinct(V, Y, Z))
# Helper predicates
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)
L_assigned = Or(V == L, Y == L, Z == L)
O_assigned = Or(V == O, Y == O, Z == O)
# Constraints
solver.add(Xor(K_assigned, N_assigned))
solver.add(Implies(J_assigned, K_assigned))
solver.add(Implies(V == O, Not(Y == K)))
solver.add(Implies(L_assigned, Z == L))
# Dummy contradiction
dummy = Bool('dummy')
# Options definitions (original claims)
options = {
    "A": Z == J,               # Jaramillo assigned to Zambia
    "B": Z == K,               # Kayne assigned to Zambia
    "C": Z == N,               # Novetzke assigned to Zambia
    "D": Not(L_assigned),      # Landon not assigned
    "E": Not(O_assigned)       # Ong not assigned
}
found_options = []
for letter, claim in [("A", options["A"]),
                     ("B", options["B"]),
                     ("C", options["C"]),
                     ("D", options["D"]),
                     ("E", options["E"])]:
    solver.push()
    # Add implication that forces contradiction if claim holds
    solver.add(Implies(claim, And(dummy, Not(dummy))))
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