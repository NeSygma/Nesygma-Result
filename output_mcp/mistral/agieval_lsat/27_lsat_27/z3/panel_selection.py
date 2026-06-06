from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each scientist
# Botanists: F, G, H
# Chemists: K, L, M
# Zoologists: P, Q, R
selected = {
    'F': Bool('F'),
    'G': Bool('G'),
    'H': Bool('H'),
    'K': Bool('K'),
    'L': Bool('L'),
    'M': Bool('M'),
    'P': Bool('P'),
    'Q': Bool('Q'),
    'R': Bool('R'),
}

solver = Solver()

# Base constraints
# 1. Exactly 5 scientists are selected
solver.add(Sum([selected[s] for s in selected]) == 5)

# 2. At least one of each type is selected
# Botanists: F, G, H
solver.add(Or(selected['F'], selected['G'], selected['H']))
# Chemists: K, L, M
solver.add(Or(selected['K'], selected['L'], selected['M']))
# Zoologists: P, Q, R
solver.add(Or(selected['P'], selected['Q'], selected['R']))

# 3. If more than one botanist is selected, then at most one zoologist is selected
# Count botanists
botanists = [selected['F'], selected['G'], selected['H']]
num_botanists = Sum(botanists)
# Count zoologists
zoologists = [selected['P'], selected['Q'], selected['R']]
num_zoologists = Sum(zoologists)
# Constraint: If num_botanists > 1, then num_zoologists <= 1
solver.add(Implies(num_botanists > 1, num_zoologists <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(selected['F'], selected['K'])))

# 5. K and M cannot both be selected
solver.add(Not(And(selected['K'], selected['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(selected['M'], And(selected['P'], selected['R'])))

# Given: F, L, Q, R are selected
solver.add(selected['F'])
solver.add(selected['L'])
solver.add(selected['Q'])
solver.add(selected['R'])

# Evaluate each option
found_options = []

# Option A: G is the fifth scientist
solver.push()
solver.add(selected['G'])
result_A = solver.check()
solver.pop()

# Option B: H is the fifth scientist
solver.push()
solver.add(selected['H'])
result_B = solver.check()
solver.pop()

# Option C: K is the fifth scientist
solver.push()
solver.add(selected['K'])
result_C = solver.check()
solver.pop()

# Option D: M is the fifth scientist
solver.push()
solver.add(selected['M'])
result_D = solver.check()
solver.pop()

# Option E: P is the fifth scientist
solver.push()
solver.add(selected['P'])
result_E = solver.check()
solver.pop()

# Collect valid options
if result_A == sat:
    found_options.append("A")
if result_B == sat:
    found_options.append("B")
if result_C == sat:
    found_options.append("C")
if result_D == sat:
    found_options.append("D")
if result_E == sat:
    found_options.append("E")

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