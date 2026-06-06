from z3 import *

# Create solver
solver = Solver()

# Define students and teams
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
teams = ["green", "red"]

# Create symbolic variables for team assignment
# 0 = green, 1 = red (or we can use Bool: True for green, False for red)
team = {s: Int(f"team_{s}") for s in students}
for s in students:
    solver.add(Or(team[s] == 0, team[s] == 1))  # 0 = green, 1 = red

# Create symbolic variables for facilitator status
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Constraint: One team has 2 members, the other has 3 members
# Count green team members
green_count = Sum([If(team[s] == 0, 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# Constraint: One member of each team is a facilitator
# For green team: exactly one facilitator
green_facilitators = Sum([If(And(team[s] == 0, facilitator[s]), 1, 0) for s in students])
solver.add(green_facilitators == 1)

# For red team: exactly one facilitator
red_facilitators = Sum([If(And(team[s] == 1, facilitator[s]), 1, 0) for s in students])
solver.add(red_facilitators == 1)

# Constraint: Juana is assigned to a different team than Olga
solver.add(team["Juana"] != team["Olga"])

# Constraint: Lateefah is assigned to the green team
solver.add(team["Lateefah"] == 0)

# Constraint: Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# Constraint: Olga is a facilitator
solver.add(facilitator["Olga"])

# Additional constraint: If Mei is assigned to the green team (this is the premise for the question)
solver.add(team["Mei"] == 0)

# Now evaluate each answer choice
# The question asks: "If Mei is assigned to the green team, then which one of the following must be true?"
# We need to check which of the options is necessarily true given all constraints

# Define the options as constraints that would make the option true
opt_a_constr = team["Juana"] == 0  # Juana is assigned to the green team
opt_b_constr = team["Kelly"] == 1  # Kelly is assigned to the red team
opt_c_constr = team["Olga"] == 0   # Olga is assigned to the green team
opt_d_constr = facilitator["Lateefah"]  # Lateefah is a facilitator
opt_e_constr = facilitator["Mei"]  # Mei is a facilitator

# We need to check which options MUST be true (i.e., are entailed by the constraints)
# For each option, we check if the option is true in ALL models that satisfy the constraints
# This is equivalent to checking if the negation of the option leads to unsat

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    # Create a new solver to check if the option is necessarily true
    s = Solver()
    # Add all base constraints
    for stu in students:
        s.add(Or(team[stu] == 0, team[stu] == 1))
    s.add(Or(green_count == 2, green_count == 3))
    s.add(green_facilitators == 1)
    s.add(red_facilitators == 1)
    s.add(team["Juana"] != team["Olga"])
    s.add(team["Lateefah"] == 0)
    s.add(Not(facilitator["Kelly"]))
    s.add(facilitator["Olga"])
    s.add(team["Mei"] == 0)
    
    # Add the negation of the option
    s.add(Not(constr))
    
    # Check if the negation is satisfiable
    if s.check() == unsat:
        # If negation is unsat, then the option must be true
        found_options.append(letter)

# According to the problem, we should find exactly one option that must be true
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")