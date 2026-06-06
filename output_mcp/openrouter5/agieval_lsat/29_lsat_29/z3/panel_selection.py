from z3 import *

# Scientists: botanists (F, G, H), chemists (K, L, M), zoologists (P, Q, R)
# We'll use Bool variables: True means selected, False means not selected.

F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# The panel must include at least one scientist of each of the three types.
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# If more than one botanist is selected, then at most one zoologist is selected.
# "more than one botanist" means at least 2 botanists selected.
# "at most one zoologist" means number of zoologists <= 1.
# We encode: (num_botanists >= 2) => (num_zoologists <= 1)
num_botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
num_zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(num_botanists >= 2, num_zoologists <= 1))

# F and K cannot both be selected.
solver.add(Not(And(F, K)))

# K and M cannot both be selected.
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected.
solver.add(Implies(M, And(P, R)))

# Additional condition from the question: both G and H are among the scientists selected.
solver.add(And(G, H))

# Now we need to determine which of the options must be true (i.e., is entailed by the premises).
# The question: "If both G and H are among the scientists selected, then the panel must include either ..."
# So we need to find which option is NECESSARILY true (entailed).
# We'll test each option: is it forced by the constraints?
# An option like "F or else K" means: the panel must include either F or K (or both).
# So we check if NOT(F or K) is inconsistent with the premises.
# If NOT(option) is unsat, then the option is forced (must be true).

found_options = []

# Option A: F or else K  (i.e., F or K)
opt_a = Or(F, K)
# Option B: F or else M  (i.e., F or M)
opt_b = Or(F, M)
# Option C: K or else M  (i.e., K or M)
opt_c = Or(K, M)
# Option D: M or else Q  (i.e., M or Q)
opt_d = Or(M, Q)
# Option E: P or else Q  (i.e., P or Q)
opt_e = Or(P, Q)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # To check if the option is forced, we add the negation of the option.
    # If the negation is unsat, then the option must be true.
    solver.add(Not(constr))
    if solver.check() == unsat:
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