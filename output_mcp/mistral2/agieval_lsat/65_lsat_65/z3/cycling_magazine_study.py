from z3 import *

solver = Solver()

# Riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Days
days = ["Day1", "Day2"]

# Create a 2D array: rider x day -> bicycle
assignments = [[Int(f"{r}_{d}") for d in days] for r in riders]

# Each rider must test a bicycle on each day (one of F, G, H, J)
for r in riders:
    for d in days:
        solver.add(Or([assignments[riders.index(r)][days.index(d)] == b for b in bicycles]))

# Each bicycle is tested by exactly one rider per day
for d in days:
    for b in bicycles:
        solver.add(Sum([If(assignments[r][days.index(d)] == b, 1, 0) for r in range(len(riders))]) == 1)

# Constraints
# Reynaldo cannot test F
solver.add(assignments[riders.index("Reynaldo")][days.index("Day1")] != "F")
solver.add(assignments[riders.index("Reynaldo")][days.index("Day2")] != "F")

# Yuki cannot test J
solver.add(assignments[riders.index("Yuki")][days.index("Day1")] != "J")
solver.add(assignments[riders.index("Yuki")][days.index("Day2")] != "J")

# Theresa must be one of the testers for H
solver.add(Or([assignments[riders.index("Theresa")][days.index(d)] == "H" for d in days]))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(ForAll([b], Implies(
    assignments[riders.index("Yuki")][days.index("Day1")] == b,
    assignments[riders.index("Seamus")][days.index("Day2")] == b
)))

# Additional constraint: Each rider tests a different bicycle on Day2 than on Day1
for r in riders:
    solver.add(assignments[riders.index(r)][days.index("Day1")] != assignments[riders.index(r)][days.index("Day2")])

# Now evaluate the multiple choice options
found_options = []

# Option A: Both Reynaldo and Seamus test J
# This means Reynaldo tests J on Day1 and Seamus tests J on Day2
solver.push()
solver.add(assignments[riders.index("Reynaldo")][days.index("Day1")] == "J")
solver.add(assignments[riders.index("Seamus")][days.index("Day2")] == "J")
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Both Reynaldo and Theresa test J
# This means Reynaldo tests J on Day1 and Theresa tests J on Day1
solver.push()
solver.add(assignments[riders.index("Reynaldo")][days.index("Day1")] == "J")
solver.add(assignments[riders.index("Theresa")][days.index("Day1")] == "J")
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Both Reynaldo and Yuki test G
# This means Reynaldo tests G on Day1 and Yuki tests G on Day1
solver.push()
solver.add(assignments[riders.index("Reynaldo")][days.index("Day1")] == "G")
solver.add(assignments[riders.index("Yuki")][days.index("Day1")] == "G")
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Both Seamus and Theresa test G
# This means Seamus tests G on Day1 and Theresa tests G on Day1
solver.push()
solver.add(assignments[riders.index("Seamus")][days.index("Day1")] == "G")
solver.add(assignments[riders.index("Theresa")][days.index("Day1")] == "G")
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Both Theresa and Yuki test F
# This means Theresa tests F on Day1 and Yuki tests F on Day1
solver.push()
solver.add(assignments[riders.index("Theresa")][days.index("Day1")] == "F")
solver.add(assignments[riders.index("Yuki")][days.index("Day1")] == "F")
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