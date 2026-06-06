from z3 import *

solver = Solver()

# Declare riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Map bicycles to integers for Z3
bicycle_to_int = {"F": 0, "G": 1, "H": 2, "J": 3}
int_to_bicycle = {0: "F", 1: "G", 2: "H", 3: "J"}

# Declare variables for day 1 and day 2 assignments as integers
day1 = {r: Int(f"day1_{r}") for r in riders}
day2 = {r: Int(f"day2_{r}") for r in riders}

# Each rider is assigned a unique bicycle each day
solver.add(Distinct(list(day1.values())))
solver.add(Distinct(list(day2.values())))

# Constraints from the problem statement
# Reynaldo cannot test F (0)
solver.add(day1["Reynaldo"] != bicycle_to_int["F"])
solver.add(day2["Reynaldo"] != bicycle_to_int["F"])

# Yuki cannot test J (3)
solver.add(day1["Yuki"] != bicycle_to_int["J"])
solver.add(day2["Yuki"] != bicycle_to_int["J"])

# Theresa must be one of the testers for H (2)
solver.add(Or(day1["Theresa"] == bicycle_to_int["H"], day2["Theresa"] == bicycle_to_int["H"]))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
# Fix: Use a loop to add constraints for each possible bicycle
for b in bicycles:
    solver.add(Implies(day1["Yuki"] == bicycle_to_int[b], day2["Seamus"] == bicycle_to_int[b]))

# Bounds for bicycle assignments (0 to 3)
for r in riders:
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# Now evaluate the multiple choice options
found_options = []

# Option A: Reynaldo tests G (1) on the second day
solver.push()
solver.add(day2["Reynaldo"] == bicycle_to_int["G"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Seamus tests F (0) on the first day
solver.push()
solver.add(day1["Seamus"] == bicycle_to_int["F"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Theresa tests F (0) on the second day
solver.push()
solver.add(day2["Theresa"] == bicycle_to_int["F"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Reynaldo tests H (2) on the first day
solver.push()
solver.add(day1["Reynaldo"] == bicycle_to_int["H"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yuki tests F (0) on the second day
solver.push()
solver.add(day2["Yuki"] == bicycle_to_int["F"])
if solver.check() == sat:
    found_options.append("E")
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