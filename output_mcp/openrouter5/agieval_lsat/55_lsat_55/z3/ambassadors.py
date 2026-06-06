from z3 import *

# Candidates: Jaramillo, Kayne, Landon, Novetzke, Ong
# Countries: Venezuela, Yemen, Zambia
# We need to assign exactly 3 ambassadors to 3 countries, leaving 2 unassigned.

# Let's model: for each candidate, which country they are assigned to (or 0 for unassigned)
# Use Int variables with domain 0..3 where 0=unassigned, 1=Venezuela, 2=Yemen, 3=Zambia

J, K, L, N, O = Ints('J K L N O')

solver = Solver()

# Domain: each candidate gets a value 0,1,2,3
for v in [J, K, L, N, O]:
    solver.add(And(v >= 0, v <= 3))

# Exactly 3 candidates are assigned (value != 0), and 2 are unassigned (value == 0)
# Count assigned: sum of If(v != 0, 1, 0) == 3
solver.add(Sum([If(v != 0, 1, 0) for v in [J, K, L, N, O]]) == 3)

# Each country gets exactly one ambassador (Distinct among non-zero assignments)
# We need: for each country c (1,2,3), exactly one candidate has that value.
# Equivalent: the multiset of non-zero values is exactly {1,2,3}
# So the non-zero values must be a permutation of 1,2,3.
# We can enforce: Distinct among all values, but 0 can appear multiple times.
# Better: use cardinality constraints.
for c in [1, 2, 3]:
    solver.add(Sum([If(v == c, 1, 0) for v in [J, K, L, N, O]]) == 1)

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
# "assigned" means value != 0
solver.add(Or(K != 0, N != 0))  # at least one assigned
solver.add(Not(And(K != 0, N != 0)))  # not both assigned

# Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
solver.add(Implies(J != 0, K != 0))

# Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen.
# Venezuela = 1, Yemen = 2
solver.add(Implies(O == 1, K != 2))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia.
# Zambia = 3
solver.add(Implies(L != 0, L == 3))

# Now evaluate each option: which pair of candidates are NOT assigned (value == 0)?
# Option A: Jaramillo and Novetzke are the two unassigned
opt_a = And(J == 0, N == 0)
# Option B: Jaramillo and Ong
opt_b = And(J == 0, O == 0)
# Option C: Kayne and Landon
opt_c = And(K == 0, L == 0)
# Option D: Kayne and Novetzke
opt_d = And(K == 0, N == 0)
# Option E: Landon and Ong
opt_e = And(L == 0, O == 0)

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