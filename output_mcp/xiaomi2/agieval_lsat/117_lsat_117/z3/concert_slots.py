from z3 import *

solver = Solver()

# Bands: Uneasy(U), Vegemite(V), Wellspring(W), Xpert(X), Yardsign(Y), Zircon(Z)
# Each band assigned to a slot 1-6, all different
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Each band in exactly one slot (1-6)
for b in bands:
    solver.add(And(b >= 1, b <= 6))

# All bands in different slots
solver.add(Distinct(bands))

# Constraint 1: Vegemite performs in an earlier slot than Zircon
solver.add(V < Z)

# Constraint 2: Wellspring performs in an earlier slot than Xpert
solver.add(W < X)

# Constraint 3: Zircon performs in an earlier slot than Xpert
solver.add(Z < X)

# Constraint 4: Uneasy performs in one of the last three slots (4, 5, 6)
solver.add(And(U >= 4, U <= 6))

# Constraint 5: Yardsign performs in one of the first three slots (1, 2, 3)
solver.add(And(Y >= 1, Y <= 3))

# Additional constraint from question: Zircon performs in an earlier slot than Yardsign
solver.add(Z < Y)

# Question: What is the earliest slot in which Wellspring could perform?
# Check each option: can W be in that slot (or earlier)?
# Option A: W <= 2, Option B: W <= 3, Option C: W <= 4, Option D: W <= 5, Option E: W <= 6

found_options = []
for letter, constr in [("A", W <= 2), ("B", W <= 3), ("C", W <= 4), ("D", W <= 5), ("E", W <= 6)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The question asks for the EARLIEST slot Wellspring could perform.
# We want the smallest slot number that is achievable.
# If W<=2 is SAT, earliest is 2 (A). If only W<=3 is SAT, earliest is 3 (B), etc.
# But we need the MINIMUM possible W value. Let's find it directly.

opt = Optimize()
# Copy all base constraints
opt.add(Distinct(bands))
for b in bands:
    opt.add(And(b >= 1, b <= 6))
opt.add(V < Z)
opt.add(W < X)
opt.add(Z < X)
opt.add(And(U >= 4, U <= 6))
opt.add(And(Y >= 1, Y <= 3))
opt.add(Z < Y)

opt.minimize(W)
opt_result = opt.check()

if opt_result == sat:
    m = opt.model()
    min_w = m[W]
    print(f"Minimum W slot = {min_w}")
    print(f"All values: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")

# Now determine which single option is the earliest
# The earliest slot is the minimum value of W
# Map min_w to answer letter
if opt_result == sat:
    min_w_val = int(str(m[W]))
    answer_map = {2: "A", 3: "B", 4: "C", 5: "D", 6: "E"}
    if min_w_val in answer_map:
        print("STATUS: sat")
        print(f"answer:{answer_map[min_w_val]}")
    else:
        print("STATUS: unsat")
        print(f"Refine: min_w={min_w_val} not in options")
else:
    print("STATUS: unsat")
    print("Refine: Could not find minimum")