from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca

# Define the sessions as a list of 6 integers (0-5), representing the lab assistant for each session
# Sessions are ordered as: Wed Morning, Wed Afternoon, Thu Morning, Thu Afternoon, Fri Morning, Fri Afternoon

# Base constraints:
# 1. Each session is assigned to exactly one assistant (0-5)
# 2. Each assistant is assigned to exactly one session
# 3. Kevin (1) and Rebecca (5) must be on the same day
# 4. Lan (2) and Olivia (4) cannot be on the same day
# 5. Nessa (3) must be in an afternoon session
# 6. Julio (0) must be on an earlier day than Olivia (4)

# We will evaluate each option individually to see if it satisfies all constraints

found_options = []

# Helper function to check if an option satisfies all constraints
def check_option(option_name, sessions):
    solver = Solver()
    
    # Assign the sessions
    s = [Int(f"s_{i}") for i in range(6)]
    for i in range(6):
        solver.add(s[i] == sessions[i])
    
    # Constraint 1: Each assistant is assigned to exactly one session
    solver.add(Distinct(s))
    
    # Constraint 2: Kevin (1) and Rebecca (5) must be on the same day
    kevin_day = Int("kevin_day")
    rebecca_day = Int("rebecca_day")
    solver.add(
        Or([
            And(
                s[i] == 1,
                s[j] == 5,
                kevin_day == i // 2,
                rebecca_day == j // 2,
                kevin_day == rebecca_day
            )
            for i in range(6) for j in range(6) if i != j
        ])
    )
    
    # Constraint 3: Lan (2) and Olivia (4) cannot be on the same day
    solver.add(
        Not(Or([
            And(
                s[i] == 2,
                s[j] == 4,
                i // 2 == j // 2
            )
            for i in range(6) for j in range(6) if i != j
        ]))
    )
    
    # Constraint 4: Nessa (3) must be in an afternoon session
    solver.add(Or([s[i] == 3 and i % 2 == 1 for i in range(6)]))
    
    # Constraint 5: Julio (0) must be on an earlier day than Olivia (4)
    solver.add(
        Or([
            And(
                s[i] == 0,
                s[j] == 4,
                i // 2 < j // 2
            )
            for i in range(6) for j in range(6) if i != j
        ])
    )
    
    # Check if the option satisfies all constraints
    if solver.check() == sat:
        return True
    else:
        return False

# Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
# Sessions: [5, 1, 0, 2, 3, 4]
opt_a = [5, 1, 0, 2, 3, 4]
if check_option("A", opt_a):
    found_options.append("A")

# Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
# Sessions: [4, 3, 0, 2, 1, 5]
opt_b = [4, 3, 0, 2, 1, 5]
if check_option("B", opt_b):
    found_options.append("B")

# Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
# Sessions: [2, 1, 5, 0, 4, 3]
opt_c = [2, 1, 5, 0, 4, 3]
if check_option("C", opt_c):
    found_options.append("C")

# Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
# Sessions: [1, 5, 0, 3, 4, 2]
opt_d = [1, 5, 0, 3, 4, 2]
if check_option("D", opt_d):
    found_options.append("D")

# Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
# Sessions: [0, 2, 4, 3, 5, 1]
opt_e = [0, 2, 4, 3, 5, 1]
if check_option("E", opt_e):
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