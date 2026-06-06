from z3 import *

# BENCHMARK_MODE: ON (model-finding with single correct answer expected)
BENCHMARK_MODE = True

solver = Solver()

# 1. Declare symbolic variables
# bird[i] = bird type for lecture i (0: oystercatchers, 1: petrels, 2: rails, 3: sandpipers, 4: terns)
# Use Z3 Array to allow symbolic indexing
bird = Array('bird', IntSort(), IntSort())
# location[i] = True means Howard Auditorium, False means Gladwyn Hall
location = Array('location', IntSort(), BoolSort())

# Helper: Define bird types for each lecture
# We will constrain the values at indices 0..4
lecture_indices = [0, 1, 2, 3, 4]

# 2. Add base constraints from the problem

# Each bird type appears exactly once among lectures 0..4
solver.add(Distinct([bird[i] for i in lecture_indices]))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(Not(location[0]))

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(location[3])

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(Not(location[i]), 1, 0) for i in lecture_indices]) == 3)

# Constraint 4: Sandpipers (3) is in Howard and is earlier than oystercatchers (0)
# Find index of sandpipers and oystercatchers
sandpiper_idx = Int('sandpiper_idx')
oystercatcher_idx = Int('oystercatcher_idx')
solver.add(sandpiper_idx >= 0, sandpiper_idx < 5)
solver.add(oystercatcher_idx >= 0, oystercatcher_idx < 5)
solver.add(bird[sandpiper_idx] == 3)
solver.add(bird[oystercatcher_idx] == 0)
solver.add(location[sandpiper_idx])  # sandpipers in Howard
solver.add(sandpiper_idx < oystercatcher_idx)  # sandpipers earlier than oystercatchers

# Constraint 5: Terns (4) is earlier than petrels (1), and petrels is in Gladwyn Hall
# Find index of terns and petrels
tern_idx = Int('tern_idx')
petrel_idx = Int('petrel_idx')
solver.add(tern_idx >= 0, tern_idx < 5)
solver.add(petrel_idx >= 0, petrel_idx < 5)
solver.add(bird[tern_idx] == 4)
solver.add(bird[petrel_idx] == 1)
solver.add(tern_idx < petrel_idx)  # terns earlier than petrels
solver.add(Not(location[petrel_idx]))  # petrels in Gladwyn Hall

# Additional condition: Third lecture (index 2) is on sandpipers
solver.add(bird[2] == 3)

# 3. Check base constraints are satisfiable
base_result = solver.check()
if base_result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    exit(0)

# 4. Evaluate multiple-choice options
found_options = []

# Option A: Second lecture is on oystercatchers and is in Gladwyn Hall
solver.push()
solver.add(bird[1] == 0)
solver.add(Not(location[1]))
opt_a_result = solver.check()
solver.pop()
if opt_a_result == sat:
    found_options.append("A")

# Option B: Fifth lecture is on oystercatchers and is in Howard Auditorium
solver.push()
solver.add(bird[4] == 0)
solver.add(location[4])
opt_b_result = solver.check()
solver.pop()
if opt_b_result == sat:
    found_options.append("B")

# Option C: Second lecture is on rails and is in Howard Auditorium
solver.push()
solver.add(bird[1] == 2)
solver.add(location[1])
opt_c_result = solver.check()
solver.pop()
if opt_c_result == sat:
    found_options.append("C")

# Option D: Second lecture is on terns and is in Gladwyn Hall
solver.push()
solver.add(bird[1] == 4)
solver.add(Not(location[1]))
opt_d_result = solver.check()
solver.pop()
if opt_d_result == sat:
    found_options.append("D")

# Option E: Fourth lecture is on terns and is in Howard Auditorium
solver.push()
solver.add(bird[3] == 4)
# location[3] is already constrained to be Howard, so no need to add again
opt_e_result = solver.check()
solver.pop()
if opt_e_result == sat:
    found_options.append("E")

# 5. Determine final answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")