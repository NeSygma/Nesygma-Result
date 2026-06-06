from z3 import *

# Define the days and session types
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Session types: 0=Morning, 1=Afternoon

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca

# Create a solver
solver = Solver()

# Decision variables: Assign each session to an assistant
# Sessions are ordered as: Wed Morning, Wed Afternoon, Thu Morning, Thu Afternoon, Fri Morning, Fri Afternoon
sessions = [Int(f"session_{i}") for i in range(6)]

# Each session is assigned to exactly one assistant (0-5)
for i in range(6):
    solver.add(Or([sessions[i] == a for a in range(6)]))

# Each assistant is assigned to exactly one session
solver.add(Distinct(sessions))

# Helper function to get the day and session type for a session index
def get_day_and_type(session_idx):
    day = session_idx // 2
    session_type = session_idx % 2
    return day, session_type

# Constraints

# 1. Kevin (1) and Rebecca (5) must lead sessions on the same day
# Find the day of Kevin's session and Rebecca's session and ensure they are equal
kevin_day = Int("kevin_day")
rebecca_day = Int("rebecca_day")
solver.add(kevin_day == 0)  # Placeholder, will be constrained below
solver.add(rebecca_day == 0)  # Placeholder, will be constrained below
solver.add(Or([
    And(sessions[i] == 1, kevin_day == get_day_and_type(i)[0],
        sessions[j] == 5, rebecca_day == get_day_and_type(j)[0], kevin_day == rebecca_day)
    for i in range(6) for j in range(6) if i != j
]))

# 2. Lan (2) and Olivia (4) cannot lead sessions on the same day
lan_day = Int("lan_day")
olivia_day = Int("olivia_day")
solver.add(lan_day == 0)  # Placeholder
solver.add(olivia_day == 0)  # Placeholder
solver.add(Or([
    And(sessions[i] == 2, lan_day == get_day_and_type(i)[0],
        sessions[j] == 4, olivia_day == get_day_and_type(j)[0], lan_day != olivia_day)
    for i in range(6) for j in range(6) if i != j
]))

# 3. Nessa (3) must lead an afternoon session
nessa_session = Int("nessa_session")
solver.add(Or([
    And(sessions[i] == 3, get_day_and_type(i)[1] == 1)
    for i in range(6)
]))

# 4. Julio's (0) session must be on an earlier day than Olivia's (4)
julio_day = Int("julio_day")
solver.add(Or([
    And(sessions[i] == 0, julio_day == get_day_and_type(i)[0],
        sessions[j] == 4, olivia_day == get_day_and_type(j)[0], julio_day < olivia_day)
    for i in range(6) for j in range(6) if i != j
]))

# Now evaluate each option
found_options = []

# Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
# Sessions: Wed Morning=Rebecca(5), Wed Afternoon=Kevin(1), Thu Morning=Julio(0), Thu Afternoon=Lan(2), Fri Morning=Nessa(3), Fri Afternoon=Olivia(4)
opt_a_constr = And(
    sessions[0] == 5,  # Wed Morning: Rebecca
    sessions[1] == 1,  # Wed Afternoon: Kevin
    sessions[2] == 0,  # Thu Morning: Julio
    sessions[3] == 2,  # Thu Afternoon: Lan
    sessions[4] == 3,  # Fri Morning: Nessa
    sessions[5] == 4   # Fri Afternoon: Olivia
)

# Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
# Sessions: Wed Morning=Olivia(4), Wed Afternoon=Nessa(3), Thu Morning=Julio(0), Thu Afternoon=Lan(2), Fri Morning=Kevin(1), Fri Afternoon=Rebecca(5)
opt_b_constr = And(
    sessions[0] == 4,  # Wed Morning: Olivia
    sessions[1] == 3,  # Wed Afternoon: Nessa
    sessions[2] == 0,  # Thu Morning: Julio
    sessions[3] == 2,  # Thu Afternoon: Lan
    sessions[4] == 1,  # Fri Morning: Kevin
    sessions[5] == 5   # Fri Afternoon: Rebecca
)

# Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
# Sessions: Wed Morning=Lan(2), Wed Afternoon=Kevin(1), Thu Morning=Rebecca(5), Thu Afternoon=Julio(0), Fri Morning=Olivia(4), Fri Afternoon=Nessa(3)
opt_c_constr = And(
    sessions[0] == 2,  # Wed Morning: Lan
    sessions[1] == 1,  # Wed Afternoon: Kevin
    sessions[2] == 5,  # Thu Morning: Rebecca
    sessions[3] == 0,  # Thu Afternoon: Julio
    sessions[4] == 4,  # Fri Morning: Olivia
    sessions[5] == 3   # Fri Afternoon: Nessa
)

# Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
# Sessions: Wed Morning=Kevin(1), Wed Afternoon=Rebecca(5), Thu Morning=Julio(0), Thu Afternoon=Nessa(3), Fri Morning=Olivia(4), Fri Afternoon=Lan(2)
opt_d_constr = And(
    sessions[0] == 1,  # Wed Morning: Kevin
    sessions[1] == 5,  # Wed Afternoon: Rebecca
    sessions[2] == 0,  # Thu Morning: Julio
    sessions[3] == 3,  # Thu Afternoon: Nessa
    sessions[4] == 4,  # Fri Morning: Olivia
    sessions[5] == 2   # Fri Afternoon: Lan
)

# Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
# Sessions: Wed Morning=Julio(0), Wed Afternoon=Lan(2), Thu Morning=Olivia(4), Thu Afternoon=Nessa(3), Fri Morning=Rebecca(5), Fri Afternoon=Kevin(1)
opt_e_constr = And(
    sessions[0] == 0,  # Wed Morning: Julio
    sessions[1] == 2,  # Wed Afternoon: Lan
    sessions[2] == 4,  # Thu Morning: Olivia
    sessions[3] == 3,  # Thu Afternoon: Nessa
    sessions[4] == 5,  # Fri Morning: Rebecca
    sessions[5] == 1   # Fri Afternoon: Kevin
)

# Evaluate each option
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