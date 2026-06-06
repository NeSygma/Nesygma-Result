from z3 import *

solver = Solver()

# Define historian indices
FARLEY = 0
GARCIA = 1
HOLDEN = 2
JIANG = 3

# Define topic indices
LITHOGRAPHS = 0
OIL = 1
SCULPTURES = 2
WATERCOLORS = 3

# Variables: topic[i] = topic given by historian i, time[i] = time slot of historian i
topic = [Int(f'topic_{i}') for i in range(4)]
time = [Int(f'time_{i}') for i in range(4)]

# Domain constraints
for i in range(4):
    solver.add(topic[i] >= 0, topic[i] <= 3)
    solver.add(time[i] >= 1, time[i] <= 4)

# All topics distinct
solver.add(Distinct(topic))
# All times distinct
solver.add(Distinct(time))

# Watercolors lecture is third
solver.add(Or([And(topic[i] == WATERCOLORS, time[i] == 3) for i in range(4)]))

# Oil paintings and watercolors earlier than lithographs
# time_oil < time_lith and time_water < time_lith
solver.add(Or([And(topic[i] == OIL, topic[j] == LITHOGRAPHS, time[i] < time[j]) for i in range(4) for j in range(4) if i != j]))
solver.add(Or([And(topic[i] == WATERCOLORS, topic[j] == LITHOGRAPHS, time[i] < time[j]) for i in range(4) for j in range(4) if i != j]))

# Farley's lecture earlier than oil paintings
solver.add(Or([And(topic[i] == OIL, time[FARLEY] < time[i]) for i in range(4)]))

# Holden's lecture earlier than Garcia's and Jiang's
solver.add(time[HOLDEN] < time[GARCIA])
solver.add(time[HOLDEN] < time[JIANG])

# Now evaluate each answer choice
found_options = []

# Option A: Farley gives the watercolors lecture
solver.push()
solver.add(topic[FARLEY] == WATERCOLORS)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia gives the oil paintings lecture
solver.push()
solver.add(topic[GARCIA] == OIL)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Garcia gives the sculptures lecture
solver.push()
solver.add(topic[GARCIA] == SCULPTURES)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Holden gives the sculptures lecture
solver.push()
solver.add(topic[HOLDEN] == SCULPTURES)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Jiang gives the lithographs lecture
solver.push()
solver.add(topic[JIANG] == LITHOGRAPHS)
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