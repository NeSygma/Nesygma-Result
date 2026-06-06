from z3 import *

solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Three kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# For each kind, we have 3 batches (batch 1, 2, 3)
# We'll encode the day each batch is made as an integer 0..4

# Variables: O[i], P[i], S[i] for i=0,1,2 (batch indices 0=first, 1=second, 2=third)
O = [Int(f"O_{i}") for i in range(3)]
P = [Int(f"P_{i}") for i in range(3)]
S = [Int(f"S_{i}") for i in range(3)]

all_batches = O + P + S

# Domain: each batch is made on Monday through Friday (0..4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Exactly three batches of each kind, each batch on a single day (already encoded)

# No two batches of the same kind are made on the same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))

# At least one batch of cookies is made on Monday
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
solver.add(O[1] == P[0])

# The second batch of sugar cookies is made on Thursday (day index 3)
solver.add(S[1] == 3)

# Additional condition from the question: The first batch of peanut butter cookies is made on Tuesday (day index 1)
solver.add(P[0] == 1)

# Now evaluate each option

# Option A: Two different kinds of cookie have their first batch made on Monday.
# That means at least two of {O[0], P[0], S[0]} equal 0 (Monday)
opt_a = Sum([If(O[0] == 0, 1, 0), If(P[0] == 0, 1, 0), If(S[0] == 0, 1, 0)]) >= 2

# Option B: Two different kinds of cookie have their first batch made on Tuesday.
opt_b = Sum([If(O[0] == 1, 1, 0), If(P[0] == 1, 1, 0), If(S[0] == 1, 1, 0)]) >= 2

# Option C: Two different kinds of cookie have their second batch made on Wednesday.
opt_c = Sum([If(O[1] == 2, 1, 0), If(P[1] == 2, 1, 0), If(S[1] == 2, 1, 0)]) >= 2

# Option D: Two different kinds of cookie have their second batch made on Thursday.
opt_d = Sum([If(O[1] == 3, 1, 0), If(P[1] == 3, 1, 0), If(S[1] == 3, 1, 0)]) >= 2

# Option E: Two different kinds of cookie have their third batch made on Friday.
opt_e = Sum([If(O[2] == 4, 1, 0), If(P[2] == 4, 1, 0), If(S[2] == 4, 1, 0)]) >= 2

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