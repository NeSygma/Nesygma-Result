from z3 import *

solver = Solver()

# Declare variables
I_W = Int('I_W')
I_V = Int('I_V')
S_W = Int('S_W')
S_V = Int('S_V')
T_W = Int('T_W')
T_V = Int('T_V')

# Domain constraints: each target is 1, 2, or 3
solver.add(I_W >= 1, I_W <= 3)
solver.add(I_V >= 1, I_V <= 3)
solver.add(S_W >= 1, S_W <= 3)
solver.add(S_V >= 1, S_V <= 3)
solver.add(T_W >= 1, T_W <= 3)
solver.add(T_V >= 1, T_V <= 3)

# Condition 1: website target <= voicemail target for each client
solver.add(I_W <= I_V)
solver.add(S_W <= S_V)
solver.add(T_W <= T_V)

# Condition 2: Image's voicemail target is shorter than the others
solver.add(I_V < S_V)
solver.add(I_V < T_V)

# Condition 3: Solide's website target is shorter than Truvest's website target
solver.add(S_W < T_W)

# Additional condition: Truvest's website target is shorter than its voicemail target
solver.add(T_W < T_V)

# Now evaluate each answer choice
found_options = []

# Option A: Image's voicemail target is 2 days
opt_a = (I_V == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Image's website target is 2 days
opt_b = (I_W == 2)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Image's website target is 1 day
opt_c = (I_W == 1)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Solide's website target is 2 days
opt_d = (S_W == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Solide's website target is 1 day
opt_e = (S_W == 1)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")