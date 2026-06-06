from z3 import *

# Create solver
solver = Solver()

# Declare variables for each client's targets
# Image
img_website = Int('img_website')
img_voicemail = Int('img_voicemail')
# Solide
sol_website = Int('sol_website')
sol_voicemail = Int('sol_voicemail')
# Truvest
tru_website = Int('tru_website')
tru_voicemail = Int('tru_voicemail')

# Domain constraints: targets can be 1, 2, or 3 days
solver.add(Or([img_website == 1, img_website == 2, img_website == 3]))
solver.add(Or([img_voicemail == 1, img_voicemail == 2, img_voicemail == 3]))
solver.add(Or([sol_website == 1, sol_website == 2, sol_website == 3]))
solver.add(Or([sol_voicemail == 1, sol_voicemail == 2, sol_voicemail == 3]))
solver.add(Or([tru_website == 1, tru_website == 2, tru_website == 3]))
solver.add(Or([tru_voicemail == 1, tru_voicemail == 2, tru_voicemail == 3]))

# Constraint 1: For each client, website target ≤ voicemail target
solver.add(img_website <= img_voicemail)
solver.add(sol_website <= sol_voicemail)
solver.add(tru_website <= tru_voicemail)

# Constraint 2: Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(img_voicemail < sol_voicemail)
solver.add(img_voicemail < tru_voicemail)

# Constraint 3: Solide's website target must be shorter than Truvest's website target
solver.add(sol_website < tru_website)

# Additional constraint: None of the clients has a website target of 2 days
solver.add(img_website != 2)
solver.add(sol_website != 2)
solver.add(tru_website != 2)

# Define the answer choices as constraints
opt_a_constr = (img_website < sol_website)  # Image's website target is shorter than Solide's
opt_b_constr = (sol_website < img_website)  # Solide's website target is shorter than Image's
opt_c_constr = (sol_voicemail < tru_voicemail)  # Solide's voicemail target is shorter than Truvest's
opt_d_constr = (tru_website < img_website)  # Truvest's website target is shorter than Image's
opt_e_constr = (tru_voicemail < sol_voicemail)  # Truvest's voicemail target is shorter than Solide's

# Test each option using the exact skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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