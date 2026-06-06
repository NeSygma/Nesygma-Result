from z3 import *

# Define riders and bicycles as symbolic constants
Riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
Bikes = ["F", "G", "H", "J"]

# Map riders and bikes to Int values for Z3
rider_to_int = {r: i for i, r in enumerate(Riders)}
bike_to_int = {b: i for i, b in enumerate(Bikes)}

# Create solver
solver = Solver()

# Declare variables for assignments: day1[rider] and day2[rider]
day1 = [Int(f"day1_{r}") for r in Riders]
day2 = [Int(f"day2_{r}") for r in Riders]

# Helper function to convert bike names to Int values
def bike_name_to_int(b):
    return bike_to_int[b]

# Base constraints

# 1. Each rider tests a different bike on day2 than on day1
for i in range(len(Riders)):
    solver.add(day1[i] != day2[i])

# 2. All bikes are tested each day
# For day1: all bikes must appear in day1 assignments
solver.add(Distinct(day1))
# For day2: all bikes must appear in day2 assignments
solver.add(Distinct(day2))

# 3. Reynaldo cannot test F
reynaldo_idx = rider_to_int["Reynaldo"]
solver.add(day1[reynaldo_idx] != bike_name_to_int("F"))
solver.add(day2[reynaldo_idx] != bike_name_to_int("F"))

# 4. Yuki cannot test J
solver.add(day1[rider_to_int["Yuki"]] != bike_name_to_int("J"))
solver.add(day2[rider_to_int["Yuki"]] != bike_name_to_int("J"))

# 5. Theresa must test H on at least one day
theresa_idx = rider_to_int["Theresa"]
solver.add(Or(
    day1[theresa_idx] == bike_name_to_int("H"),
    day2[theresa_idx] == bike_name_to_int("H")
))

# 6. If Yuki tests bike X on day1, Seamus tests X on day2
# This is a conditional constraint: day1[Yuki] = X => day2[Seamus] = X
# We can model this by ensuring that day2[Seamus] = day1[Yuki]
seamus_idx = rider_to_int["Seamus"]
yuki_idx = rider_to_int["Yuki"]
solver.add(day2[seamus_idx] == day1[yuki_idx])

# Now evaluate each option
found_options = []

# Option A: Both Reynaldo and Seamus test J
# This means Reynaldo's assignment (either day) is J, and Seamus's assignment (either day) is J
solver.push()
solver.add(Or(
    day1[reynaldo_idx] == bike_name_to_int("J"),
    day2[reynaldo_idx] == bike_name_to_int("J")
))
solver.add(Or(
    day1[seamus_idx] == bike_name_to_int("J"),
    day2[seamus_idx] == bike_name_to_int("J")
))
opt_a_res = solver.check()
solver.pop()

# Option B: Both Reynaldo and Theresa test G
solver.push()
solver.add(Or(
    day1[reynaldo_idx] == bike_name_to_int("G"),
    day2[reynaldo_idx] == bike_name_to_int("G")
))
solver.add(Or(
    day1[theresa_idx] == bike_name_to_int("G"),
    day2[theresa_idx] == bike_name_to_int("G")
))
opt_b_res = solver.check()
solver.pop()

# Option C: Both Reynaldo and Yuki test G
solver.push()
solver.add(Or(
    day1[reynaldo_idx] == bike_name_to_int("G"),
    day2[reynaldo_idx] == bike_name_to_int("G")
))
solver.add(Or(
    day1[yuki_idx] == bike_name_to_int("G"),
    day2[yuki_idx] == bike_name_to_int("G")
))
opt_c_res = solver.check()
solver.pop()

# Option D: Both Seamus and Theresa test G
solver.push()
solver.add(Or(
    day1[seamus_idx] == bike_name_to_int("G"),
    day2[seamus_idx] == bike_name_to_int("G")
))
solver.add(Or(
    day1[theresa_idx] == bike_name_to_int("G"),
    day2[theresa_idx] == bike_name_to_int("G")
))
opt_d_res = solver.check()
solver.pop()

# Option E: Both Theresa and Yuki test F
solver.push()
solver.add(Or(
    day1[theresa_idx] == bike_name_to_int("F"),
    day2[theresa_idx] == bike_name_to_int("F")
))
solver.add(Or(
    day1[yuki_idx] == bike_name_to_int("F"),
    day2[yuki_idx] == bike_name_to_int("F")
))
opt_e_res = solver.check()
solver.pop()

# Collect results
found_options = []
if opt_a_res == sat:
    found_options.append("A")
if opt_b_res == sat:
    found_options.append("B")
if opt_c_res == sat:
    found_options.append("C")
if opt_d_res == sat:
    found_options.append("D")
if opt_e_res == sat:
    found_options.append("E")

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")