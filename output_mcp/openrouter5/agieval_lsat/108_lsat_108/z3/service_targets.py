from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: 1 day, 2 days, 3 days (1 = shortest, 3 = longest)
# For each client: website target (W) and voicemail target (V)

# Variables: IW, IV, SW, SV, TW, TV
# Domain: {1, 2, 3} where 1=1day, 2=2days, 3=3days

IW, IV, SW, SV, TW, TV = Ints('IW IV SW SV TW TV')

solver = Solver()

# Domain constraints
for var in [IW, IV, SW, SV, TW, TV]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# i.e., website <= voicemail for each client
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# i.e., IV < SV and IV < TV
solver.add(IV < SV)
solver.add(IV < TV)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# i.e., SW < TW
solver.add(SW < TW)

# Additional condition from the question: None of the clients has a website target of 2 days.
# So each website target is either 1 or 3.
solver.add(IW != 2)
solver.add(SW != 2)
solver.add(TW != 2)

# Now evaluate each option

# Option A: Image's website target is shorter than Solide's. (IW < SW)
opt_a = (IW < SW)

# Option B: Solide's website target is shorter than Image's. (SW < IW)
opt_b = (SW < IW)

# Option C: Solide's voicemail target is shorter than Truvest's. (SV < TV)
opt_c = (SV < TV)

# Option D: Truvest's website target is shorter than Image's. (TW < IW)
opt_d = (TW < IW)

# Option E: Truvest's voicemail target is shorter than Solide's. (TV < SV)
opt_e = (TV < SV)

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