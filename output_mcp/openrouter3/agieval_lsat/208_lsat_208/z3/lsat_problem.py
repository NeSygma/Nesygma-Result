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
# For each team, exactly one facilitator
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
# Answer choices specify exact team compositions and facilitators
# We'll encode each choice as constraints and check consistency

found_options = []

# Helper function to encode an answer choice
def encode_choice(green_members, green_fac, red_members, red_fac):
    constraints = []
    # Reset all assignments (we'll add specific ones)
    # For each student, set team and facilitator based on choice
    for s in students:
        if s in green_members:
            constraints.append(team[student_to_idx[s]] == 0)
        elif s in red_members:
            constraints.append(team[student_to_idx[s]] == 1)
        else:
            # Student not in either team - invalid
            return False  # This choice is invalid
    
    # Set facilitators
    constraints.append(facilitator[student_to_idx[green_fac]] == True)
    constraints.append(facilitator[student_to_idx[red_fac]] == True)
    
    # Ensure only these facilitators are set (others are False)
    for s in students:
        if s != green_fac and s != red_fac:
            constraints.append(Not(facilitator[student_to_idx[s]]))
    
    return constraints

# Define each answer choice
choices = [
    # (A) green team: Juana, Lateefah, Olga (facilitator) red team: Kelly, Mei (facilitator)
    ("A", ["Juana", "Lateefah", "Olga"], "Olga", ["Kelly", "Mei"], "Mei"),
    # (B) green team: Kelly, Lateefah (facilitator), Olga red team: Juana, Mei (facilitator)
    ("B", ["Kelly", "Lateefah", "Olga"], "Lateefah", ["Juana", "Mei"], "Mei"),
    # (C) green team: Kelly, Lateefah, Olga (facilitator) red team: Juana (facilitator), Mei
    ("C", ["Kelly", "Lateefah", "Olga"], "Olga", ["Juana", "Mei"], "Juana"),
    # (D) green team: Kelly, Mei, Olga (facilitator) red team: Juana (facilitator), Lateefah
    ("D", ["Kelly", "Mei", "Olga"], "Olga", ["Juana", "Lateefah"], "Juana"),
    # (E) green team: Lateefah, Olga (facilitator) red team: Juana, Kelly (facilitator), Mei
    ("E", ["Lateefah", "Olga"], "Olga", ["Juana", "Kelly", "Mei"], "Juana"),
]

for letter, green_members, green_fac, red_members, red_fac in choices:
    solver.push()
    # Add the specific constraints for this choice
    choice_constraints = encode_choice(green_members, green_fac, red_members, red_fac)
    if choice_constraints:
        solver.add(choice_constraints)
        if solver.check() == sat:
            found_options.append(letter)
    solver.pop()

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