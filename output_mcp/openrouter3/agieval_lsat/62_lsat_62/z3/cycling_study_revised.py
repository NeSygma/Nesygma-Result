from z3 import *

# Create solver
solver = Solver()

# Define bicycle indices
F, G, H, J = 0, 1, 2, 3
bicycle_names = {F: "F", G: "G", H: "H", J: "J"}

# Rider indices
REYNALDO, SEAMUS, THERESA, YUKI = 0, 1, 2, 3
rider_names = {REYNALDO: "Reynaldo", SEAMUS: "Seamus", THERESA: "Theresa", YUKI: "Yuki"}

# Variables: rider_day[rider][day] = bicycle tested
# day 0 = first day, day 1 = second day
rider_day = [[Int(f"r{r}_d{d}") for d in range(2)] for r in range(4)]

# Domain constraints: each rider tests exactly one bicycle per day (0-3)
for r in range(4):
    for d in range(2):
        solver.add(rider_day[r][d] >= 0)
        solver.add(rider_day[r][d] <= 3)

# Each bicycle is tested by exactly one rider per day
for d in range(2):
    for b in range(4):
        # Exactly one rider tests bicycle b on day d
        solver.add(Or([rider_day[r][d] == b for r in range(4)]))
        # No two riders test the same bicycle on the same day
        for r1 in range(4):
            for r2 in range(r1+1, 4):
                solver.add(rider_day[r1][d] != rider_day[r2][d])

# Constraint 1: Reynaldo cannot test F (on either day)
solver.add(rider_day[REYNALDO][0] != F)
solver.add(rider_day[REYNALDO][1] != F)

# Constraint 2: Yuki cannot test J (on either day)
solver.add(rider_day[YUKI][0] != J)
solver.add(rider_day[YUKI][1] != J)

# Constraint 3: Theresa must be one of the testers for H (on either day)
solver.add(Or(rider_day[THERESA][0] == H, rider_day[THERESA][1] == H))

# Constraint 4: The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
solver.add(rider_day[SEAMUS][1] == rider_day[YUKI][0])

# Now evaluate each option to find which CANNOT be true
# Option A: Reynaldo tests J on the first day
opt_a_constr = (rider_day[REYNALDO][0] == J)

# Option B: Reynaldo tests J on the second day
opt_b_constr = (rider_day[REYNALDO][1] == J)

# Option C: Seamus tests H on the first day
opt_c_constr = (rider_day[SEAMUS][0] == H)

# Option D: Yuki tests H on the first day
opt_d_constr = (rider_day[YUKI][0] == H)

# Option E: Yuki tests H on the second day
opt_e_constr = (rider_day[YUKI][1] == H)

# Test each option - we want to find which one is impossible (unsat)
impossible_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

# Print results
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")