from z3 import *

# Countries: Venezuela, Yemen, Zambia
# We'll assign each country an ambassador (one of the 5 candidates)
# Candidates: Jaramillo(0), Kayne(1), Landon(2), Novetzke(3), Ong(4)

# We'll use Int variables for each country, with domain 0..4
V = Int('Venezuela')
Y = Int('Yemen')
Z = Int('Zambia')

solver = Solver()

# Domain: each is one of the 5 candidates
solver.add(V >= 0, V <= 4)
solver.add(Y >= 0, Y <= 4)
solver.add(Z >= 0, Z <= 4)

# All different (one ambassador per country, no repeats)
solver.add(Distinct(V, Y, Z))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned to one of the ambassadorships.
solver.add(Or(
    And(Or(V == 1, Y == 1, Z == 1), Not(Or(V == 3, Y == 3, Z == 3))),
    And(Or(V == 3, Y == 3, Z == 3), Not(Or(V == 1, Y == 1, Z == 1)))
))

# Constraint 2: If Jaramillo(0) is assigned to one of the ambassadorships, then so is Kayne(1).
solver.add(Implies(Or(V == 0, Y == 0, Z == 0), Or(V == 1, Y == 1, Z == 1)))

# Constraint 3: If Ong(4) is assigned as ambassador to Venezuela, Kayne(1) is not assigned as ambassador to Yemen.
solver.add(Implies(V == 4, Y != 1))

# Constraint 4: If Landon(2) is assigned to an ambassadorship, it is to Zambia.
solver.add(Implies(Or(V == 2, Y == 2, Z == 2), Z == 2))

# Additional condition from the question: Ong is assigned as ambassador to Venezuela
solver.add(V == 4)

# Now evaluate each option
# Each option gives the OTHER TWO ambassadors (the ones not assigned to Venezuela)
# So we need to check if the pair can be assigned to Yemen and Zambia (in some order)

# Option A: Jaramillo(0) and Landon(2)
opt_a = And(
    Or(Y == 0, Z == 0),  # Jaramillo is one of the other two
    Or(Y == 2, Z == 2),  # Landon is one of the other two
    Y != Z               # They are different
)

# Option B: Jaramillo(0) and Novetzke(3)
opt_b = And(
    Or(Y == 0, Z == 0),
    Or(Y == 3, Z == 3),
    Y != Z
)

# Option C: Kayne(1) and Landon(2)
opt_c = And(
    Or(Y == 1, Z == 1),
    Or(Y == 2, Z == 2),
    Y != Z
)

# Option D: Kayne(1) and Novetzke(3)
opt_d = And(
    Or(Y == 1, Z == 1),
    Or(Y == 3, Z == 3),
    Y != Z
)

# Option E: Landon(2) and Novetzke(3)
opt_e = And(
    Or(Y == 2, Z == 2),
    Or(Y == 3, Z == 3),
    Y != Z
)

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