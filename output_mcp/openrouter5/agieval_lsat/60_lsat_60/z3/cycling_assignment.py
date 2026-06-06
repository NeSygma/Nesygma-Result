from z3 import *

# Riders: Reynaldo, Seamus, Theresa, Yuki
# Bicycles: F, G, H, J
# Days: 1 and 2

# We'll model assignments as: for each rider, which bike they test on day 1 and day 2.
# But the answer choices list for each bicycle the riders in order (day1, day2).
# So we need to check consistency.

# Let's encode the problem using variables:
# For each rider r and day d, bike(r, d) is the bicycle they test.
# Domain: 0=F, 1=G, 2=H, 3=J

riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bikes = ["F", "G", "H", "J"]

# Map names to indices
rider_idx = {"Reynaldo": 0, "Seamus": 1, "Theresa": 2, "Yuki": 3}
bike_idx = {"F": 0, "G": 1, "H": 2, "J": 3}

# Create variables: bike[r][d] = Int
bike = [[Int(f"bike_{r}_{d}") for d in range(2)] for r in range(4)]

solver = Solver()

# Domain constraints: each bike variable is 0..3
for r in range(4):
    for d in range(2):
        solver.add(bike[r][d] >= 0, bike[r][d] <= 3)

# Each day, all four bicycles are tested (each rider gets a different bike each day)
for d in range(2):
    solver.add(Distinct([bike[r][d] for r in range(4)]))

# Each rider tests a different bicycle on day 1 and day 2
for r in range(4):
    solver.add(bike[r][0] != bike[r][1])

# Conditions:
# 1. Reynaldo cannot test F.
solver.add(bike[0][0] != 0)  # Reynaldo day1 != F
solver.add(bike[0][1] != 0)  # Reynaldo day2 != F

# 2. Yuki cannot test J.
solver.add(bike[3][0] != 3)  # Yuki day1 != J
solver.add(bike[3][1] != 3)  # Yuki day2 != J

# 3. Theresa must be one of the testers for H.
# Theresa tests H on day1 or day2
solver.add(Or(bike[2][0] == 2, bike[2][1] == 2))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
# bike[3][0] == bike[1][1]
solver.add(bike[3][0] == bike[1][1])

# Now define each option as a constraint.
# Each option gives for each bicycle the riders in order (day1, day2).
# So for option A: F: Seamus, Reynaldo means bike F is tested by Seamus day1, Reynaldo day2.
# That means: bike[Seamus][0] == F and bike[Reynaldo][1] == F.

def make_option_constr(option_dict):
    """option_dict maps bike_letter -> (rider_day1, rider_day2)"""
    constrs = []
    for bike_letter, (r1_name, r2_name) in option_dict.items():
        b = bike_idx[bike_letter]
        r1 = rider_idx[r1_name]
        r2 = rider_idx[r2_name]
        constrs.append(bike[r1][0] == b)
        constrs.append(bike[r2][1] == b)
    return And(constrs)

# Option A
opt_a = {
    "F": ("Seamus", "Reynaldo"),
    "G": ("Yuki", "Seamus"),
    "H": ("Theresa", "Yuki"),
    "J": ("Reynaldo", "Theresa")
}

# Option B
opt_b = {
    "F": ("Seamus", "Yuki"),
    "G": ("Reynaldo", "Theresa"),
    "H": ("Yuki", "Seamus"),
    "J": ("Theresa", "Reynaldo")
}

# Option C
opt_c = {
    "F": ("Yuki", "Seamus"),
    "G": ("Seamus", "Reynaldo"),
    "H": ("Theresa", "Yuki"),
    "J": ("Reynaldo", "Theresa")
}

# Option D
opt_d = {
    "F": ("Yuki", "Seamus"),
    "G": ("Theresa", "Reynaldo"),
    "H": ("Reynaldo", "Theresa"),
    "J": ("Seamus", "Yuki")
}

# Option E
opt_e = {
    "F": ("Yuki", "Theresa"),
    "G": ("Seamus", "Yuki"),
    "H": ("Theresa", "Reynaldo"),
    "J": ("Reynaldo", "Seamus")
}

found_options = []
for letter, constr in [("A", make_option_constr(opt_a)),
                        ("B", make_option_constr(opt_b)),
                        ("C", make_option_constr(opt_c)),
                        ("D", make_option_constr(opt_d)),
                        ("E", make_option_constr(opt_e))]:
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