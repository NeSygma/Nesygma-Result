from z3 import *

solver = Solver()

# Riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Day 1 and Day 2 assignments
# We model assignments as dictionaries: {rider: bicycle}
day1 = {r: Int(f"day1_{r}") for r in riders}
day2 = {r: Int(f"day2_{r}") for r in riders}

# Each rider gets a unique bicycle per day
solver.add(Distinct(list(day1.values())))
solver.add(Distinct(list(day2.values())))

# Each bicycle is tested each day (implied by Distinct and domain)

# Constraints
# Reynaldo cannot test F
solver.add(day1["Reynaldo"] != "F")
solver.add(day2["Reynaldo"] != "F")

# Yuki cannot test J
solver.add(day1["Yuki"] != "J")
solver.add(day2["Yuki"] != "J")

# Theresa must be one of the testers for H
solver.add(Or([day1[r] == "H" for r in riders]))
solver.add(Or([day2[r] == "H" for r in riders]))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(ForAll([r], Implies(day1[r] == day1["Yuki"], day2["Seamus"] == day1[r])))

# Helper function to check if a constraint is satisfiable
found_options = []

# Option A: Reynaldo tests J on the first day
solver.push()
solver.add(day1["Reynaldo"] == "J")
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Reynaldo tests J on the second day
solver.push()
solver.add(day2["Reynaldo"] == "J")
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Seamus tests H on the first day
solver.push()
solver.add(day1["Seamus"] == "H")
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yuki tests H on the first day
solver.push()
solver.add(day1["Yuki"] == "H")
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yuki tests H on the second day
solver.push()
solver.add(day2["Yuki"] == "H")
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