from z3 import *

# Riders: Reynaldo, Seamus, Theresa, Yuki
# Bikes: F, G, H, J
# Days: 1 (first), 2 (second)

# We'll use integer variables for each rider-day pair, representing which bike they test.
# Bike encoding: F=0, G=1, H=2, J=3
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bikes = ["F", "G", "H", "J"]

# Create variables: assign[r][d] = bike index (0-3)
assign = [[Int(f"assign_{riders[r]}_day{d+1}") for d in range(2)] for r in range(4)]

solver = Solver()

# Domain constraints: each assignment is one of the 4 bikes
for r in range(4):
    for d in range(2):
        solver.add(assign[r][d] >= 0, assign[r][d] <= 3)

# Each day, all four bikes are tested (distinct per day)
for d in range(2):
    solver.add(Distinct([assign[r][d] for r in range(4)]))

# Each rider tests a different bike on day 2 than day 1
for r in range(4):
    solver.add(assign[r][0] != assign[r][1])

# Condition 1: Reynaldo cannot test F (bike 0)
solver.add(assign[0][0] != 0)
solver.add(assign[0][1] != 0)

# Condition 2: Yuki cannot test J (bike 3)
solver.add(assign[3][0] != 3)
solver.add(assign[3][1] != 3)

# Condition 3: Theresa must be one of the testers for H (bike 2)
# Theresa is index 2. She must test H on at least one of the two days.
solver.add(Or(assign[2][0] == 2, assign[2][1] == 2))

# Condition 4: The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# Yuki is index 3, Seamus is index 1.
solver.add(assign[3][0] == assign[1][1])

# Additional condition from the question: Theresa tests G on the second day.
# G is bike 1. Theresa is index 2.
solver.add(assign[2][1] == 1)

# Now evaluate each option
# Option A: Reynaldo tests H on the first day. Reynaldo=0, H=2, day1=0
opt_a = (assign[0][0] == 2)

# Option B: Reynaldo tests J on the first day. Reynaldo=0, J=3, day1=0
opt_b = (assign[0][0] == 3)

# Option C: Theresa tests H on the second day. Theresa=2, H=2, day2=1
opt_c = (assign[2][1] == 2)

# Option D: Theresa tests J on the first day. Theresa=2, J=3, day1=0
opt_d = (assign[2][0] == 3)

# Option E: Yuki tests H on the second day. Yuki=3, H=2, day2=1
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