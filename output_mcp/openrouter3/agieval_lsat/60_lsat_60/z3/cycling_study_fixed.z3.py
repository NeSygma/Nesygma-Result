from z3 import *

# Create solver
solver = Solver()

# Define riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Create symbolic variables for assignments
# For each bicycle, we need to know which rider tests it on day 1 and day 2
# We'll use arrays indexed by bicycle index
bike_to_rider_day1 = [Int(f"bike_{b}_day1") for b in bicycles]
bike_to_rider_day2 = [Int(f"bike_{b}_day2") for b in bicycles]

# Map rider names to indices for easier constraint writing
rider_to_idx = {r: i for i, r in enumerate(riders)}
bike_to_idx = {b: i for i, b in enumerate(bicycles)}

# Base constraints:
# 1. Each rider tests exactly one bicycle per day
# 2. All bicycles are tested each day
# 3. Each rider tests a different bicycle on the two days

# For each day, the mapping from bicycle to rider must be a permutation
# We'll use the constraint that all bike_to_rider_day1 values are distinct
# and all bike_to_rider_day2 values are distinct
solver.add(Distinct(bike_to_rider_day1))
solver.add(Distinct(bike_to_rider_day2))

# Also, each rider must appear exactly once per day
# We can enforce this by ensuring the set of riders for each day is exactly {0,1,2,3}
for day in [bike_to_rider_day1, bike_to_rider_day2]:
    for rider_idx in range(4):
        solver.add(Or([day[b] == rider_idx for b in range(4)]))

# Additional constraints from problem statement:
# 1. Reynaldo cannot test F
# Reynaldo is index 0, F is index 0
solver.add(bike_to_rider_day1[bike_to_idx["F"]] != rider_to_idx["Reynaldo"])
solver.add(bike_to_rider_day2[bike_to_idx["F"]] != rider_to_idx["Reynaldo"])

# 2. Yuki cannot test J
# Yuki is index 3, J is index 3
solver.add(bike_to_rider_day1[bike_to_idx["J"]] != rider_to_idx["Yuki"])
solver.add(bike_to_rider_day2[bike_to_idx["J"]] != rider_to_idx["Yuki"])

# 3. Theresa must be one of the testers for H
# Theresa is index 2, H is index 2
# This means Theresa tests H on either day 1 or day 2 (or both)
solver.add(Or(
    bike_to_rider_day1[bike_to_idx["H"]] == rider_to_idx["Theresa"],
    bike_to_rider_day2[bike_to_idx["H"]] == rider_to_idx["Theresa"]
))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
# We need to find which bicycle Yuki tests on day 1, then ensure Seamus tests that same bicycle on day 2
# Use Or-Loop pattern to avoid indexing with Z3 variable
yuki_day1_bike = Int('yuki_day1_bike')
solver.add(yuki_day1_bike >= 0, yuki_day1_bike < 4)

# Yuki tests this bicycle on day 1
# Use Or-Loop: yuki_day1_bike == i AND bike_to_rider_day1[i] == Yuki for some i
solver.add(Or([And(yuki_day1_bike == i, bike_to_rider_day1[i] == rider_to_idx["Yuki"]) for i in range(4)]))

# Seamus tests the same bicycle on day 2
# Use Or-Loop: yuki_day1_bike == i AND bike_to_rider_day2[i] == Seamus for some i
solver.add(Or([And(yuki_day1_bike == i, bike_to_rider_day2[i] == rider_to_idx["Seamus"]) for i in range(4)]))

# Now, let's define the answer choices as constraints
# Each choice gives the riders for each bicycle in order (day 1, day 2)
# We need to convert these to constraints on our variables

def make_choice_constraint(choice_dict):
    """Convert a choice dictionary to Z3 constraints"""
    constraints = []
    for bike, (rider1, rider2) in choice_dict.items():
        bike_idx = bike_to_idx[bike]
        rider1_idx = rider_to_idx[rider1]
        rider2_idx = rider_to_idx[rider2]
        constraints.append(bike_to_rider_day1[bike_idx] == rider1_idx)
        constraints.append(bike_to_rider_day2[bike_idx] == rider2_idx)
    return And(constraints)

# Define each answer choice
opt_a_constr = make_choice_constraint({
    "F": ("Seamus", "Reynaldo"),
    "G": ("Yuki", "Seamus"),
    "H": ("Theresa", "Yuki"),
    "J": ("Reynaldo", "Theresa")
})

opt_b_constr = make_choice_constraint({
    "F": ("Seamus", "Yuki"),
    "G": ("Reynaldo", "Theresa"),
    "H": ("Yuki", "Seamus"),
    "J": ("Theresa", "Reynaldo")
})

opt_c_constr = make_choice_constraint({
    "F": ("Yuki", "Seamus"),
    "G": ("Seamus", "Reynaldo"),
    "H": ("Theresa", "Yuki"),
    "J": ("Reynaldo", "Theresa")
})

opt_d_constr = make_choice_constraint({
    "F": ("Yuki", "Seamus"),
    "G": ("Theresa", "Reynaldo"),
    "H": ("Reynaldo", "Theresa"),
    "J": ("Seamus", "Yuki")
})

opt_e_constr = make_choice_constraint({
    "F": ("Yuki", "Theresa"),
    "G": ("Seamus", "Yuki"),
    "H": ("Theresa", "Reynaldo"),
    "J": ("Reynaldo", "Seamus")
})

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")