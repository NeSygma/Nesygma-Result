from z3 import *

# Define students as constants for clarity
JUANA = 0
KELLY = 1
LATEEFAH = 2
MEI = 3
OLGA = 4

# Create solver
solver = Solver()

# Decision variables
# team[i] = 0 means student i is on green team, 1 means red team
team = [Int(f"team_{i}") for i in range(5)]

# facilitator[t] = which student is facilitator of team t (t=0 for green, t=1 for red)
facilitator = [Int(f"facilitator_{t}") for t in range(2)]

# Base constraints

# 1. Lateefah is on green team
solver.add(team[LATEEFAH] == 0)

# 2. Kelly is not a facilitator (cannot be facilitator of green or red team)
solver.add(facilitator[0] != KELLY)
solver.add(facilitator[1] != KELLY)

# 3. Olga is a facilitator
# Olga must be facilitator of her team
# Use Or-Loop pattern to avoid symbolic indexing
for t in range(2):
    solver.add(Or(
        And(facilitator[t] == JUANA, team[JUANA] == t),
        And(facilitator[t] == KELLY, team[KELLY] == t),
        And(facilitator[t] == LATEEFAH, team[LATEEFAH] == t),
        And(facilitator[t] == MEI, team[MEI] == t),
        And(facilitator[t] == OLGA, team[OLGA] == t)
    ))

# 4. Lateefah is a facilitator (additional condition for the question)
# Lateefah must be facilitator of her team
for t in range(2):
    solver.add(Or(
        And(facilitator[t] == LATEEFAH, team[LATEEFAH] == t),
    ))

# 5. Team sizes: one team has 2 members, the other has 3
# Count students on green team
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])

# One team has 2, the other has 3
solver.add(Or(
    And(green_count == 2, red_count == 3),
    And(green_count == 3, red_count == 2)
))

# 6. Juana and Olga are on different teams
solver.add(team[JUANA] != team[OLGA])

# Now test each option
found_options = []

# Option A: Juana and Kelly are both assigned to the red team
solver.push()
solver.add(team[JUANA] == 1)
solver.add(team[KELLY] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Juana and Mei are both assigned to the red team
solver.push()
solver.add(team[JUANA] == 1)
solver.add(team[MEI] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Lateefah and Olga are both assigned to the green team
solver.push()
solver.add(team[LATEEFAH] == 0)
solver.add(team[OLGA] == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Mei and Olga are both assigned to the green team
solver.push()
solver.add(team[MEI] == 0)
solver.add(team[OLGA] == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Mei and Olga are both assigned to the red team
solver.push()
solver.add(team[MEI] == 1)
solver.add(team[OLGA] == 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")