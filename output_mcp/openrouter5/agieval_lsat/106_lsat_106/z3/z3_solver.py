from z3 import *

# We have 3 clients: Image (I), Solide (S), Truvest (T)
# For each client, two targets: website (w) and voicemail (v)
# Targets are 1, 2, or 3 days (1 = shortest, 3 = longest)
# Actually: 1 day, 2 days, 3 days. Let's use 1, 2, 3.

I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

solver = Solver()

# Domain: each target is 1, 2, or 3 days
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# i.e., website <= voicemail for each client
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

# Additional condition from the question: Solide's voicemail target is shorter than Truvest's website target.
# S_v < T_w
solver.add(S_v < T_w)

# Now evaluate each option: which target COULD be 2 days?
# We test each option by adding the constraint that the specific target equals 2.

found_options = []

# Option A: Image's website target = 2 days
opt_a = (I_w == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Image's voicemail target = 2 days
opt_b = (I_v == 2)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's website target = 2 days
opt_c = (S_w == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's voicemail target = 2 days
opt_d = (T_v == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's website target = 2 days
opt_e = (T_w == 2)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
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