from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: 1 day, 2 days, or 3 days
# For each client: website target and voicemail target

# Variables: I_w, I_v, S_w, S_v, T_w, T_v
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

solver = Solver()

# Domain: each target is 1, 2, or 3 days
all_vars = [I_w, I_v, S_w, S_v, T_w, T_v]
for v in all_vars:
    solver.add(Or(v == 1, v == 2, v == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# So for each client: website <= voicemail
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# I_v < S_v and I_v < T_v
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# S_w < T_w
solver.add(S_w < T_w)

# Given: Image's website target is 2 days
solver.add(I_w == 2)

# Now evaluate each option: which target must also be 2 days?
# We test each option by adding the constraint that the option's target is NOT 2 days.
# If the system becomes unsat, then that option MUST be 2 days.

found_options = []

# Option A: Image's voicemail target is 2 days
solver.push()
solver.add(I_v != 2)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Solide's website target is 2 days
solver.push()
solver.add(S_w != 2)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Solide's voicemail target is 2 days
solver.push()
solver.add(S_v != 2)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's website target is 2 days
solver.push()
solver.add(T_w != 2)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's voicemail target is 2 days
solver.push()
solver.add(T_v != 2)
if solver.check() == unsat:
    found_options.append("E")
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