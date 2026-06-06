from z3 import *

solver = Solver()

# Riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Map bicycles to integers for Z3
bicycle_to_int = {"F": 0, "G": 1, "H": 2, "J": 3}
int_to_bicycle = {v: k for k, v in bicycle_to_int.items()}

# Day 1 and Day 2 assignments
# We model assignments as dictionaries: {rider: bicycle (as Int)}
day1 = {r: Int(f"day1_{r}") for r in riders}
day2 = {r: Int(f"day2_{r}") for r in riders}

# Each rider gets a unique bicycle per day
solver.add(Distinct(list(day1.values())))
solver.add(Distinct(list(day2.values())))

# Domain constraints for bicycles (0 to 3)
for r in riders:
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# Constraints
# Reynaldo cannot test F (0)
solver.add(day1["Reynaldo"] != bicycle_to_int["F"])
solver.add(day2["Reynaldo"] != bicycle_to_int["F"])

# Yuki cannot test J (3)
solver.add(day1["Yuki"] != bicycle_to_int["J"])
solver.add(day2["Yuki"] != bicycle_to_int["J"])

# Theresa must test H (2) on both days
solver.add(day1["Theresa"] == bicycle_to_int["H"])
solver.add(day2["Theresa"] == bicycle_to_int["H"])

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(day2["Seamus"] == day1["Yuki"])

# Helper function to check if a constraint is satisfiable
found_options = []

# Option A: Reynaldo tests J on the first day
solver.push()
solver.add(day1["Reynaldo"] == bicycle_to_int["J"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Reynaldo tests J on the second day
solver.push()
solver.add(day2["Reynaldo"] == bicycle_to_int["J"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Seamus tests H on the first day
solver.push()
solver.add(day1["Seamus"] == bicycle_to_int["H"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yuki tests H on the first day
solver.push()
solver.add(day1["Yuki"] == bicycle_to_int["H"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yuki tests H on the second day
solver.push()
solver.add(day2["Yuki"] == bicycle_to_int["H"])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Evaluate results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")