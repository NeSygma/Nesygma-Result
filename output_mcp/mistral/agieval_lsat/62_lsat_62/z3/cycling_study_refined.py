from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare riders and bicycles as Int variables for indexing
# Riders: Reynaldo=0, Seamus=1, Theresa=2, Yuki=3
# Bicycles: F=0, G=1, H=2, J=3

# Day 1 and Day 2 assignments for each rider
# rider_day1[i] = bicycle assigned to rider i on day 1
# rider_day2[i] = bicycle assigned to rider i on day 2
rider_day1 = [Int(f"rider_day1_{i}") for i in range(4)]
rider_day2 = [Int(f"rider_day2_{i}") for i in range(4)]

solver = Solver()

# Helper: All bicycles are distinct per day
solver.add(Distinct(rider_day1))
solver.add(Distinct(rider_day2))

# Constraint 1: Reynaldo (0) cannot test F (0) on either day
solver.add(rider_day1[0] != 0)
solver.add(rider_day2[0] != 0)

# Constraint 2: Yuki (3) cannot test J (3) on either day
solver.add(rider_day1[3] != 3)
solver.add(rider_day2[3] != 3)

# Constraint 3: Theresa (2) must test H (2) on one of the days
solver.add(Or(rider_day1[2] == 2, rider_day2[2] == 2))

# Constraint 4: The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
# Let yuki_day1_bike = rider_day1[3]
# Then rider_day2[1] == yuki_day1_bike
solver.add(rider_day2[1] == rider_day1[3])

# Additional constraint: No rider tests the same bicycle on both days
for i in range(4):
    solver.add(rider_day1[i] != rider_day2[i])

# Now, evaluate each option to find which one is impossible (i.e., leads to unsat when enforced)

# Option A: Reynaldo tests J on the first day
# rider_day1[0] == 3
opt_a_constr = (rider_day1[0] == 3)

# Option B: Reynaldo tests J on the second day
# rider_day2[0] == 3
opt_b_constr = (rider_day2[0] == 3)

# Option C: Seamus tests H on the first day
# rider_day1[1] == 2
opt_c_constr = (rider_day1[1] == 2)

# Option D: Yuki tests H on the first day
# rider_day1[3] == 2
opt_d_constr = (rider_day1[3] == 2)

# Option E: Yuki tests H on the second day
# rider_day2[3] == 2
opt_e_constr = (rider_day2[3] == 2)

# Check which option is impossible (i.e., leads to unsat when enforced)
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The correct answer is the one that is NOT in found_options (i.e., impossible)
# So we invert the logic: the answer is the option that is NOT satisfiable
if len(found_options) == 4:
    # The only option not in found_options is the correct answer
    correct_answer = ["A", "B", "C", "D", "E"]
    for opt in correct_answer:
        if opt not in found_options:
            print("STATUS: sat")
            print(f"answer:{opt}")
            break
    else:
        print("STATUS: unsat")
        print("Refine: No unique answer found")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")