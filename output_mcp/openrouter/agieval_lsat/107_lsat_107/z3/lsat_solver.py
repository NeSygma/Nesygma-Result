from z3 import *

solver = Solver()
# Declare variables for website (W) and voicemail (V) targets for each client
W_Image = Int('W_Image')
V_Image = Int('V_Image')
W_Solide = Int('W_Solide')
V_Solide = Int('V_Solide')
W_Truvest = Int('W_Truvest')
V_Truvest = Int('V_Truvest')

vars = [W_Image, V_Image, W_Solide, V_Solide, W_Truvest, V_Truvest]
# Domain constraints: each target is 1, 2, or 3 days
for v in vars:
    solver.add(v >= 1, v <= 3)

# 1. Website target cannot be longer than voicemail target for each client
solver.add(W_Image <= V_Image)
solver.add(W_Solide <= V_Solide)
solver.add(W_Truvest <= V_Truvest)

# 2. Image's voicemail target is shorter than the other clients' voicemail targets
solver.add(V_Image < V_Solide)
solver.add(V_Image < V_Truvest)

# 3. Solide's website target is shorter than Truvest's website target
solver.add(W_Solide < W_Truvest)

# Define option constraints: each checks if at least two clients share the specified target
opt_a_constr = Sum([If(W_Image == 1, 1, 0), If(W_Solide == 1, 1, 0), If(W_Truvest == 1, 1, 0)]) >= 2  # 1-day website
opt_b_constr = Sum([If(V_Image == 2, 1, 0), If(V_Solide == 2, 1, 0), If(V_Truvest == 2, 1, 0)]) >= 2  # 2-day voicemail
opt_c_constr = Sum([If(W_Image == 2, 1, 0), If(W_Solide == 2, 1, 0), If(W_Truvest == 2, 1, 0)]) >= 2  # 2-day website
opt_d_constr = Sum([If(V_Image == 3, 1, 0), If(V_Solide == 3, 1, 0), If(V_Truvest == 3, 1, 0)]) >= 2  # 3-day voicemail
opt_e_constr = Sum([If(W_Image == 3, 1, 0), If(W_Solide == 3, 1, 0), If(W_Truvest == 3, 1, 0)]) >= 2  # 3-day website

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The correct answer is the option that CANNOT be set for more than one client,
# i.e., the option NOT in found_options.
all_options = {"A", "B", "C", "D", "E"}
missing = all_options - set(found_options)
if len(missing) == 1:
    ans = missing.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
elif len(missing) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be duplicated {missing}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be duplicated, unexpected")