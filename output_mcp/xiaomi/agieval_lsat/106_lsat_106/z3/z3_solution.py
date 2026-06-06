from z3 import *

solver = Solver()

# Define variables for each client's website and voicemail targets
# Values: 1, 2, or 3 days
I_w = Int('Image_website')      # Image's website target
I_v = Int('Image_voicemail')    # Image's voicemail target
S_w = Int('Solide_website')     # Solide's website target
S_v = Int('Solide_voicemail')   # Solide's voicemail target
T_w = Int('Truvest_website')    # Truvest's website target
T_v = Int('Truvest_voicemail')  # Truvest's voicemail target

# All targets are 1, 2, or 3 days
for v in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(v == 1, v == 2, v == 3))

# Condition 1: None of the clients can have a website target longer than its voicemail target
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target
solver.add(S_w < T_w)

# Additional condition from the question: Solide's voicemail target is shorter than Truvest's website target
solver.add(S_v < T_w)

# Now test each option to see which target COULD be 2 days
# "Could be" means there exists a valid assignment where that target equals 2

found_options = []

# Option A: Image's website target could be 2
opt_a = (I_w == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Image's voicemail target could be 2
opt_b = (I_v == 2)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's website target could be 2
opt_c = (S_w == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's voicemail target could be 2
opt_d = (T_v == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's website target could be 2
opt_e = (T_w == 2)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Found valid options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")