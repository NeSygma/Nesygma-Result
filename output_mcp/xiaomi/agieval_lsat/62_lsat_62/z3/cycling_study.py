from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bikes: 0=F, 1=G, 2=H, 3=J
# Variables: day1[r] = bike tested by rider r on day 1, day2[r] = bike tested by rider r on day 2

day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Each bike value is 0-3
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# All riders test different bikes on each day (all-different)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bike on day 2 vs day 1
for r in range(4):
    solver.add(day1[r] != day2[r])

# Constraint 1: Reynaldo (0) cannot test F (0) on either day
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Constraint 2: Yuki (3) cannot test J (3) on either day
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Constraint 3: Theresa (2) must test H (2) on at least one day
solver.add(Or(day1[2] == 2, day2[2] == 2))

# Constraint 4: Bike Yuki tests on Day 1 must be tested by Seamus on Day 2
solver.add(day2[1] == day1[3])

# Now test each option - we're looking for which CANNOT be true
# "Any of the following could be true EXCEPT" = find the impossible one

found_options = []

# Option A: Reynaldo tests J on the first day
opt_a = (day1[0] == 3)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Reynaldo tests J on the second day
opt_b = (day2[0] == 3)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Seamus tests H on the first day
opt_c = (day1[1] == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yuki tests H on the first day
opt_d = (day1[3] == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yuki tests H on the second day
opt_e = (day2[3] == 2)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Options that COULD be true: {found_options}")
print(f"Options that CANNOT be true: {[l for l in ['A','B','C','D','E'] if l not in found_options]}")

# The EXCEPT answer is the one NOT in found_options
impossible = [l for l in ['A','B','C','D','E'] if l not in found_options]

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: All options could be true - no EXCEPT found")