from z3 import *

# Define riders and bicycles as integers for simplicity
Riders = ['Reynaldo', 'Seamus', 'Theresa', 'Yuki']
Bicycles = ['F', 'G', 'H', 'J']

# Create a 2D array for assignments: assignment[rider][day] = bicycle
# Days: 0 = Day 1, 1 = Day 2
assignment = [[Int(f"{rider}_{day}") for day in range(2)] for rider in Riders]

solver = Solver()

# Helper function to get the index of a rider or bicycle
def get_rider_index(rider):
    return Riders.index(rider)

def get_bicycle_index(bicycle):
    return Bicycles.index(bicycle)

# Constraints:
# 1. Each rider tests a different bicycle each day
for rider in Riders:
    for day in range(2):
        solver.add(And(assignment[get_rider_index(rider)][day] >= 0,
                       assignment[get_rider_index(rider)][day] < 4))

# 2. All bicycles are tested each day
for day in range(2):
    solver.add(Distinct([assignment[rider_idx][day] for rider_idx in range(4)]))

# 3. Reynaldo cannot test F (F = 0)
solver.add(assignment[get_rider_index('Reynaldo')][0] != 0)
solver.add(assignment[get_rider_index('Reynaldo')][1] != 0)

# 4. Yuki cannot test J (J = 3)
solver.add(assignment[get_rider_index('Yuki')][0] != 3)
solver.add(assignment[get_rider_index('Yuki')][1] != 3)

# 5. Theresa must test H (H = 2) on at least one day
solver.add(Or(assignment[get_rider_index('Theresa')][0] == 2,
              assignment[get_rider_index('Theresa')][1] == 2))

# 6. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(assignment[get_rider_index('Yuki')][0] == assignment[get_rider_index('Seamus')][1])

# 7. Given: Theresa tests G (G = 1) on the second day
solver.add(assignment[get_rider_index('Theresa')][1] == 1)

# Multiple choice options:
# (A) Reynaldo tests H (H = 2) on the first day
opt_a_constr = (assignment[get_rider_index('Reynaldo')][0] == 2)

# (B) Reynaldo tests J (J = 3) on the first day
opt_b_constr = (assignment[get_rider_index('Reynaldo')][0] == 3)

# (C) Theresa tests H (H = 2) on the second day
# But we already have Theresa tests G on the second day, so this is impossible
opt_c_constr = (assignment[get_rider_index('Theresa')][1] == 2)

# (D) Theresa tests J (J = 3) on the first day
opt_d_constr = (assignment[get_rider_index('Theresa')][0] == 3)

# (E) Yuki tests H (H = 2) on the second day
opt_e_constr = (assignment[get_rider_index('Yuki')][1] == 2)

# Evaluate each option
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