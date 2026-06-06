from z3 import *

# BENCHMARK_MODE: ON (model-finding with refinement on unsat)
BENCHMARK_MODE = True

# Declare the houses as symbolic constants
Houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']

# Positions: 0=1st, 1=2nd, 2=3rd, 3=4th, 4=5th, 5=6th, 6=7th
# Morning: 0,1; Afternoon: 2,3,4; Evening: 5,6

# Create a solver
solver = Solver()

# Assign each house to a unique position
position = {h: Int(f'pos_{h}') for h in Houses}

# All positions are distinct
solver.add(Distinct(list(position.values())))

# Position bounds: 0 to 6
for h in Houses:
    solver.add(position[h] >= 0, position[h] <= 6)

# Rule 1: J must be shown in the evening (positions 5 or 6)
solver.add(Or(position['J'] == 5, position['J'] == 6))

# Rule 2: K cannot be shown in the morning (positions 0 or 1)
solver.add(Not(Or(position['K'] == 0, position['K'] == 1)))

# Rule 3: L must be shown after K and before M (K < L < M)
solver.add(position['K'] < position['L'])
solver.add(position['L'] < position['M'])

# Given: P is shown in the afternoon (positions 2, 3, or 4)
solver.add(Or(position['P'] == 2, position['P'] == 3, position['P'] == 4))

# Now evaluate each option under the given constraints
found_options = []

# Option A: J is shown seventh (position 6)
solver.push()
solver.add(position['J'] == 6)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: K is shown third (position 2)
solver.push()
solver.add(position['K'] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: N is shown first (position 0)
solver.push()
solver.add(position['N'] == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: M is shown in the afternoon (positions 2, 3, or 4)
solver.push()
solver.add(Or(position['M'] == 2, position['M'] == 3, position['M'] == 4))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: O is shown in the morning (positions 0 or 1)
solver.push()
solver.add(Or(position['O'] == 0, position['O'] == 1))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")