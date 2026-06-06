from z3 import *

# Define variables for positions 1..6
pos_K = Int('pos_K')  # Kammer
pos_L = Int('pos_L')  # Lugo
pos_T = Int('pos_T')  # Trillo
pos_W = Int('pos_W')  # Waite
pos_Y = Int('pos_Y')  # Yoshida
pos_Z = Int('pos_Z')  # Zinn
positions = [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]

base = Solver()
# domain constraints
for p in positions:
    base.add(p >= 1, p <= 6)
# all distinct
base.add(Distinct(positions))
# Recorded: K and L are recorded
# Fourth audition cannot be recorded
base.add(pos_K != 4, pos_L != 4)
# Fifth audition must be recorded
base.add(Or(pos_K == 5, pos_L == 5))
# Kammer earlier than Trillo
base.add(pos_K < pos_T)
# Zinn earlier than Yoshida
base.add(pos_Z < pos_Y)
# Original Waite condition (to be used in implication checks)
orig_waite = And(pos_W < pos_K, pos_W < pos_L)

# Define option constraints
opt_A = And(pos_Z < pos_W,
            pos_W < pos_K,
            pos_W < pos_L,
            pos_W < pos_T,
            pos_W < pos_Y)
opt_B = Or(pos_W == pos_Z + 1, pos_Z == pos_W + 1)
opt_C = pos_W < pos_L
opt_D = Or(pos_W == 1, pos_W == 2)
opt_E = And(pos_K != 1, pos_L != 1)

options = [
    ("A", opt_A),
    ("B", opt_B),
    ("C", opt_C),
    ("D", opt_D),
    ("E", opt_E)
]

found_options = []
for letter, opt in options:
    # Check original => option (orig & not opt unsat?)
    s1 = Solver()
    s1.add(base.assertions())
    s1.add(orig_waite)
    s1.add(Not(opt))
    res1 = s1.check()
    # Check option => original (opt & not orig unsat?)
    s2 = Solver()
    s2.add(base.assertions())
    s2.add(opt)
    s2.add(Not(orig_waite))
    res2 = s2.check()
    if res1 == unsat and res2 == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")