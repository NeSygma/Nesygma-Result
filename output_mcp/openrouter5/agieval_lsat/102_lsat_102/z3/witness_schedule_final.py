from z3 import *

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
# Days: Monday=0, Tuesday=1, Wednesday=2

solver = Solver()

F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]

for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Franco != Garcia
solver.add(F != G)

# Iturbe on Wednesday
solver.add(I == 2)

# Exactly two on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong not on Monday
solver.add(H != 0)

# At least one on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Franco same day as Hong
solver.add(F == H)

# Now evaluate each option using the required skeleton
# Option A: Franco on Wednesday (F == 2)
opt_a = (F == 2)

# Option B: Garcia on Monday (G == 0)
opt_b = (G == 0)

# Option C: Garcia on Wednesday (G == 2)
opt_c = (G == 2)

# Option D: Hong on Tuesday (H == 1)
opt_d = (H == 1)

# Option E: Iturbe is the only witness on Wednesday
# I == 2 and all others != 2
opt_e = And(I == 2, F != 2, G != 2, H != 2, J != 2)

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