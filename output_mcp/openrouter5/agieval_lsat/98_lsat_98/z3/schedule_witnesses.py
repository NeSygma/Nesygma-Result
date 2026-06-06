from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: Monday (0), Tuesday (1), Wednesday (2)

# We'll use Int variables for each witness, representing the day they testify
F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

solver = Solver()

# Domain: each witness testifies on Monday(0), Tuesday(1), or Wednesday(2)
for w in witnesses:
    solver.add(w >= 0, w <= 2)

# 1. Franco does not testify on the same day that Garcia testifies.
solver.add(F != G)

# 2. Iturbe testifies on Wednesday.
solver.add(I == 2)

# 3. Exactly two witnesses testify on Tuesday.
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# 4. Hong does not testify on Monday.
solver.add(H != 0)

# 5. At least one witness testifies on Monday.
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Now define each option as a set of constraints

# Option A: Monday: Franco, Tuesday: Hong and Iturbe, Wednesday: Garcia and Jackson
opt_a = And(F == 0, H == 1, I == 1, G == 2, J == 2)

# Option B: Monday: Franco and Hong, Tuesday: Iturbe and Jackson, Wednesday: Garcia
opt_b = And(F == 0, H == 0, I == 1, J == 1, G == 2)

# Option C: Monday: Garcia, Tuesday: Franco and Iturbe, Wednesday: Hong and Jackson
opt_c = And(G == 0, F == 1, I == 1, H == 2, J == 2)

# Option D: Monday: Garcia and Jackson, Tuesday: Franco and Hong, Wednesday: Iturbe
opt_d = And(G == 0, J == 0, F == 1, H == 1, I == 2)

# Option E: Monday: Garcia and Jackson, Tuesday: Hong, Wednesday: Franco and Iturbe
opt_e = And(G == 0, J == 0, H == 1, F == 2, I == 2)

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