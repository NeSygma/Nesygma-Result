from z3 import *

solver = Solver()

# Declare entities and teams
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
teams = ["green", "red"]

# Assignments: student -> team (use Int to represent team assignments)
assignment = {s: Int(f"team_{s}") for s in students}

# Facilitator: student -> Bool (True if facilitator)
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Base constraints
# 1. Lateefah is assigned to the green team
# Represent teams as integers: 0 for green, 1 for red
solver.add(assignment["Lateefah"] == 0)

# 2. Juana is assigned to a different team than Olga
solver.add(assignment["Juana"] != assignment["Olga"])

# 3. Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# 4. Olga is a facilitator
solver.add(facilitator["Olga"])

# 5. Team sizes: one team has 2 members, the other has 3
# Count team sizes
team_counts = {t: Sum([If(assignment[s] == t, 1, 0) for s in students]) for t in [0, 1]}
solver.add(Or(
    And(team_counts[0] == 2, team_counts[1] == 3),
    And(team_counts[0] == 3, team_counts[1] == 2)
))

# 6. Exactly one facilitator per team
# For each team, count facilitators
facilitator_counts = {t: Sum([If(And(assignment[s] == t, facilitator[s]), 1, 0) for s in students]) for t in [0, 1]}
solver.add(And(facilitator_counts[0] == 1, facilitator_counts[1] == 1))

# Evaluate each option to determine which must be false
# We will check each option to see if it is possible under the constraints.
# If an option is possible (sat), it cannot be the answer (since we want the one that must be false).
# If an option is impossible (unsat), it is a candidate for the answer.

# Define the options as constraints
# Option A: Lateefah is a facilitator, and she is assigned to the same team as Kelly
opt_a_constr = And(
    facilitator["Lateefah"],
    assignment["Lateefah"] == assignment["Kelly"]
)

# Option B: Mei is a facilitator, and she is assigned to the same team as Kelly
opt_b_constr = And(
    facilitator["Mei"],
    assignment["Mei"] == assignment["Kelly"]
)

# Option C: Olga is a facilitator, and she is assigned to the same team as Mei
opt_c_constr = And(
    facilitator["Olga"],  # Already true from base constraints
    assignment["Olga"] == assignment["Mei"]
)

# Option D: Lateefah is a facilitator, and she is assigned to a different team than Juana
opt_d_constr = And(
    facilitator["Lateefah"],
    assignment["Lateefah"] != assignment["Juana"]
)

# Option E: Mei is a facilitator, and she is assigned to a different team than Olga
opt_e_constr = And(
    facilitator["Mei"],
    assignment["Mei"] != assignment["Olga"]
)

# Test each option
found_options = []
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