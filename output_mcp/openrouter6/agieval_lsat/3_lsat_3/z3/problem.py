from z3 import *

# Student indices
GEORGE = 0
HELEN = 1
IRVING = 2
KYLE = 3
LENORE = 4
NINA = 5
OLIVIA = 6
ROBERT = 7

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Times: 0=morning, 1=afternoon

# Create slot variables: slot[day][time] = student index
slot = [[Int(f'slot_{d}_{t}') for t in range(2)] for d in range(3)]

# Base constraints
solver_base = Solver()

# Domain constraints: each slot must be a student index 0..7
for d in range(3):
    for t in range(2):
        solver_base.add(slot[d][t] >= 0)
        solver_base.add(slot[d][t] <= 7)

# All slots distinct
all_slots = [slot[d][t] for d in range(3) for t in range(2)]
solver_base.add(Distinct(all_slots))

# George can only give report on Tuesday (day 1)
# So George cannot be on Monday or Wednesday
for d in [0, 2]:
    for t in range(2):
        solver_base.add(slot[d][t] != GEORGE)

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver_base.add(slot[d][1] != OLIVIA)
    solver_base.add(slot[d][1] != ROBERT)

# Nina condition: if Nina gives a report on Monday or Tuesday,
# then the next day both Helen and Irving must give reports.
for d in range(2):  # d = 0 (Monday) or 1 (Tuesday)
    nina_on_d = Or(slot[d][0] == NINA, slot[d][1] == NINA)
    # Next day must have both Helen and Irving (the two slots are exactly Helen and Irving)
    helen_irving_next = Or(
        And(slot[d+1][0] == HELEN, slot[d+1][1] == IRVING),
        And(slot[d+1][0] == IRVING, slot[d+1][1] == HELEN)
    )
    solver_base.add(Implies(nina_on_d, helen_irving_next))

# Function to check if a pair can be together on Monday or Tuesday
def can_be_together_on_mon_tue(pair):
    X, Y = pair
    s = Solver()
    s.add(solver_base.assertions())
    # Constraint: they are together on Monday or Tuesday
    together_mon = Or(
        And(slot[0][0] == X, slot[0][1] == Y),
        And(slot[0][0] == Y, slot[0][1] == X)
    )
    together_tue = Or(
        And(slot[1][0] == X, slot[1][1] == Y),
        And(slot[1][0] == Y, slot[1][1] == X)
    )
    s.add(Or(together_mon, together_tue))
    return s.check() == sat

# Function to check if a pair can be together on Wednesday
def can_be_together_on_wed(pair):
    X, Y = pair
    s = Solver()
    s.add(solver_base.assertions())
    # Constraint: they are together on Wednesday
    together_wed = Or(
        And(slot[2][0] == X, slot[2][1] == Y),
        And(slot[2][0] == Y, slot[2][1] == X)
    )
    s.add(together_wed)
    return s.check() == sat

# Options
options = [
    ("A", (GEORGE, LENORE)),
    ("B", (HELEN, NINA)),
    ("C", (IRVING, ROBERT)),
    ("D", (KYLE, NINA)),
    ("E", (OLIVIA, KYLE))
]

found_options = []
for letter, pair in options:
    # Check if they can be together on Monday or Tuesday
    if can_be_together_on_mon_tue(pair):
        # If yes, then they are not forced to be on Wednesday
        continue
    # If not, check if they can be together on Wednesday
    if can_be_together_on_wed(pair):
        found_options.append(letter)

# Output according to multiple choice skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")