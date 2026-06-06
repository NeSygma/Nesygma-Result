from z3 import *

# Variables for positions 1..6
K = Int('K')  # Kammer (recorded)
L = Int('L')  # Lugo (recorded)
T = Int('T')  # Trillo
W = Int('W')  # Waite
Y = Int('Y')  # Yoshida
Z = Int('Z')  # Zinn
vars = [K, L, T, W, Y, Z]

base = Solver()
# domain constraints
for v in vars:
    base.add(v >= 1, v <= 6)
# all distinct
base.add(Distinct(vars))
# Fourth audition cannot be recorded (K or L)
base.add(K != 4, L != 4)
# Fifth audition must be recorded (K or L)
base.add(Or(K == 5, L == 5))
# Kammer earlier than Trillo
base.add(K < T)
# Zinn earlier than Yoshida
base.add(Z < Y)
# original condition: Waite earlier than both recorded
original_cond = And(W < K, W < L)

# Option constraints
opt_constraints = {}
# A: Z is the only one that can be earlier than Waite
opt_A = And(Z < W,
            K > W,
            L > W,
            T > W,
            Y > W)
opt_constraints['A'] = opt_A
# B: Waite immediately before or after Zinn
opt_B = Or(W == Z + 1, W == Z - 1)
opt_constraints['B'] = opt_B
# C: Waite earlier than Lugo
opt_C = W < L
opt_constraints['C'] = opt_C
# D: Waite either first or second
opt_D = Or(W == 1, W == 2)
opt_constraints['D'] = opt_D
# E: First audition cannot be recorded
opt_E = And(K != 1, L != 1)
opt_constraints['E'] = opt_E

found_options = []
for letter, opt in opt_constraints.items():
    # Check if opt is equivalent to original_cond under base constraints
    # (base + opt) => original_cond
    s1 = Solver()
    s1.add(base.assertions())
    s1.add(opt)
    s1.add(Not(original_cond))
    imp1 = s1.check()
    # (base + original_cond) => opt
    s2 = Solver()
    s2.add(base.assertions())
    s2.add(original_cond)
    s2.add(Not(opt))
    imp2 = s2.check()
    if imp1 == unsat and imp2 == unsat:
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