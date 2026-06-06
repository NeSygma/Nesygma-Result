from z3 import *

# Declare symbolic variables for each scientist
botanists = [Bool(f) for f in ['F', 'G', 'H']]
chemists = [Bool(f) for f in ['K', 'L', 'M']]
zoologists = [Bool(f) for f in ['P', 'Q', 'R']]

# Base constraints
solver = Solver()

# At least one scientist of each type
solver.add(Or(botanists))
solver.add(Or(chemists))
solver.add(Or(zoologists))

# If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(Sum(botanists) > 1, Sum(zoologists) <= 1))

# F and K cannot both be selected
solver.add(Not(And(botanists[0], chemists[0])))

# K and M cannot both be selected
solver.add(Not(And(chemists[0], chemists[2])))

# If M is selected, both P and R must be selected
solver.add(Implies(chemists[2], And(zoologists[0], zoologists[2])))

# Define the options as constraints
options = {
    "A": And(
        botanists[0], botanists[1], chemists[0], zoologists[0], zoologists[1],
        # Ensure no other scientists are selected
        Sum(botanists) == 2,
        Sum(chemists) == 1,
        Sum(zoologists) == 2
    ),
    "B": And(
        botanists[1], botanists[2], chemists[0], chemists[1], chemists[2],
        # Ensure no other scientists are selected
        Sum(botanists) == 2,
        Sum(chemists) == 3,
        Sum(zoologists) == 0
    ),
    "C": And(
        botanists[1], botanists[2], chemists[0], chemists[1], zoologists[2],
        # Ensure no other scientists are selected
        Sum(botanists) == 2,
        Sum(chemists) == 2,
        Sum(zoologists) == 1
    ),
    "D": And(
        botanists[2], chemists[0], chemists[2], zoologists[0], zoologists[2],
        # Ensure no other scientists are selected
        Sum(botanists) == 1,
        Sum(chemists) == 2,
        Sum(zoologists) == 2
    ),
    "E": And(
        botanists[2], chemists[1], chemists[2], zoologists[0], zoologists[1],
        # Ensure no other scientists are selected
        Sum(botanists) == 1,
        Sum(chemists) == 2,
        Sum(zoologists) == 2
    )
}

# Evaluate each option
found_options = []
for letter, constr in options.items():
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