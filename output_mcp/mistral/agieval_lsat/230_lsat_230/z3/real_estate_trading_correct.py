from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Define companies
RealProp = Int("RealProp")
Southco = Int("Southco")
Trustcorp = Int("Trustcorp")

# Define building classes
class1 = Int("class1")
class2 = Int("class2")
class3 = Int("class3")

# Initial counts of buildings per class per company
# RealProp initially owns 1 class1, 0 class2, 2 class3
# Southco initially owns 1 class1, 1 class2, 0 class3
# Trustcorp initially owns 0 class1, 3 class2, 0 class3

# Variables for final counts
rp_c1 = Int("rp_c1")  # RealProp class1
rp_c2 = Int("rp_c2")  # RealProp class2
rp_c3 = Int("rp_c3")  # RealProp class3
sc_c1 = Int("sc_c1")  # Southco class1
sc_c2 = Int("sc_c2")  # Southco class2
sc_c3 = Int("sc_c3")  # Southco class3
tc_c1 = Int("tc_c1")  # Trustcorp class1
tc_c2 = Int("tc_c2")  # Trustcorp class2
tc_c3 = Int("tc_c3")  # Trustcorp class3

# Initial state constraints
solver.add(rp_c1 == 1, rp_c2 == 0, rp_c3 == 2)
solver.add(sc_c1 == 1, sc_c2 == 1, sc_c3 == 0)
solver.add(tc_c1 == 0, tc_c2 == 3, tc_c3 == 0)

# Total buildings per class must remain constant
total_c1 = rp_c1 + sc_c1 + tc_c1
solver.add(total_c1 == 2)  # Initial total class1 buildings
total_c2 = rp_c2 + sc_c2 + tc_c2
solver.add(total_c2 == 4)  # Initial total class2 buildings
total_c3 = rp_c3 + sc_c3 + tc_c3
solver.add(total_c3 == 2)  # Initial total class3 buildings

# Now, let's define the multiple choice options as constraints on the final counts

# Option A: RealProp owns Lynch Building, Meyer Building, and Ortiz Building
# These are all class2 buildings, so RealProp would own 0 class1, 3 class2, 0 class3
option_a = And(
    rp_c1 == 0,
    rp_c2 == 3,
    rp_c3 == 0
)

# Option B: Southco owns Garza Tower (class1) and Meyer Building (class2)
# So Southco would own 1 class1, 1 class2, 0 class3
option_b = And(
    sc_c1 == 1,
    sc_c2 == 1,
    sc_c3 == 0
)

# Option C: Southco owns King Building, Meyer Building, and Ortiz Building (all class2)
# So Southco would own 0 class1, 3 class2, 0 class3
option_c = And(
    sc_c1 == 0,
    sc_c2 == 3,
    sc_c3 == 0
)

# Option D: Trustcorp owns Flores Tower (class1) and Yates House (class3)
# So Trustcorp would own 1 class1, 0 class2, 1 class3
option_d = And(
    tc_c1 == 1,
    tc_c2 == 0,
    tc_c3 == 1
)

# Option E: Trustcorp owns Garza Tower (class1) and Lynch Building (class2)
# So Trustcorp would own 1 class1, 1 class2, 0 class3
option_e = And(
    tc_c1 == 1,
    tc_c2 == 1,
    tc_c3 == 0
)

# Now, we check which of these options CANNOT be true (i.e., are unsatisfiable)
unsat_options = []

# Check Option A
solver.push()
solver.add(option_a)
if solver.check() == unsat:
    unsat_options.append("A")
    print("Option A is UNSAT (cannot be true)")
else:
    print("Option A is SAT (can be true)")
solver.pop()

# Check Option B
solver.push()
solver.add(option_b)
if solver.check() == unsat:
    unsat_options.append("B")
    print("Option B is UNSAT (cannot be true)")
else:
    print("Option B is SAT (can be true)")
solver.pop()

# Check Option C
solver.push()
solver.add(option_c)
if solver.check() == unsat:
    unsat_options.append("C")
    print("Option C is UNSAT (cannot be true)")
else:
    print("Option C is SAT (can be true)")
solver.pop()

# Check Option D
solver.push()
solver.add(option_d)
if solver.check() == unsat:
    unsat_options.append("D")
    print("Option D is UNSAT (cannot be true)")
else:
    print("Option D is SAT (can be true)")
solver.pop()

# Check Option E
solver.push()
solver.add(option_e)
if solver.check() == unsat:
    unsat_options.append("E")
    print("Option E is UNSAT (cannot be true)")
else:
    print("Option E is SAT (can be true)")
solver.pop()

# Determine the result
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options cannot be true (all can be true)")