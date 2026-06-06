from z3 import *

# ----- Base model -----
# Candidates: Jaramillo (J), Kayne (K), Landon (L), Novetzke (N), Ong (O)
J, K, L, N, O = 0, 1, 2, 3, 4

# Countries: Venezuela (V), Yemen (Y), Zambia (Z)
V, Y, Z = Ints('V Y Z')
solver = Solver()

# Each country gets one distinct candidate (indices 0..4)
solver.add(And(V >= 0, V <= 4))
solver.add(And(Y >= 0, Y <= 4))
solver.add(And(Z >= 0, Z <= 4))
solver.add(Distinct(V, Y, Z))

# Helper predicates: whether a candidate is assigned somewhere
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)
L_assigned = Or(V == L, Y == L, Z == L)
O_assigned = Or(V == O, Y == O, Z == O)

# ----- Problem constraints -----
# 1. Exactly one of Kayne or Novetzke (but not both) is assigned.
solver.add(Xor(K_assigned, N_assigned))

# 2. If Jaramillo is assigned, then Kayne is also assigned.
solver.add(Implies(J_assigned, K_assigned))

# 3. If Ong is assigned to Venezuela, Kayne is not assigned to Yemen.
solver.add(Implies(V == O, Not(Y == K)))

# 4. If Landon is assigned, it must be to Zambia.
solver.add(Implies(L_assigned, Z == L))

# ----- Options to test (each option states a claim that could be true) -----
options = {
    "A": Z == J,               # Jaramillo is assigned to Zambia
    "B": Z == K,               # Kayne is assigned to Zambia
    "C": Z == N,               # Novetzke is assigned to Zambia
    "D": Not(L_assigned),      # Landon is not assigned to any ambassadorship
    "E": Not(O_assigned)       # Ong is not assigned to any ambassadorship
}

# ----- Evaluate each option using push/pop as required -----
found_options = []
for letter, opt_constr in [("A", options["A"]),
                           ("B", options["B"]),
                           ("C", options["C"]),
                           ("D", options["D"]),
                           ("E", options["E"])]:
    solver.push()
    solver.add(opt_constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# ----- Determine the unique impossible option -----
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")