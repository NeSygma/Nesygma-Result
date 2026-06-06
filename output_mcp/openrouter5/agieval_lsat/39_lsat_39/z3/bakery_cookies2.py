from z3 import *

solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

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

# From P[0] == 1 and O[1] == P[0], we get O[1] == 1 (Tuesday)
# So O[1] == 1

# Let's check what the model looks like
result = solver.check()
if result == sat:
    m = solver.model()
    print("Model found:")
    for i in range(3):
        print(f"O_{i} = {m[O[i]]}, P_{i} = {m[P[i]]}, S_{i} = {m[S[i]]}")
else:
    print("No model")

# Now evaluate each option more carefully.
# The question asks: "each of the following could be true EXCEPT"
# So we need to find which option CANNOT be true (is impossible/unsat)
# while the others CAN be true (are sat).

# Let's test each option individually with a fresh solver context

def test_option(constr, desc):
    s = Solver()
    # Add all base constraints
    for b in all_batches:
        s.add(b >= 0, b <= 4)
    s.add(Distinct(O))
    s.add(Distinct(P))
    s.add(Distinct(S))
    s.add(Or([b == 0 for b in all_batches]))
    s.add(O[1] == P[0])
    s.add(S[1] == 3)
    s.add(P[0] == 1)
    s.add(constr)
    res = s.check()
    if res == sat:
        m = s.model()
        print(f"{desc}: SAT")
        for i in range(3):
            print(f"  O_{i} = {m[O[i]]}, P_{i} = {m[P[i]]}, S_{i} = {m[S[i]]}")
        return True
    else:
        print(f"{desc}: UNSAT")
        return False

# Option A: Two different kinds of cookie have their first batch made on Monday.
opt_a = Sum([If(O[0] == 0, 1, 0), If(P[0] == 0, 1, 0), If(S[0] == 0, 1, 0)]) >= 2

# Option B: Two different kinds of cookie have their first batch made on Tuesday.
opt_b = Sum([If(O[0] == 1, 1, 0), If(P[0] == 1, 1, 0), If(S[0] == 1, 1, 0)]) >= 2

# Option C: Two different kinds of cookie have their second batch made on Wednesday.
opt_c = Sum([If(O[1] == 2, 1, 0), If(P[1] == 2, 1, 0), If(S[1] == 2, 1, 0)]) >= 2

# Option D: Two different kinds of cookie have their second batch made on Thursday.
opt_d = Sum([If(O[1] == 3, 1, 0), If(P[1] == 3, 1, 0), If(S[1] == 3, 1, 0)]) >= 2

# Option E: Two different kinds of cookie have their third batch made on Friday.
opt_e = Sum([If(O[2] == 4, 1, 0), If(P[2] == 4, 1, 0), If(S[2] == 4, 1, 0)]) >= 2

print("\n--- Testing each option ---")
test_a = test_option(opt_a, "A")
test_b = test_option(opt_b, "B")
test_c = test_option(opt_c, "C")
test_d = test_option(opt_d, "D")
test_e = test_option(opt_e, "E")

# The answer is the one that is UNSAT (cannot be true)
results = {"A": test_a, "B": test_b, "C": test_c, "D": test_d, "E": test_e}
unsat_options = [k for k, v in results.items() if not v]
sat_options = [k for k, v in results.items() if v]

print(f"\nSAT options: {sat_options}")
print(f"UNSAT options: {unsat_options}")

if len(unsat_options) == 1:
    print(f"STATUS: sat")
    print(f"answer:{unsat_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Unexpected results")