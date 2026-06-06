from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Declare symbolic variables for each scientist (True if selected, False otherwise)
botanists = [Bool('F'), Bool('G'), Bool('H')]
chemists = [Bool('K'), Bool('L'), Bool('M')]
zoologists = [Bool('P'), Bool('Q'), Bool('R')]

# Base constraints from the problem statement
solver = Solver()

# At least one scientist of each type must be selected
solver.add(Or(botanists))
solver.add(Or(chemists))
solver.add(Or(zoologists))

# If more than one botanist is selected, then at most one zoologist is selected
# We can encode this as: (number of botanists > 1) implies (number of zoologists <= 1)
num_botanists = Sum(botanists)
num_zoologists = Sum(zoologists)
solver.add(Implies(num_botanists > 1, num_zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(botanists[0], chemists[0])))

# K and M cannot both be selected
solver.add(Not(And(chemists[0], chemists[2])))

# If M is selected, both P and R must be selected
solver.add(Implies(chemists[2], And(zoologists[0], zoologists[2])))

# Additional constraint for the question: M is the only chemist selected
solver.add(chemists[2] == True)  # M is selected
solver.add(chemists[0] == False)  # K is not selected
solver.add(chemists[1] == False)  # L is not selected

# Ensure exactly one chemist is selected (M)
solver.add(Sum(chemists) == 1)

# Now, evaluate each option to see which one must be true
found_options = []

# Option A: F and G are both selected
solver.push()
solver.add(And(botanists[0], botanists[1]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: G and H are both selected
solver.push()
solver.add(And(botanists[1], botanists[2]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: H and P are both selected
solver.push()
solver.add(And(botanists[2], zoologists[0]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: F, G, and H are all selected
solver.push()
solver.add(And(botanists[0], botanists[1], botanists[2]))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P, Q, and R are all selected
solver.push()
solver.add(And(zoologists[0], zoologists[1], zoologists[2]))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")