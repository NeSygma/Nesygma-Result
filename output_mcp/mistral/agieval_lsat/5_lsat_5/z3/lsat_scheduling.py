from z3 import *

# Define students as constants for clarity
George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert = Ints('George Helen Irving Kyle Lenore Nina Olivia Robert')
students = [George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert]

# Create a solver
solver = Solver()

# Helper: All students are distinct and represent the 8 individuals
solver.add(Distinct(students))

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Slots: 0=Morning, 1=Afternoon
morning = [Int(f'morning_{i}') for i in range(3)]
afternoon = [Int(f'afternoon_{i}') for i in range(3)]

# Each morning/afternoon assignment is one of the students
for i in range(3):
    solver.add(Or([morning[i] == s for s in students]))
    solver.add(Or([afternoon[i] == s for s in students]))

# Exactly 6 distinct students give reports (6 reports total)
all_reports = [morning[0], morning[1], morning[2], afternoon[0], afternoon[1], afternoon[2]]
solver.add(Distinct(all_reports))

# Constraint 1: Tuesday is the only day George can give a report
# George can only be on Tuesday (day 1)
solver.add(Or([morning[1] == George, afternoon[1] == George]))
# George cannot be on Monday or Wednesday
solver.add(morning[0] != George)
# solver.add(afternoon[0] != George)  # Not explicitly stated, but "only Tuesday" implies George cannot be on Monday or Wednesday at all
solver.add(morning[2] != George)
solver.add(afternoon[2] != George)

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
for i in range(3):
    solver.add(afternoon[i] != Olivia)
    solver.add(afternoon[i] != Robert)

# Constraint 3: Nina constraint
# If Nina gives a report on day d, then on day d+1 (if exists), both Helen and Irving must give reports
# We'll encode this as: for each day d, if Nina is in morning[d] or afternoon[d], then both Helen and Irving must be in {morning[d+1], afternoon[d+1]}
for d in range(2):  # Only for days 0 and 1 (since day 2 has no next day)
    # Nina is on day d in either slot
    nina_on_day_d = Or(morning[d] == Nina, afternoon[d] == Nina)
    # Both Helen and Irving must be on day d+1 in either slot
    helen_on_next_day = Or(morning[d+1] == Helen, afternoon[d+1] == Helen)
    irving_on_next_day = Or(morning[d+1] == Irving, afternoon[d+1] == Irving)
    solver.add(Implies(nina_on_day_d, And(helen_on_next_day, irving_on_next_day)))

# Given scenario: Kyle gives the afternoon report on Tuesday, and Helen gives the afternoon report on Wednesday
solver.add(afternoon[1] == Kyle)
solver.add(afternoon[2] == Helen)

# Now evaluate the multiple choice options for morning reports
# Options are:
# (A) Irving, Lenore, and Nina
# (B) Lenore, George, and Irving
# (C) Nina, Irving, and Lenore
# (D) Robert, George, and Irving
# (E) Robert, Irving, and Lenore

# Map student names to variables for option constraints
option_constraints = {
    "A": And(
        morning[0] == Irving,
        morning[1] == Lenore,
        morning[2] == Nina
    ),
    "B": And(
        morning[0] == Lenore,
        morning[1] == George,
        morning[2] == Irving
    ),
    "C": And(
        morning[0] == Nina,
        morning[1] == Irving,
        morning[2] == Lenore
    ),
    "D": And(
        morning[0] == Robert,
        morning[1] == George,
        morning[2] == Irving
    ),
    "E": And(
        morning[0] == Robert,
        morning[1] == Irving,
        morning[2] == Lenore
    )
}

found_options = []
for letter, constr in option_constraints.items():
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