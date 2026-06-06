from z3 import *

solver = Solver()

# Define variables for each client's website and voicemail targets
# Clients: Image, Solide, Truvest
# Targets: 1, 2, or 3 days

I_w = Int('Image_website')
I_v = Int('Image_voicemail')
S_w = Int('Solide_website')
S_v = Int('Solide_voicemail')
T_w = Int('Truvest_website')
T_v = Int('Truvest_voicemail')

# All targets must be 1, 2, or 3 days
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target
solver.add(S_w < T_w)

# Given: Image's website target is 2 days
solver.add(I_w == 2)

# Now check each option to see which MUST be 2 days
# We check if each option is FORCED to be 2 by the constraints

found_options = []

# Option A: Image's voicemail target must be 2
opt_a_constr = (I_v == 2)
# Option B: Solide's website target must be 2
opt_b_constr = (S_w == 2)
# Option C: Solide's voicemail target must be 2
opt_c_constr = (S_v == 2)
# Option D: Truvest's website target must be 2
opt_d_constr = (T_w == 2)
# Option E: Truvest's voicemail target must be 2
opt_e_constr = (T_v == 2)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Check if the negation is unsatisfiable (meaning the option MUST be true)
    solver.add(Not(constr))
    if solver.check() == unsat:
        # The negation is unsat, so the option must be true
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