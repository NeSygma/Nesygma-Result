from z3 import *

# Create solver
solver = Solver()

# Define students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
student_to_idx = {s: i for i, s in enumerate(students)}

# Team assignment: 0 = Green, 1 = Red
team = [Int(f"team_{s}") for s in students]

# Facilitator status
facilitator = [Bool(f"fac_{s}") for s in students]

# Base constraints
# 1. Team assignments are 0 or 1
for t in team:
    solver.add(Or(t == 0, t == 1))

# 2. One team has 2 members, the other has 3 members
team0_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
team1_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(
    And(team0_count == 2, team1_count == 3),
    And(team0_count == 3, team1_count == 2)
))

# 3. One facilitator per team
for team_val in [0, 1]:
    facilitator_count = Sum([If(And(team[i] == team_val, facilitator[i]), 1, 0) for i in range(5)])
    solver.add(facilitator_count == 1)

# 4. Juana is assigned to a different team than Olga
solver.add(team[student_to_idx["Juana"]] != team[student_to_idx["Olga"]])

# 5. Lateefah is assigned to the green team (team 0)
solver.add(team[student_to_idx["Lateefah"]] == 0)

# 6. Kelly is not a facilitator
solver.add(Not(facilitator[student_to_idx["Kelly"]]))

# 7. Olga is a facilitator
solver.add(facilitator[student_to_idx["Olga"]])

# Now evaluate each answer choice
# We'll create a separate solver for each choice to avoid interference

found_options = []

# Define each answer choice with exact team compositions and facilitators
choices = [
    # (A) green team: Juana, Lateefah, Olga (facilitator) red team: Kelly, Mei (facilitator)
    ("A", {"green": ["Juana", "Lateefah", "Olga"], "green_fac": "Olga", 
           "red": ["Kelly", "Mei"], "red_fac": "Mei"}),
    # (B) green team: Kelly, Lateefah (facilitator), Olga red team: Juana, Mei (facilitator)
    ("B", {"green": ["Kelly", "Lateefah", "Olga"], "green_fac": "Lateefah", 
           "red": ["Juana", "Mei"], "red_fac": "Mei"}),
    # (C) green team: Kelly, Lateefah, Olga (facilitator) red team: Juana (facilitator), Mei
    ("C", {"green": ["Kelly", "Lateefah", "Olga"], "green_fac": "Olga", 
           "red": ["Juana", "Mei"], "red_fac": "Juana"}),
    # (D) green team: Kelly, Mei, Olga (facilitator) red team: Juana (facilitator), Lateefah
    ("D", {"green": ["Kelly", "Mei", "Olga"], "green_fac": "Olga", 
           "red": ["Juana", "Lateefah"], "red_fac": "Juana"}),
    # (E) green team: Lateefah, Olga (facilitator) red team: Juana, Kelly (facilitator), Mei
    ("E", {"green": ["Lateefah", "Olga"], "green_fac": "Olga", 
           "red": ["Juana", "Kelly", "Mei"], "red_fac": "Juana"}),
]

for letter, choice in choices:
    # Create a new solver for each choice
    choice_solver = Solver()
    
    # Add all base constraints to this solver
    for t in team:
        choice_solver.add(Or(t == 0, t == 1))
    
    # Add team size constraints
    team0_count_choice = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
    team1_count_choice = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
    choice_solver.add(Or(
        And(team0_count_choice == 2, team1_count_choice == 3),
        And(team0_count_choice == 3, team1_count_choice == 2)
    ))
    
    # Add facilitator constraints
    for team_val in [0, 1]:
        facilitator_count = Sum([If(And(team[i] == team_val, facilitator[i]), 1, 0) for i in range(5)])
        choice_solver.add(facilitator_count == 1)
    
    # Add other base constraints
    choice_solver.add(team[student_to_idx["Juana"]] != team[student_to_idx["Olga"]])
    choice_solver.add(team[student_to_idx["Lateefah"]] == 0)
    choice_solver.add(Not(facilitator[student_to_idx["Kelly"]]))
    choice_solver.add(facilitator[student_to_idx["Olga"]])
    
    # Add choice-specific constraints
    # Set team assignments
    for s in choice["green"]:
        choice_solver.add(team[student_to_idx[s]] == 0)
    for s in choice["red"]:
        choice_solver.add(team[student_to_idx[s]] == 1)
    
    # Set facilitators
    choice_solver.add(facilitator[student_to_idx[choice["green_fac"]]] == True)
    choice_solver.add(facilitator[student_to_idx[choice["red_fac"]]] == True)
    
    # Ensure only these facilitators are set (others are False)
    for s in students:
        if s != choice["green_fac"] and s != choice["red_fac"]:
            choice_solver.add(Not(facilitator[student_to_idx[s]]))
    
    # Check if this choice is consistent
    if choice_solver.check() == sat:
        found_options.append(letter)

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")