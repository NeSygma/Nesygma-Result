from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for targets
# Clients: Image, Solide, Truvest
# Channels: Website, Voicemail

# Targets are 1, 2, or 3 (days)
# We'll use Int variables for each target

# Clients: 0=Image, 1=Solide, 2=Truvest
# Channels: 0=Website, 1=Voicemail

# Target variables: targets[client][channel]
targets = [[Int(f"target_{i}_{j}") for j in range(2)] for i in range(3)]

# Website=0, Voicemail=1
solver = Solver()

# Add constraints

# 1. None of the clients can have a website target that is longer than its voicemail target
for client in range(3):
    solver.add(targets[client][0] <= targets[client][1])

# 2. Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(targets[0][1] < targets[1][1])  # Image < Solide
solver.add(targets[0][1] < targets[2][1])  # Image < Truvest

# 3. Solide's website target must be shorter than Truvest's website target
solver.add(targets[1][0] < targets[2][0])  # Solide < Truvest

# Targets can only be 1, 2, or 3
for client in range(3):
    for channel in range(2):
        solver.add(Or(targets[client][channel] == 1, 
                      targets[client][channel] == 2, 
                      targets[client][channel] == 3))

# Now evaluate each option to see if it can be set for more than one client

# Option A: a 1-day website target
# Check if at least two clients can have a 1-day website target
solver.push()
solver.add(Or(
    And(targets[0][0] == 1, targets[1][0] == 1),
    And(targets[0][0] == 1, targets[2][0] == 1),
    And(targets[1][0] == 1, targets[2][0] == 1)
))
result_A = solver.check()
solver.pop()

# Option B: a 2-day voicemail target
# Check if at least two clients can have a 2-day voicemail target
solver.push()
solver.add(Or(
    And(targets[0][1] == 2, targets[1][1] == 2),
    And(targets[0][1] == 2, targets[2][1] == 2),
    And(targets[1][1] == 2, targets[2][1] == 2)
))
result_B = solver.check()
solver.pop()

# Option C: a 2-day website target
# Check if at least two clients can have a 2-day website target
solver.push()
solver.add(Or(
    And(targets[0][0] == 2, targets[1][0] == 2),
    And(targets[0][0] == 2, targets[2][0] == 2),
    And(targets[1][0] == 2, targets[2][0] == 2)
))
result_C = solver.check()
solver.pop()

# Option D: a 3-day voicemail target
# Check if at least two clients can have a 3-day voicemail target
solver.push()
solver.add(Or(
    And(targets[0][1] == 3, targets[1][1] == 3),
    And(targets[0][1] == 3, targets[2][1] == 3),
    And(targets[1][1] == 3, targets[2][1] == 3)
))
result_D = solver.check()
solver.pop()

# Option E: a 3-day website target
# Check if at least two clients can have a 3-day website target
solver.push()
solver.add(Or(
    And(targets[0][0] == 3, targets[1][0] == 3),
    And(targets[0][0] == 3, targets[2][0] == 3),
    And(targets[1][0] == 3, targets[2][0] == 3)
))
result_E = solver.check()
solver.pop()

# Evaluate results
found_options = []
if result_A == sat:
    found_options.append("A")
if result_B == sat:
    found_options.append("B")
if result_C == sat:
    found_options.append("C")
if result_D == sat:
    found_options.append("D")
if result_E == sat:
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")