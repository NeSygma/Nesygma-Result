from z3 import *

# Riders: Reynaldo (R), Seamus (S), Theresa (T), Yuki (Y)
# Bicycles: F, G, H, J
# Days: 1 (first day), 2 (second day)

# We'll model assignments as: rider_day[rider][day] = bicycle
# Use integers: 0=F, 1=G, 2=H, 3=J

riders = ["R", "S", "T", "Y"]
bikes = ["F", "G", "H", "J"]

# Create variables: assign[rider][day] where rider index 0=R,1=S,2=T,3=Y, day 0=day1, day1=day2
assign = [[Int(f"assign_{r}_{d}") for d in range(2)] for r in range(4)]

solver = Solver()

# Domain: each assignment is 0..3 (F,G,H,J)
for r in range(4):
    for d in range(2):
        solver.add(assign[r][d] >= 0, assign[r][d] <= 3)

# Each day, all four bicycles are tested (each day has a permutation)
for d in range(2):
    solver.add(Distinct([assign[r][d] for r in range(4)]))

# Each rider tests different bicycles on day 1 and day 2
for r in range(4):
    solver.add(assign[r][0] != assign[r][1])

# Condition 1: Reynaldo cannot test F (F=0)
solver.add(assign[0][0] != 0)  # Reynaldo day1 not F
solver.add(assign[0][1] != 0)  # Reynaldo day2 not F

# Condition 2: Yuki cannot test J (J=3)
solver.add(assign[3][0] != 3)  # Yuki day1 not J
solver.add(assign[3][1] != 3)  # Yuki day2 not J

# Condition 3: Theresa must be one of the testers for H (H=2)
# Theresa tests H on at least one of the two days
solver.add(Or(assign[2][0] == 2, assign[2][1] == 2))

# Condition 4: The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# Yuki's day1 bike = Seamus's day2 bike
solver.add(assign[3][0] == assign[1][1])

# Now evaluate each option

# Option A: Reynaldo tests J on the first day. J=3
opt_a = (assign[0][0] == 3)

# Option B: Reynaldo tests J on the second day. J=3
opt_b = (assign[0][1] == 3)

# Option C: Seamus tests H on the first day. H=2
opt_c = (assign[1][0] == 2)

# Option D: Yuki tests H on the first day. H=2
opt_d = (assign[3][0] == 2)

# Option E: Yuki tests H on the second day. H=2
opt_e = (assign[3][1] == 2)

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