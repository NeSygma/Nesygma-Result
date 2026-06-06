from z3 import *

# Base constraints for the problem
solver = Solver()

# Riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Day 1 and Day 2 assignments
# We represent assignments as dictionaries: {rider: bicycle}
day1 = {r: Int(f"day1_{r}") for r in riders}
day2 = {r: Int(f"day2_{r}") for r in riders}

# Each rider is assigned a unique bicycle each day
solver.add(Distinct(list(day1.values())))
solver.add(Distinct(list(day2.values())))

# All bicycles are tested each day (implied by Distinct and 4 riders/bicycles)

# Constraints:
# 1. Reynaldo cannot test F
solver.add(day1["Reynaldo"] != 0)  # Assuming F=0, G=1, H=2, J=3
solver.add(day2["Reynaldo"] != 0)

# 2. Yuki cannot test J
solver.add(day1["Yuki"] != 3)  # J=3
solver.add(day2["Yuki"] != 3)

# 3. Theresa must be one of the testers for H
solver.add(Or(day1["Theresa"] == 2, day2["Theresa"] == 2))  # H=2

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(day2["Seamus"] == day1["Yuki"])

# Helper function to convert bicycle names to indices
# F=0, G=1, H=2, J=3
def get_bike_index(bike):
    return {"F": 0, "G": 1, "H": 2, "J": 3}[bike]

# Helper function to convert index to bicycle name
def get_bike_name(idx):
    return {0: "F", 1: "G", 2: "H", 3: "J"}[idx]

# Helper function to convert rider index to name
def get_rider_name(idx):
    return riders[idx]

# Define the options as constraints
options = []

# Option A: F: Seamus, Reynaldo; G: Yuki, Seamus; H: Theresa, Yuki; J: Reynaldo, Theresa
# Day1: F=Seamus, G=Yuki, H=Theresa, J=Reynaldo
# Day2: F=Reynaldo, G=Seamus, H=Yuki, J=Theresa
opt_a_constr = And(
    day1["Seamus"] == 0, day1["Yuki"] == 1, day1["Theresa"] == 2, day1["Reynaldo"] == 3,
    day2["Reynaldo"] == 0, day2["Seamus"] == 1, day2["Yuki"] == 2, day2["Theresa"] == 3
)

# Option B: F: Seamus, Yuki; G: Reynaldo, Theresa; H: Yuki, Seamus; J: Theresa, Reynaldo
# Day1: F=Seamus, G=Reynaldo, H=Yuki, J=Theresa
# Day2: F=Yuki, G=Theresa, H=Seamus, J=Reynaldo
opt_b_constr = And(
    day1["Seamus"] == 0, day1["Reynaldo"] == 1, day1["Yuki"] == 2, day1["Theresa"] == 3,
    day2["Yuki"] == 0, day2["Theresa"] == 1, day2["Seamus"] == 2, day2["Reynaldo"] == 3
)

# Option C: F: Yuki, Seamus; G: Seamus, Reynaldo; H: Theresa, Yuki; J: Reynaldo, Theresa
# Day1: F=Yuki, G=Seamus, H=Theresa, J=Reynaldo
# Day2: F=Seamus, G=Reynaldo, H=Yuki, J=Theresa
opt_c_constr = And(
    day1["Yuki"] == 0, day1["Seamus"] == 1, day1["Theresa"] == 2, day1["Reynaldo"] == 3,
    day2["Seamus"] == 0, day2["Reynaldo"] == 1, day2["Yuki"] == 2, day2["Theresa"] == 3
)

# Option D: F: Yuki, Seamus; G: Theresa, Reynaldo; H: Reynaldo, Theresa; J: Seamus, Yuki
# Day1: F=Yuki, G=Theresa, H=Reynaldo, J=Seamus
# Day2: F=Seamus, G=Reynaldo, H=Theresa, J=Yuki
opt_d_constr = And(
    day1["Yuki"] == 0, day1["Theresa"] == 1, day1["Reynaldo"] == 2, day1["Seamus"] == 3,
    day2["Seamus"] == 0, day2["Reynaldo"] == 1, day2["Theresa"] == 2, day2["Yuki"] == 3
)

# Option E: F: Yuki, Theresa; G: Seamus, Yuki; H: Theresa, Reynaldo; J: Reynaldo, Seamus
# Day1: F=Yuki, G=Seamus, H=Theresa, J=Reynaldo
# Day2: F=Theresa, G=Yuki, H=Reynaldo, J=Seamus
opt_e_constr = And(
    day1["Yuki"] == 0, day1["Seamus"] == 1, day1["Theresa"] == 2, day1["Reynaldo"] == 3,
    day2["Theresa"] == 0, day2["Yuki"] == 1, day2["Reynaldo"] == 2, day2["Seamus"] == 3
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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