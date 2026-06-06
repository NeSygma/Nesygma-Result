from z3 import *

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Day 1: d1[b] = rider testing bicycle b on day 1
# Day 2: d2[b] = rider testing bicycle b on day 2

solver = Solver()

# Create variables for day 1 and day 2 assignments (bicycle -> rider)
d1 = [Int(f'd1_{b}') for b in range(4)]  # d1[b] = rider on bicycle b, day 1
d2 = [Int(f'd2_{b}') for b in range(4)]  # d2[b] = rider on bicycle b, day 2

# Each rider tests exactly one bicycle per day (all-different per day)
solver.add(Distinct(d1))
solver.add(Distinct(d2))

# Each rider tests a different bicycle on day 2 than day 1
# For each rider, the bicycle they test on day 1 != bicycle on day 2
for r in range(4):
    # Find which bicycle rider r tests on day 1 and day 2
    # rider r tests bicycle b1 on day 1 and bicycle b2 on day 2, b1 != b2
    b1 = Int(f'b1_{r}')
    b2 = Int(f'b2_{r}')
    # b1 is the bicycle tested by rider r on day 1
    solver.add(Or([And(d1[b] == r, b1 == b) for b in range(4)]))
    # b2 is the bicycle tested by rider r on day 2
    solver.add(Or([And(d2[b] == r, b2 == b) for b in range(4)]))
    solver.add(b1 != b2)

# Domain constraints
for b in range(4):
    solver.add(d1[b] >= 0, d1[b] <= 3)
    solver.add(d2[b] >= 0, d2[b] <= 3)

# Condition 1: Reynaldo (0) cannot test F (0)
solver.add(d1[0] != 0)
solver.add(d2[0] != 0)

# Condition 2: Yuki (3) cannot test J (3)
solver.add(d1[3] != 3)
solver.add(d2[3] != 3)

# Condition 3: Theresa (2) must be one of the testers for H (2)
solver.add(Or(d1[2] == 2, d2[2] == 2))

# Condition 4: The bicycle that Yuki tests on day 1 must be tested by Seamus on day 2
# Find which bicycle Yuki tests on day 1
yuki_d1_bike = Int('yuki_d1_bike')
solver.add(Or([And(d1[b] == 3, yuki_d1_bike == b) for b in range(4)]))
# That bicycle must be tested by Seamus (1) on day 2
solver.add(Or([And(yuki_d1_bike == b, d2[b] == 1) for b in range(4)]))

# Now encode each answer choice as constraints
# Format: F: rider1, rider2; G: rider1, rider2; H: rider1, rider2; J: rider1, rider2
# rider1 = day 1, rider2 = day 2

# (A) F: Seamus(1), Reynaldo(0); G: Yuki(3), Seamus(1); H: Theresa(2), Yuki(3); J: Reynaldo(0), Theresa(2)
opt_a = And(
    d1[0] == 1, d2[0] == 0,  # F
    d1[1] == 3, d2[1] == 1,  # G
    d1[2] == 2, d2[2] == 3,  # H
    d1[3] == 0, d2[3] == 2   # J
)

# (B) F: Seamus(1), Yuki(3); G: Reynaldo(0), Theresa(2); H: Yuki(3), Seamus(1); J: Theresa(2), Reynaldo(0)
opt_b = And(
    d1[0] == 1, d2[0] == 3,  # F
    d1[1] == 0, d2[1] == 2,  # G
    d1[2] == 3, d2[2] == 1,  # H
    d1[3] == 2, d2[3] == 0   # J
)

# (C) F: Yuki(3), Seamus(1); G: Seamus(1), Reynaldo(0); H: Theresa(2), Yuki(3); J: Reynaldo(0), Theresa(2)
opt_c = And(
    d1[0] == 3, d2[0] == 1,  # F
    d1[1] == 1, d2[1] == 0,  # G
    d1[2] == 2, d2[2] == 3,  # H
    d1[3] == 0, d2[3] == 2   # J
)

# (D) F: Yuki(3), Seamus(1); G: Theresa(2), Reynaldo(0); H: Reynaldo(0), Theresa(2); J: Seamus(1), Yuki(3)
opt_d = And(
    d1[0] == 3, d2[0] == 1,  # F
    d1[1] == 2, d2[1] == 0,  # G
    d1[2] == 0, d2[2] == 2,  # H
    d1[3] == 1, d2[3] == 3   # J
)

# (E) F: Yuki(3), Theresa(2); G: Seamus(1), Yuki(3); H: Theresa(2), Reynaldo(0); J: Reynaldo(0), Seamus(1)
opt_e = And(
    d1[0] == 3, d2[0] == 2,  # F
    d1[1] == 1, d2[1] == 3,  # G
    d1[2] == 2, d2[2] == 0,  # H
    d1[3] == 0, d2[3] == 1   # J
)

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