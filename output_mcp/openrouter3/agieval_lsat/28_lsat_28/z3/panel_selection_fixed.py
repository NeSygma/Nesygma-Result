from z3 import *

# Create solver
solver = Solver()

# Define scientists
botanists = ['F', 'G', 'H']
chemists = ['K', 'L', 'M']
zoologists = ['P', 'Q', 'R']
all_scientists = botanists + chemists + zoologists

# Create boolean variables for selection
selected = {s: Bool(f'selected_{s}') for s in all_scientists}

# Base constraints
# 1. Exactly 5 scientists selected
solver.add(Sum([If(selected[s], 1, 0) for s in all_scientists]) == 5)

# 2. At least one of each type
solver.add(Or([selected[b] for b in botanists]))  # At least one botanist
solver.add(Or([selected[c] for c in chemists]))   # At least one chemist
solver.add(Or([selected[z] for z in zoologists])) # At least one zoologist

# 3. If more than one botanist, then at most one zoologist
botanist_count = Sum([If(selected[b], 1, 0) for b in botanists])
zoologist_count = Sum([If(selected[z], 1, 0) for z in zoologists])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 4. F and K cannot both be selected
solver.add(Or(Not(selected['F']), Not(selected['K'])))

# 5. K and M cannot both be selected
solver.add(Or(Not(selected['K']), Not(selected['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(selected['M'], And(selected['P'], selected['R'])))

# Additional condition: P is the only zoologist selected
solver.add(selected['P'])
solver.add(Not(selected['Q']))
solver.add(Not(selected['R']))

# Now evaluate each answer choice
# For each choice, we check if the negation is satisfiable
# If negation is unsatisfiable, then the choice must be true

found_options = []

# Choice A: If K is selected, G cannot be selected
# This means: selected[K] => Not(selected[G])
# Check if this is always true by checking if its negation is satisfiable
# Negation: selected[K] AND selected[G] is possible
solver.push()
solver.add(selected['K'], selected['G'])
if solver.check() == unsat:
    found_options.append('A')
solver.pop()

# Choice B: If L is selected, F cannot be selected
# Negation: selected[L] AND selected[F] is possible
solver.push()
solver.add(selected['L'], selected['F'])
if solver.check() == unsat:
    found_options.append('B')
solver.pop()

# Choice C: If exactly one chemist is selected, it must be K
# This means: If chemist_count == 1, then that chemist is K
# Check if this is always true
# We need to check if there exists a valid model where chemist_count == 1 but the chemist is not K
solver.push()
# Add constraint that exactly one chemist is selected, but it's not K
chemist_count = Sum([If(selected[c], 1, 0) for c in chemists])
solver.add(chemist_count == 1)
solver.add(Not(selected['K']))
# Also need to ensure at least one chemist (already have that)
if solver.check() == unsat:
    found_options.append('C')
solver.pop()

# Choice D: If exactly two chemists are selected, F cannot be selected
# Check if there exists a valid model where chemist_count == 2 AND F is selected
solver.push()
chemist_count = Sum([If(selected[c], 1, 0) for c in chemists])
solver.add(chemist_count == 2)
solver.add(selected['F'])
if solver.check() == unsat:
    found_options.append('D')
solver.pop()

# Choice E: If exactly two chemists are selected, G cannot be selected
# Check if there exists a valid model where chemist_count == 2 AND G is selected
solver.push()
chemist_count = Sum([If(selected[c], 1, 0) for c in chemists])
solver.add(chemist_count == 2)
solver.add(selected['G'])
if solver.check() == unsat:
    found_options.append('E')
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")