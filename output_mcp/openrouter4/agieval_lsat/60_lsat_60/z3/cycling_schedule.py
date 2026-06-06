from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bikes: 0=F, 1=G, 2=H, 3=J

# rider_day1[b] = rider who tests bike b on day 1
# rider_day2[b] = rider who tests bike b on day 2
rider_day1 = [Int(f"rider_day1_{b}") for b in range(4)]
rider_day2 = [Int(f"rider_day2_{b}") for b in range(4)]

# Domain: each rider-day assignment is a rider index (0-3)
for b in range(4):
    solver.add(rider_day1[b] >= 0, rider_day1[b] <= 3)
    solver.add(rider_day2[b] >= 0, rider_day2[b] <= 3)

# Each rider appears exactly once on day 1 (each bike has different rider on day 1)
solver.add(Distinct(rider_day1))

# Each rider appears exactly once on day 2 (each bike has different rider on day 2)
solver.add(Distinct(rider_day2))

# Each rider tests a different bike on day 2 than day 1
# For each rider r, the day1 bike and day2 bike are different
# Bike b1 is r's day1 bike iff rider_day1[b1] == r
# Bike b2 is r's day2 bike iff rider_day2[b2] == r
# We need b1 != b2 for each rider r
# Equivalent to: for each rider r, the two bikes they ride are different
# Since each rider appears exactly once each day, we can use:
# For each pair of bikes (b1, b2), if the same rider rides both, then b1 != b2
# More directly: rider_day1 and rider_day2 are permutations, and for each rider,
# the index where they appear in rider_day1 differs from where they appear in rider_day2
for r in range(4):
    # r's day1 bike index and day2 bike index must differ
    day1_bikes = [rider_day1[b] for b in range(4)]
    day2_bikes = [rider_day2[b] for b in range(4)]
    # b is the day1 bike of r iff rider_day1[b] == r
    # Using Or-Exists pattern: There exist b1 != b2 such that rider_day1[b1]==r and rider_day2[b2]==r
    # Actually, simpler: since each rider appears exactly once in each day,
    # we can just say: for each rider r, if rider_day1[b1]==r and rider_day2[b2]==r, then b1 != b2
    # This is already enforced if we ensure that no bike has the same rider on both days.
    pass

# Simpler approach: each bike must have two DIFFERENT riders on day 1 and day 2
# (since each rider tests a different bike each day, but also each bike is tested by different riders each day? No, that's not necessarily a constraint. A bike could be tested by the same rider both days... wait no, each rider tests a DIFFERENT one of the bicycles on the second day. So each rider takes a different bike on day 2. But a bike could have different riders each day - that's fine.)

# Actually, let me re-read: "Each rider will then test a different one of the bicycles on the second day."
# So each rider tests a different bicycle on day 2 (not the same bike as day 1).
# This means for each rider r, if they test bike b1 on day 1 and bike b2 on day 2, then b1 != b2.

# Since each rider appears exactly once in rider_day1 and exactly once in rider_day2,
# we can use: For each bike b, the rider on day 1 must be different from the rider on day 2?
# No, that's not the constraint. The constraint is about riders, not bikes.

# Let me think again. If rider r tests bike b1 on day 1 and bike b2 on day 2, then b1 != b2.
# This means r appears in rider_day1 at position b1 and in rider_day2 at position b2, and b1 != b2.

# For each rider r, let b1 be the bike s.t. rider_day1[b1]==r, and b2 be the bike s.t. rider_day2[b2]==r.
# Then we need b1 != b2.

# Since Distinct(rider_day1) and Distinct(rider_day2), each rider appears exactly once in each.
# So for each rider r:
# The bike index where rider_day1[b] == r (call it b1) and the bike index where rider_day2[b] == r (call it b2) must satisfy b1 != b2.

# I can encode this as:
for r in range(4):
    # Find b1 such that rider_day1[b1] == r
    # Find b2 such that rider_day2[b2] == r
    # b1 != b2
    # Since these are indices (0-3), I can use Implies pattern
    # For any pair (b1, b2) where b1 == b2, we cannot have rider_day1[b1]==r AND rider_day2[b2]==r
    for b in range(4):
        solver.add(Not(And(rider_day1[b] == r, rider_day2[b] == r)))

# Constraints:
# 1. Reynaldo (0) cannot test F (0)
solver.add(rider_day1[0] != 0)
solver.add(rider_day2[0] != 0)

# 2. Yuki (3) cannot test J (3)
solver.add(rider_day1[3] != 3)
solver.add(rider_day2[3] != 3)

# 3. Theresa (2) must be one of the testers for H (2)
solver.add(Or(rider_day1[2] == 2, rider_day2[2] == 2))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# There exists a bicycle b such that rider_day1[b] == 3 (Yuki) AND rider_day2[b] == 1 (Seamus)
solver.add(Or([And(rider_day1[b] == 3, rider_day2[b] == 1) for b in range(4)]))

# Now encode each answer choice and test
# Option A:
# F(0): Seamus(1), Reynaldo(0) => rider_day1[0]=1, rider_day2[0]=0
# G(1): Yuki(3), Seamus(1) => rider_day1[1]=3, rider_day2[1]=1
# H(2): Theresa(2), Yuki(3) => rider_day1[2]=2, rider_day2[2]=3
# J(3): Reynaldo(0), Theresa(2) => rider_day1[3]=0, rider_day2[3]=2
opt_a_constr = And(
    rider_day1[0] == 1, rider_day2[0] == 0,
    rider_day1[1] == 3, rider_day2[1] == 1,
    rider_day1[2] == 2, rider_day2[2] == 3,
    rider_day1[3] == 0, rider_day2[3] == 2
)

# Option B:
# F(0): Seamus(1), Yuki(3) => rider_day1[0]=1, rider_day2[0]=3
# G(1): Reynaldo(0), Theresa(2) => rider_day1[1]=0, rider_day2[1]=2
# H(2): Yuki(3), Seamus(1) => rider_day1[2]=3, rider_day2[2]=1
# J(3): Theresa(2), Reynaldo(0) => rider_day1[3]=2, rider_day2[3]=0
opt_b_constr = And(
    rider_day1[0] == 1, rider_day2[0] == 3,
    rider_day1[1] == 0, rider_day2[1] == 2,
    rider_day1[2] == 3, rider_day2[2] == 1,
    rider_day1[3] == 2, rider_day2[3] == 0
)

# Option C:
# F(0): Yuki(3), Seamus(1) => rider_day1[0]=3, rider_day2[0]=1
# G(1): Seamus(1), Reynaldo(0) => rider_day1[1]=1, rider_day2[1]=0
# H(2): Theresa(2), Yuki(3) => rider_day1[2]=2, rider_day2[2]=3
# J(3): Reynaldo(0), Theresa(2) => rider_day1[3]=0, rider_day2[3]=2
opt_c_constr = And(
    rider_day1[0] == 3, rider_day2[0] == 1,
    rider_day1[1] == 1, rider_day2[1] == 0,
    rider_day1[2] == 2, rider_day2[2] == 3,
    rider_day1[3] == 0, rider_day2[3] == 2
)

# Option D:
# F(0): Yuki(3), Seamus(1) => rider_day1[0]=3, rider_day2[0]=1
# G(1): Theresa(2), Reynaldo(0) => rider_day1[1]=2, rider_day2[1]=0
# H(2): Reynaldo(0), Theresa(2) => rider_day1[2]=0, rider_day2[2]=2
# J(3): Seamus(1), Yuki(3) => rider_day1[3]=1, rider_day2[3]=3
opt_d_constr = And(
    rider_day1[0] == 3, rider_day2[0] == 1,
    rider_day1[1] == 2, rider_day2[1] == 0,
    rider_day1[2] == 0, rider_day2[2] == 2,
    rider_day1[3] == 1, rider_day2[3] == 3
)

# Option E:
# F(0): Yuki(3), Theresa(2) => rider_day1[0]=3, rider_day2[0]=2
# G(1): Seamus(1), Yuki(3) => rider_day1[1]=1, rider_day2[1]=3
# H(2): Theresa(2), Reynaldo(0) => rider_day1[2]=2, rider_day2[2]=0
# J(3): Reynaldo(0), Seamus(1) => rider_day1[3]=0, rider_day2[3]=1
opt_e_constr = And(
    rider_day1[0] == 3, rider_day2[0] == 2,
    rider_day1[1] == 1, rider_day2[1] == 3,
    rider_day1[2] == 2, rider_day2[2] == 0,
    rider_day1[3] == 0, rider_day2[3] == 1
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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