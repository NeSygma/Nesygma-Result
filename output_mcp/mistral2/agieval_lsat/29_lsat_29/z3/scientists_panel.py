from z3 import *

solver = Solver()

# Declare symbolic variables for each scientist (True if selected, False otherwise)
botanists = [Bool('F'), Bool('G'), Bool('H')]
chemists = [Bool('K'), Bool('L'), Bool('M')]
zoologists = [Bool('P'), Bool('Q'), Bool('R')]

# Base constraints:
# 1. Exactly 5 scientists are selected in total
solver.add(Sum(botanists + chemists + zoologists) == 5)

# 2. At least one scientist of each type must be selected
solver.add(Sum(botanists) >= 1)
solver.add(Sum(chemists) >= 1)
solver.add(Sum(zoologists) >= 1)

# 3. If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(Sum(botanists) > 1, Sum(zoologists) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(botanists[0], chemists[0])))

# 5. K and M cannot both be selected
solver.add(Not(And(chemists[0], chemists[2])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(chemists[2], And(zoologists[0], zoologists[2])))

# Additional constraint for the question:
# If both G and H are among the scientists selected, then the panel must include either:
# (A) F or else K
# (B) F or else M
# (C) K or else M
# (D) M or else Q
# (E) P or else Q

# We will test each option under the condition that both G and H are selected.
found_options = []

# Condition: Both G and H are selected
condition = And(botanists[1], botanists[2])

# Define the options as constraints
options = [
    ("A", And(Or(botanists[0], chemists[0]), condition)),
    ("B", And(Or(botanists[0], chemists[2]), condition)),
    ("C", And(Or(chemists[0], chemists[2]), condition)),
    ("D", And(Or(chemists[2], zoologists[1]), condition)),
    ("E", And(Or(zoologists[0], zoologists[1]), condition))
]

for letter, constr in options:
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