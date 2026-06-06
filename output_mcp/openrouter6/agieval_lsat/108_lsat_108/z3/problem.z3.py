from z3 import *

solver = Solver()

# Declare variables
W_image, W_solide, W_truvest = Ints('W_image W_solide W_truvest')
V_image, V_solide, V_truvest = Ints('V_image V_solide V_truvest')

# Base constraints
# 1. Website target <= Voicemail target for each client
solver.add(W_image <= V_image)
solver.add(W_solide <= V_solide)
solver.add(W_truvest <= V_truvest)

# 2. Image's voicemail target is shorter than the others
solver.add(V_image < V_solide)
solver.add(V_image < V_truvest)

# 3. Solide's website target is shorter than Truvest's
solver.add(W_solide < W_truvest)

# 4. Website targets are not 2 days (so they are 1 or 3)
solver.add(Or(W_image == 1, W_image == 3))
solver.add(Or(W_solide == 1, W_solide == 3))
solver.add(Or(W_truvest == 1, W_truvest == 3))

# 5. Voicemail targets are in {1,2,3}
solver.add(V_image >= 1, V_image <= 3)
solver.add(V_solide >= 1, V_solide <= 3)
solver.add(V_truvest >= 1, V_truvest <= 3)

# Define options
opt_a = (W_image < W_solide)
opt_b = (W_solide < W_image)
opt_c = (V_solide < V_truvest)
opt_d = (W_truvest < W_image)
opt_e = (V_truvest < V_solide)

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