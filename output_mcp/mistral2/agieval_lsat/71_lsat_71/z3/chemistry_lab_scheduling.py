from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Base constraints
solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=Morning, 1=Afternoon
# Sessions: 6 total, indexed 0 to 5
# Session order: Wed Morning, Wed Afternoon, Thu Morning, Thu Afternoon, Fri Morning, Fri Afternoon

# Assign a lab assistant to each session
# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
assignment = [Int(f'assignment_{i}') for i in range(6)]

# Each assistant is assigned to exactly one session
solver.add(Distinct(assignment))

# Helper function to get day from session index
# Day = session index // 2
# Time = session index % 2

def get_day(session_idx):
    return session_idx / 2

# Constraint 1: Kevin (1) and Rebecca (5) must be on the same day
# Use Or-loop to avoid indexing with symbolic variables
solver.add(Or(
    And(
        get_day(1) == get_day(5),
        assignment[1] == 1,
        assignment[5] == 5
    ),
    And(
        get_day(1) == get_day(5),
        assignment[1] == 5,
        assignment[5] == 1
    )
))

# Constraint 2: Lan (2) and Olivia (4) cannot be on the same day
solver.add(get_day(2) != get_day(4))

# Constraint 3: Nessa (3) must be in an afternoon session (time=1)
solver.add(assignment[3] == 3)

# Constraint 4: Julio's (0) session must be on an earlier day than Olivia's (4)
solver.add(get_day(0) < get_day(4))

# Now evaluate each option
options = {
    "A": [
        (0, 5),  # Wed Morning: Rebecca (5)
        (1, 1),  # Wed Afternoon: Kevin (1)
        (2, 0),  # Thu Morning: Julio (0)
        (3, 2),  # Thu Afternoon: Lan (2)
        (4, 3),  # Fri Morning: Nessa (3)
        (5, 4)   # Fri Afternoon: Olivia (4)
    ],
    "B": [
        (0, 4),  # Wed Morning: Olivia (4)
        (1, 3),  # Wed Afternoon: Nessa (3)
        (2, 0),  # Thu Morning: Julio (0)
        (3, 2),  # Thu Afternoon: Lan (2)
        (4, 1),  # Fri Morning: Kevin (1)
        (5, 5)   # Fri Afternoon: Rebecca (5)
    ],
    "C": [
        (0, 2),  # Wed Morning: Lan (2)
        (1, 1),  # Wed Afternoon: Kevin (1)
        (2, 5),  # Thu Morning: Rebecca (5)
        (3, 0),  # Thu Afternoon: Julio (0)
        (4, 4),  # Fri Morning: Olivia (4)
        (5, 3)   # Fri Afternoon: Nessa (3)
    ],
    "D": [
        (0, 1),  # Wed Morning: Kevin (1)
        (1, 5),  # Wed Afternoon: Rebecca (5)
        (2, 0),  # Thu Morning: Julio (0)
        (3, 3),  # Thu Afternoon: Nessa (3)
        (4, 4),  # Fri Morning: Olivia (4)
        (5, 2)   # Fri Afternoon: Lan (2)
    ],
    "E": [
        (0, 0),  # Wed Morning: Julio (0)
        (1, 2),  # Wed Afternoon: Lan (2)
        (2, 4),  # Thu Morning: Olivia (4)
        (3, 3),  # Thu Afternoon: Nessa (3)
        (4, 5),  # Fri Morning: Rebecca (5)
        (5, 1)   # Fri Afternoon: Kevin (1)
    ]
}

# For each option, check if the assignment satisfies all constraints
found_options = []
for letter, sessions in options.items():
    solver.push()
    # Reset assignment variables to the option's assignments
    for i, assistant in sessions:
        solver.add(assignment[i] == assistant)
    # Check if the constraints are satisfied
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