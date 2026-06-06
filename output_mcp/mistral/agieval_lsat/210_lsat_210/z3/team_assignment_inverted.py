from z3 import *

# Create solver
solver = Solver()

# Students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team assignment: 0 = green, 1 = red
team = {s: Int(f"team_{s}") for s in students}

# Facilitator assignment: True if student is facilitator
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Base constraints

# 1. Lateefah is assigned to the green team
solver.add(team["Lateefah"] == 0)

# 2. Kelly is not a facilitator
solver.add(facilitator["Kelly"] == False)

# 3. Olga is a facilitator
solver.add(facilitator["Olga"] == True)

# 4. Juana is assigned to a different team than Olga
solver.add(team["Juana"] != team["Olga"])

# Team size constraints:
# One team has 2 members, the other has 3 members
# Count number of students on green team
green_count = Sum([team[s] == 0 for s in students])
# Count number of students on red team
red_count = Sum([team[s] == 1 for s in students])
# One team has 2, the other has 3
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
# For green team: exactly one student with team==0 and facilitator==True
solver.add(Sum([If(And(team[s] == 0, facilitator[s]), 1, 0) for s in students]) == 1)

# For red team: exactly one student with team==1 and facilitator==True
solver.add(Sum([If(And(team[s] == 1, facilitator[s]), 1, 0) for s in students]) == 1)

# Now evaluate each multiple choice option
# We need to check which option MUST be false (i.e., is unsat)

# Option A: Lateefah is a facilitator, and she is assigned to the same team as Kelly
opt_a_constr = And(
    facilitator["Lateefah"],
    team["Lateefah"] == team["Kelly"]
)

# Option B: Mei is a facilitator, and she is assigned to the same team as Kelly
opt_b_constr = And(
    facilitator["Mei"],
    team["Mei"] == team["Kelly"]
)

# Option C: Olga is a facilitator, and she is assigned to the same team as Mei
opt_c_constr = And(
    facilitator["Olga"],  # Already true from base constraints
    team["Olga"] == team["Mei"]
)

# Option D: Lateefah is a facilitator, and she is assigned to a different team than Juana
opt_d_constr = And(
    facilitator["Lateefah"],
    team["Lateefah"] != team["Juana"]
)

# Option E: Mei is a facilitator, and she is assigned to a different team than Olga
opt_e_constr = And(
    facilitator["Mei"],
    team["Mei"] != team["Olga"]
)

# Test each option for unsatisfiability (must be false)
unsat_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

# Determine result
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be false")