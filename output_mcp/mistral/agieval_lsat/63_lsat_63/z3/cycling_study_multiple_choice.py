from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]
bike_to_int = {b: i for i, b in enumerate(bicycles)}
int_to_bike = {i: b for i, b in enumerate(bicycles)}

# Declare variables: rider x day -> bicycle (as int)
# day 0 = first day, day 1 = second day
assignments = [[Int(f"{r}_day{d}") for d in range(2)] for r in riders]

solver = Solver()

# Helper: All bicycles are tested each day (no duplicates per day)
for day in range(2):
    solver.add(Distinct([assignments[r][day] for r in range(4)]))

# Helper: Each rider tests a different bicycle each day (no duplicates per rider across days)
for rider in range(4):
    solver.add(Distinct([assignments[rider][day] for day in range(2)]))

# Constraints from the problem statement
# 1. Reynaldo cannot test F (0)
reynaldo_idx = riders.index("Reynaldo")
solver.add(assignments[reynaldo_idx][0] != bike_to_int["F"])
solver.add(assignments[reynaldo_idx][1] != bike_to_int["F"])

# 2. Yuki cannot test J (3)
yuki_idx = riders.index("Yuki")
solver.add(assignments[yuki_idx][0] != bike_to_int["J"])
solver.add(assignments[yuki_idx][1] != bike_to_int["J"])

# 3. Theresa must test H (2) on at least one day
theresa_idx = riders.index("Theresa")
solver.add(Or(
    assignments[theresa_idx][0] == bike_to_int["H"],
    assignments[theresa_idx][1] == bike_to_int["H"]
))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
seamus_idx = riders.index("Seamus")
solver.add(
    assignments[yuki_idx][0] == assignments[seamus_idx][1]
)

# Base constraints are now fully encoded

# Now evaluate each multiple-choice option
found_options = []

# Option A: Reynaldo tests G on the second day
solver.push()
solver.add(assignments[reynaldo_idx][1] == bike_to_int["G"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Seamus tests F on the first day
solver.push()
solver.add(assignments[seamus_idx][0] == bike_to_int["F"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Theresa tests F on the second day
solver.push()
solver.add(assignments[theresa_idx][1] == bike_to_int["F"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Reynaldo tests H on the first day
solver.push()
solver.add(assignments[reynaldo_idx][0] == bike_to_int["H"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yuki tests F on the second day
solver.push()
solver.add(assignments[yuki_idx][1] == bike_to_int["F"])
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