from z3 import *

solver = Solver()

# Variables: website and voicemail targets for each client
# Domain: {1,2,3} (days)
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

# Domain constraints
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: No client has website target longer than voicemail target
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail target shorter than other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website target shorter than Truvest's website target
solver.add(S_w < T_w)

# Additional condition: No client has a voicemail target of 3 days
solver.add(I_v != 3)
solver.add(S_v != 3)
solver.add(T_v != 3)

# Now test each option's negation to see which is NOT necessarily true
# (If adding NOT(option) is SAT, then the option can be false, i.e., not forced)

found_options = []

# Option A: Image's website target is 1 day
opt_a = (I_w == 1)
# Option B: Solide's website target is 2 days
opt_b = (S_w == 2)
# Option C: Solide's voicemail target is 2 days
opt_c = (S_v == 2)
# Option D: Truvest's website target is 2 days
opt_d = (T_w == 2)
# Option E: Truvest's voicemail target is 2 days
opt_e = (T_v == 2)

for letter, constr in [("A", Not(opt_a)),
                       ("B", Not(opt_b)),
                       ("C", Not(opt_c)),
                       ("D", Not(opt_d)),
                       ("E", Not(opt_e))]:
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