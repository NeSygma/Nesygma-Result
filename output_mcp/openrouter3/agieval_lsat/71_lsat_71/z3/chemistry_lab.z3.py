from z3 import *

# Problem analysis:
# - 6 lab sessions over 3 days (Wed, Thu, Fri)
# - Each day has 1 morning and 1 afternoon session
# - 6 lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
# - Constraints:
#   1. Kevin and Rebecca must lead sessions on the same day
#   2. Lan and Olivia cannot lead sessions on the same day
#   3. Nessa must lead an afternoon session
#   4. Julio's session must meet on an earlier day than Olivia's

# We'll model this using arrays for morning and afternoon sessions for each day
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Sessions: 0=morning, 1=afternoon

# Create symbolic variables for each session
# Each variable represents which assistant is assigned to that session
days = ["Wednesday", "Thursday", "Friday"]
sessions = ["morning", "afternoon"]

# Create a 3x2 array of assistant variables
# We'll use integers to represent assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Create variables: assign[day][session] = assistant index
assign = [[Int(f"assign_{day}_{session}") for session in range(2)] for day in range(3)]

solver = Solver()

# Base constraints:
# 1. Each assistant is used exactly once (all different)
all_assignments = [assign[day][session] for day in range(3) for session in range(2)]
solver.add(Distinct(all_assignments))

# 2. Each assistant must be in range 0-5
for day in range(3):
    for session in range(2):
        solver.add(assign[day][session] >= 0)
        solver.add(assign[day][session] <= 5)

# 3. Kevin and Rebecca must lead sessions on the same day
# Find which day Kevin is assigned to, and ensure Rebecca is on the same day
# We'll use a helper: for each day, check if Kevin is there, then Rebecca must be there too
for day in range(3):
    # Kevin is assistant index 1, Rebecca is index 5
    # If Kevin is in morning or afternoon of this day, Rebecca must be in the other session of same day
    solver.add(Or(
        # Kevin not on this day, or Rebecca on this day
        And(assign[day][0] != 1, assign[day][1] != 1),  # Kevin not here
        Or(assign[day][0] == 5, assign[day][1] == 5)    # Rebecca here
    ))

# Alternative approach: ensure Kevin and Rebecca are on same day
# We'll create a constraint that for each day, if Kevin is there, Rebecca is there, and vice versa
# Actually, simpler: ensure they are assigned to the same day index
# We need to find which day each is assigned to
# Let's create day variables for Kevin and Rebecca
kevin_day = Int('kevin_day')
rebecca_day = Int('rebecca_day')
solver.add(kevin_day >= 0, kevin_day <= 2)
solver.add(rebecca_day >= 0, rebecca_day <= 2)
solver.add(kevin_day == rebecca_day)

# Link Kevin and Rebecca to their day variables
for day in range(3):
    for session in range(2):
        solver.add(Implies(assign[day][session] == 1, kevin_day == day))
        solver.add(Implies(assign[day][session] == 5, rebecca_day == day))

# 4. Lan and Olivia cannot lead sessions on the same day
# Similar approach: create day variables for Lan and Olivia
lan_day = Int('lan_day')
olivia_day = Int('olivia_day')
solver.add(lan_day >= 0, lan_day <= 2)
solver.add(olivia_day >= 0, olivia_day <= 2)
solver.add(lan_day != olivia_day)

# Link Lan and Olivia to their day variables
for day in range(3):
    for session in range(2):
        solver.add(Implies(assign[day][session] == 2, lan_day == day))
        solver.add(Implies(assign[day][session] == 4, olivia_day == day))

# 5. Nessa must lead an afternoon session
# Nessa is assistant index 3
solver.add(Or(
    assign[0][1] == 3,  # Wednesday afternoon
    assign[1][1] == 3,  # Thursday afternoon
    assign[2][1] == 3   # Friday afternoon
))

# 6. Julio's session must meet on an earlier day than Olivia's
# Julio is index 0, Olivia is index 4
julio_day = Int('julio_day')
solver.add(julio_day >= 0, julio_day <= 2)
solver.add(julio_day < olivia_day)

# Link Julio to his day variable
for day in range(3):
    for session in range(2):
        solver.add(Implies(assign[day][session] == 0, julio_day == day))

# Now evaluate each answer choice
# Each choice gives a specific assignment for morning and afternoon on each day
# We need to check which choice satisfies all constraints

# Define the options as constraints
# Format: (letter, constraint_string)
# We'll create constraints that enforce the specific assignment in each option

options = []

# Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
# This means: Wed morning=Rebecca(5), Wed afternoon=Kevin(1); Thu morning=Julio(0), Thu afternoon=Lan(2); Fri morning=Nessa(3), Fri afternoon=Olivia(4)
opt_a = And(
    assign[0][0] == 5, assign[0][1] == 1,  # Wednesday
    assign[1][0] == 0, assign[1][1] == 2,  # Thursday
    assign[2][0] == 3, assign[2][1] == 4   # Friday
)
options.append(("A", opt_a))

# Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
opt_b = And(
    assign[0][0] == 4, assign[0][1] == 3,  # Wednesday
    assign[1][0] == 0, assign[1][1] == 2,  # Thursday
    assign[2][0] == 1, assign[2][1] == 5   # Friday
)
options.append(("B", opt_b))

# Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
opt_c = And(
    assign[0][0] == 2, assign[0][1] == 1,  # Wednesday
    assign[1][0] == 5, assign[1][1] == 0,  # Thursday
    assign[2][0] == 4, assign[2][1] == 3   # Friday
)
options.append(("C", opt_c))

# Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
opt_d = And(
    assign[0][0] == 1, assign[0][1] == 5,  # Wednesday
    assign[1][0] == 0, assign[1][1] == 3,  # Thursday
    assign[2][0] == 4, assign[2][1] == 2   # Friday
)
options.append(("D", opt_d))

# Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
opt_e = And(
    assign[0][0] == 0, assign[0][1] == 2,  # Wednesday
    assign[1][0] == 4, assign[1][1] == 3,  # Thursday
    assign[2][0] == 5, assign[2][1] == 1   # Friday
)
options.append(("E", opt_e))

# Now test each option
found_options = []
for letter, constr in options:
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