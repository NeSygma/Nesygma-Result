from z3 import *

# Riders: Reynaldo, Seamus, Theresa, Yuki
# Bikes: F, G, H, J
# Days: 1, 2

# We'll use integer variables for each rider-day pair, representing which bike they test.
# Let's encode bikes as integers 0=F, 1=G, 2=H, 3=J
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bikes = ["F", "G", "H", "J"]

# Create variables: assign[rider][day] = bike (int 0..3)
assign = [[Int(f"assign_{r}_{d}") for d in range(2)] for r in range(4)]

solver = Solver()

# Domain: each assignment is a bike 0..3
for r in range(4):
    for d in range(2):
        solver.add(assign[r][d] >= 0, assign[r][d] <= 3)

# Each day, all four bikes are tested (each rider gets a different bike)
for d in range(2):
    solver.add(Distinct([assign[r][d] for r in range(4)]))

# Each rider tests a different bike on day 2 than on day 1
for r in range(4):
    solver.add(assign[r][0] != assign[r][1])

# Conditions:
# 1. Reynaldo cannot test F (bike 0).
solver.add(assign[0][0] != 0)
solver.add(assign[0][1] != 0)

# 2. Yuki cannot test J (bike 3).
solver.add(assign[3][0] != 3)
solver.add(assign[3][1] != 3)

# 3. Theresa must be one of the testers for H (bike 2).
# That means Theresa tests H on at least one of the two days.
solver.add(Or(assign[2][0] == 2, assign[2][1] == 2))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# Yuki's day1 bike = Seamus's day2 bike
solver.add(assign[3][0] == assign[1][1])

# Additional condition from the question: Theresa tests J on the first day.
# J is bike 3.
solver.add(assign[2][0] == 3)

# Now evaluate each option
# Option A: Reynaldo tests G on the second day. G is bike 1.
opt_a = (assign[0][1] == 1)

# Option B: Seamus tests H on the first day. H is bike 2.
opt_b = (assign[1][0] == 2)

# Option C: Yuki tests H on the second day. H is bike 2.
opt_c = (assign[3][1] == 2)

# Option D: Seamus is one of the testers for J. J is bike 3.
opt_d = Or(assign[1][0] == 3, assign[1][1] == 3)

# Option E: Theresa is one of the testers for G. G is bike 1.
opt_e = Or(assign[2][0] == 1, assign[2][1] == 1)

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