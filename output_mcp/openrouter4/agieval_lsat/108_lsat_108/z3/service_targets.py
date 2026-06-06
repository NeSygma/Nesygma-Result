from z3 import *

solver = Solver()

# Variables: website (W) and voicemail (V) targets for each client
# Domain: 1 day, 2 days, 3 days
I_W, I_V = Ints('I_W I_V')
S_W, S_V = Ints('S_W S_V')
T_W, T_V = Ints('T_W T_V')

# Domain constraints
for var in [I_W, I_V, S_W, S_V, T_W, T_V]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
solver.add(I_W <= I_V)
solver.add(S_W <= S_V)
solver.add(T_W <= T_V)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
solver.add(I_V < S_V)
solver.add(I_V < T_V)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
solver.add(S_W < T_W)

# Condition from the question: None of the clients has a website target of 2 days.
solver.add(I_W != 2)
solver.add(S_W != 2)
solver.add(T_W != 2)

# Now check each option
found_options = []

# Option A: Image's website target is shorter than Solide's. (I_W < S_W)
opt_a = (I_W < S_W)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Solide's website target is shorter than Image's. (S_W < I_W)
opt_b = (S_W < I_W)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's voicemail target is shorter than Truvest's. (S_V < T_V)
opt_c = (S_V < T_V)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's website target is shorter than Image's. (T_W < I_W)
opt_d = (T_W < I_W)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's voicemail target is shorter than Solide's. (T_V < S_V)
opt_e = (T_V < S_V)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
    
    # Also print a model for the correct option to verify
    solver.push()
    if found_options[0] == "A":
        solver.add(opt_a)
    elif found_options[0] == "B":
        solver.add(opt_b)
    elif found_options[0] == "C":
        solver.add(opt_c)
    elif found_options[0] == "D":
        solver.add(opt_d)
    elif found_options[0] == "E":
        solver.add(opt_e)
    solver.check()
    m = solver.model()
    print(f"Model: I_W={m[I_W]}, I_V={m[I_V]}, S_W={m[S_W]}, S_V={m[S_V]}, T_W={m[T_W]}, T_V={m[T_V]}")
    solver.pop()
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")