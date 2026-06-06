from z3 import *

# Riders: Reynaldo, Seamus, Theresa, Yuki
# Bicycles: F, G, H, J
# Days: 1 and 2

# We'll model assignments as: for each rider and each day, which bike they test.
# Use integer variables: 0=F, 1=G, 2=H, 3=J
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bikes = ["F", "G", "H", "J"]

# Create variables: assign[rider][day] = bike index (0..3)
assign = [[Int(f"assign_{r}_{d}") for d in range(2)] for r in range(4)]

solver = Solver()

# Domain: each assignment is a bike index 0..3
for r in range(4):
    for d in range(2):
        solver.add(assign[r][d] >= 0, assign[r][d] <= 3)

# Each day, all four bicycles are tested (each bike used exactly once per day)
for d in range(2):
    solver.add(Distinct([assign[r][d] for r in range(4)]))

# Each rider tests a different bicycle on day 1 and day 2
for r in range(4):
    solver.add(assign[r][0] != assign[r][1])

# Condition 1: Reynaldo cannot test F (bike index 0)
solver.add(assign[0][0] != 0)
solver.add(assign[0][1] != 0)

# Condition 2: Yuki cannot test J (bike index 3)
solver.add(assign[3][0] != 3)
solver.add(assign[3][1] != 3)

# Condition 3: Theresa must be one of the testers for H (bike index 2)
# i.e., Theresa tests H on at least one of the two days
solver.add(Or(assign[2][0] == 2, assign[2][1] == 2))

# Condition 4: The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# Yuki is index 3, Seamus is index 1
solver.add(assign[1][1] == assign[3][0])

# Now evaluate each option
# Each option says "Both X and Y test Z" — meaning both test the same bike Z.
# But note: each rider tests two different bikes (one each day). So "Both X and Y test Z"
# means there exists some day for X and some day for Y such that they both test Z.
# More precisely: X tests Z on some day, and Y tests Z on some day (possibly different days).

# Option A: Both Reynaldo and Seamus test J (bike index 3)
opt_a = And(
    Or(assign[0][0] == 3, assign[0][1] == 3),  # Reynaldo tests J
    Or(assign[1][0] == 3, assign[1][1] == 3)   # Seamus tests J
)

# Option B: Both Reynaldo and Theresa test J (bike index 3)
opt_b = And(
    Or(assign[0][0] == 3, assign[0][1] == 3),  # Reynaldo tests J
    Or(assign[2][0] == 3, assign[2][1] == 3)   # Theresa tests J
)

# Option C: Both Reynaldo and Yuki test G (bike index 1)
opt_c = And(
    Or(assign[0][0] == 1, assign[0][1] == 1),  # Reynaldo tests G
    Or(assign[3][0] == 1, assign[3][1] == 1)   # Yuki tests G
)

# Option D: Both Seamus and Theresa test G (bike index 1)
opt_d = And(
    Or(assign[1][0] == 1, assign[1][1] == 1),  # Seamus tests G
    Or(assign[2][0] == 1, assign[2][1] == 1)   # Theresa tests G
)

# Option E: Both Theresa and Yuki test F (bike index 0)
opt_e = And(
    Or(assign[2][0] == 0, assign[2][1] == 0),  # Theresa tests F
    Or(assign[3][0] == 0, assign[3][1] == 0)   # Yuki tests F
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