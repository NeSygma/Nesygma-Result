from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare riders and bikes
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bikes = ["F", "G", "H", "J"]
bike_to_int = {b: i for i, b in enumerate(bikes)}
int_to_bike = {i: b for i, b in enumerate(bikes)}

# Declare days
days = [1, 2]

# Create a 2D array: assignment[day][rider] = bike_int
assignment = [[Int(f"assignment_{day}_{rider}") for rider in riders] for day in days]

# Create solver
solver = Solver()

# Helper function to get bike name from int

def bike_name(bike_int):
    return int_to_bike[bike_int]

# Base constraints

# 1. Domain: each assignment is a valid bike
for day in days:
    for rider_idx in range(len(riders)):
        solver.add(And(assignment[day-1][rider_idx] >= 0, assignment[day-1][rider_idx] <= 3))

# 2. Reynaldo cannot test F (0)
for day in days:
    solver.add(assignment[day-1][0] != 0)  # Reynaldo is index 0

# 3. Yuki cannot test J (3)
for day in days:
    solver.add(assignment[day-1][3] != 3)  # Yuki is index 3

# 4. Theresa must test H (2) on at least one day
solver.add(Or(assignment[0][2] == 2, assignment[1][2] == 2))  # Theresa is index 2

# 5. The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
# Yuki is index 3, Seamus is index 1
solver.add(assignment[0][3] == assignment[1][1])

# 6. All bicycles are tested each day
for day in days:
    day_assignments = assignment[day-1]
    # For each bike, at least one rider has it
    for bike in range(4):
        solver.add(Or([day_assignments[r] == bike for r in range(4)]))

# 7. Each rider tests a different bike on Day 2 than Day 1
for rider_idx in range(4):
    solver.add(assignment[0][rider_idx] != assignment[1][rider_idx])

# Now, evaluate each option
found_options = []

# Option A: Both Reynaldo and Seamus test J (3) on the same day
# Check both days
opt_a_constr_day1 = And(assignment[0][0] == 3, assignment[0][1] == 3)
opt_a_constr_day2 = And(assignment[1][0] == 3, assignment[1][1] == 3)

solver.push()
solver.add(Or(opt_a_constr_day1, opt_a_constr_day2))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Both Reynaldo and Theresa test J (3) on the same day
opt_b_constr_day1 = And(assignment[0][0] == 3, assignment[0][2] == 3)
opt_b_constr_day2 = And(assignment[1][0] == 3, assignment[1][2] == 3)

solver.push()
solver.add(Or(opt_b_constr_day1, opt_b_constr_day2))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Both Reynaldo and Yuki test G (1) on the same day
opt_c_constr_day1 = And(assignment[0][0] == 1, assignment[0][3] == 1)
opt_c_constr_day2 = And(assignment[1][0] == 1, assignment[1][3] == 1)

solver.push()
solver.add(Or(opt_c_constr_day1, opt_c_constr_day2))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Both Seamus and Theresa test G (1) on the same day
opt_d_constr_day1 = And(assignment[0][1] == 1, assignment[0][2] == 1)
opt_d_constr_day2 = And(assignment[1][1] == 1, assignment[1][2] == 1)

solver.push()
solver.add(Or(opt_d_constr_day1, opt_d_constr_day2))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Both Theresa and Yuki test F (0) on the same day
opt_e_constr_day1 = And(assignment[0][2] == 0, assignment[0][3] == 0)
opt_e_constr_day2 = And(assignment[1][2] == 0, assignment[1][3] == 0)

solver.push()
solver.add(Or(opt_e_constr_day1, opt_e_constr_day2))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")